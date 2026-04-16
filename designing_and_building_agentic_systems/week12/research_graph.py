"""
research_graph.py
-----------------
Standalone module exporting the compiled LangGraph research pipeline
for use with `langgraph dev` / LangGraph Studio.

Usage:
    cd designing_and_building_agentic_systems/week12
    langgraph dev
"""

import json
import time
import uuid
import logging
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, TypedDict, Literal
from enum import Enum

import arxiv
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langchain.agents import create_agent

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from openai import APIError, RateLimitError, APITimeoutError

load_dotenv(override=True)

# --- Load API keys from config.json (two levels up from week12/) ---
_config_paths = [
    os.path.join(os.path.dirname(__file__), "../../config.json"),
    os.path.join(os.path.dirname(__file__), "../../../config.json"),
    os.path.join(os.path.dirname(__file__), "config.json"),
]
for _cp in _config_paths:
    if os.path.exists(_cp):
        with open(_cp) as _f:
            _cfg = json.load(_f)
        os.environ.setdefault("OPENAI_API_KEY", _cfg.get("API_KEY", ""))
        os.environ.setdefault("OPENAI_API_BASE", _cfg.get("OPENAI_API_BASE", ""))
        break

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("research_system")


# ---------------------------------------------------------------------------
# State Definition
# ---------------------------------------------------------------------------

class ResearchPhase(Enum):
    INITIALIZATION = "initialization"
    PLANNING = "planning"
    DISCOVERY = "discovery"
    EVALUATION = "evaluation"
    COMPLETION = "completion"


class ResearchSystemState(TypedDict):
    request_id: str
    research_objective: str
    current_phase: ResearchPhase
    phase_history: List[Dict[str, Any]]
    discovered_papers: List[Dict[str, Any]]
    evaluation_results: List[Dict[str, Any]]
    synthesis_data: Optional[Dict[str, Any]]
    final_report: Optional[str]
    messages: List[BaseMessage]
    errors: List[Dict[str, Any]]
    total_processing_time: float


# ---------------------------------------------------------------------------
# LLM Retry Helper
# ---------------------------------------------------------------------------

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((APIError, RateLimitError, APITimeoutError)),
)
def call_llm(llm, messages):
    return llm.invoke(messages)


# ---------------------------------------------------------------------------
# ArXiv Discovery Tool
# ---------------------------------------------------------------------------

def search_arxiv(
    query: str,
    max_papers: int = 10,
    from_date: str = None,
    to_date: str = None,
) -> List[Dict[str, Any]]:
    logger.info(
        f"ArXiv search: query='{query}', max={max_papers}, "
        f"from={from_date}, to={to_date}"
    )
    try:
        categories = ["cs.AI", "cs.LG", "cs.CL", "cs.CV", "cs.NE"]
        cat_filter = " OR ".join(f"cat:{c}" for c in categories)
        full_query = f"({query}) AND ({cat_filter})"

        if from_date or to_date:
            fd = (
                datetime.strptime(from_date, "%Y-%m-%d").strftime("%Y%m%d0000")
                if from_date
                else "202001010000"
            )
            td = (
                datetime.strptime(to_date, "%Y-%m-%d").strftime("%Y%m%d2359")
                if to_date
                else datetime.now().strftime("%Y%m%d2359")
            )
            full_query += f" AND submittedDate:[{fd} TO {td}]"

        client = arxiv.Client()
        search = arxiv.Search(
            query=full_query,
            max_results=max_papers,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        papers = []
        for r in client.results(search):
            papers.append(
                {
                    "id": r.get_short_id(),
                    "title": r.title,
                    "link": r.entry_id,
                    "metadata": {
                        "authors": [
                            {"name": a.name, "affiliation": ""}
                            for a in r.authors
                        ],
                        "abstract": r.summary.replace("\n", " ").strip(),
                        "published_date": r.published.isoformat(),
                        "updated_date": r.updated.isoformat(),
                        "categories": r.categories,
                        "source": "arxiv",
                        "doi": getattr(r, "doi", None),
                        "journal_ref": getattr(r, "journal_ref", None),
                    },
                }
            )
        return papers
    except Exception as e:
        logger.error(f"ArXiv search failed: {e}")
        return []


@tool
def discover_and_process_papers(
    query: str,
    max_papers: int = 10,
    from_date: str = None,
    to_date: str = None,
) -> Dict[str, Any]:
    """Complete discovery workflow: search arXiv, deduplicate, and validate."""
    start_time = time.time()
    papers = search_arxiv(query, max_papers, from_date, to_date)

    seen_titles, unique_papers = set(), []
    for p in papers:
        norm = re.sub(r"\s+", " ", p["title"].lower().strip())
        if norm not in seen_titles:
            seen_titles.add(norm)
            unique_papers.append(p)

    valid_papers = [
        p
        for p in unique_papers
        if p.get("title")
        and len(p.get("metadata", {}).get("abstract", "")) >= 50
    ]

    return {
        "processed_papers": valid_papers,
        "statistics": {
            "initial_count": len(papers),
            "after_deduplication": len(unique_papers),
            "final_count": len(valid_papers),
            "duplicates_removed": len(papers) - len(unique_papers),
            "invalid_removed": len(unique_papers) - len(valid_papers),
            "processing_time": f"{time.time() - start_time:.2f}s",
        },
        "source_counts": {"arxiv": len(valid_papers)},
        "search_metadata": {
            "query_used": query,
            "date_range": (
                f"{from_date} to {to_date}"
                if from_date or to_date
                else "all_time"
            ),
            "sources_searched": ["arxiv"],
            "processing_timestamp": datetime.now().isoformat(),
        },
    }


DISCOVERY_TOOLS = [discover_and_process_papers]


# ---------------------------------------------------------------------------
# AGI Evaluation Framework
# ---------------------------------------------------------------------------

AGI_PARAMETERS = {
    "novel_problem_solving":     {"weight": 0.15, "desc": "Solving new, unseen problems"},
    "few_shot_learning":         {"weight": 0.15, "desc": "Learning from minimal examples"},
    "task_transfer":             {"weight": 0.15, "desc": "Applying skills across domains"},
    "abstract_reasoning":        {"weight": 0.12, "desc": "Logical thinking & pattern recognition"},
    "contextual_adaptation":     {"weight": 0.10, "desc": "Adapting behaviour to context"},
    "multi_rule_integration":    {"weight": 0.10, "desc": "Following multiple complex rules"},
    "generalization_efficiency": {"weight": 0.08, "desc": "Generalizing from small data"},
    "meta_learning":             {"weight": 0.08, "desc": "Learning how to learn"},
    "world_modeling":            {"weight": 0.04, "desc": "Modeling complex environments"},
    "autonomous_goal_setting":   {"weight": 0.03, "desc": "Setting & pursuing own objectives"},
}


def calculate_agi_score(parameter_scores: Dict[str, float]) -> tuple:
    total_weighted, total_weight = 0.0, 0.0
    contributions = {}

    for name, cfg in AGI_PARAMETERS.items():
        if name in parameter_scores:
            score = parameter_scores[name]
            weight = cfg["weight"]
            contrib = score * weight
            total_weighted += contrib
            total_weight += weight
            contributions[name] = {
                "score": score,
                "weight": weight,
                "contribution": round(contrib, 1),
            }

    final = (total_weighted / total_weight) * 10 if total_weight > 0 else 0.0
    final = round(final, 1)
    classification = (
        "High AGI Potential"
        if final >= 70
        else ("Medium AGI Potential" if final >= 40 else "Low AGI Potential")
    )
    return final, {
        "final_score": final,
        "classification": classification,
        "parameter_contributions": contributions,
        "total_weight_used": total_weight,
    }


def get_agi_evaluation_prompt(title: str, abstract: str, authors: List[str]) -> str:
    return f"""EVALUATE THIS RESEARCH PAPER FOR AGI POTENTIAL

## PAPER DETAILS
**Title:** {title}
**Authors:** {", ".join(authors[:5])}
**Abstract:** {abstract}

Rate each AGI parameter on a 1-10 scale and return ONLY valid JSON:
{{
    "parameter_scores": {{
        "novel_problem_solving": {{"score": X, "reasoning": "..."}},
        "few_shot_learning": {{"score": X, "reasoning": "..."}},
        "task_transfer": {{"score": X, "reasoning": "..."}},
        "abstract_reasoning": {{"score": X, "reasoning": "..."}},
        "contextual_adaptation": {{"score": X, "reasoning": "..."}},
        "multi_rule_integration": {{"score": X, "reasoning": "..."}},
        "generalization_efficiency": {{"score": X, "reasoning": "..."}},
        "meta_learning": {{"score": X, "reasoning": "..."}},
        "world_modeling": {{"score": X, "reasoning": "..."}},
        "autonomous_goal_setting": {{"score": X, "reasoning": "..."}}
    }},
    "overall_agi_assessment": "2-3 sentence summary",
    "key_innovations": ["innovation1", "innovation2"],
    "limitations": ["limitation1"],
    "confidence_level": "High/Medium/Low"
}}"""


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def _clean_llm_json(text: str) -> str:
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        text = text[start:end] if end > start else text[start:]
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        text = text[start:end] if end > start else text[start:]
    json_start = text.find("{")
    json_end = text.rfind("}") + 1
    if json_start < 0 or json_end <= json_start:
        return ""
    text = text[json_start:json_end]
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", text)
    return text


def _parse_eval_json(text: str) -> dict:
    cleaned = _clean_llm_json(text)
    if not cleaned:
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    fixed = re.sub(r",\s*([}\]])", r"\1", cleaned)
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    try:
        scores = {}
        for param in AGI_PARAMETERS:
            pattern = rf'"{param}"\s*:\s*\{{\s*"score"\s*:\s*(\d+(?:\.\d+)?)'
            match = re.search(pattern, cleaned)
            if match:
                scores[param] = {
                    "score": float(match.group(1)),
                    "reasoning": "extracted via fallback",
                }
        if scores:
            assessment_match = re.search(
                r'"overall_agi_assessment"\s*:\s*"([^"]*)"', cleaned
            )
            return {
                "parameter_scores": scores,
                "overall_agi_assessment": (
                    assessment_match.group(1) if assessment_match else ""
                ),
                "key_innovations": [],
                "limitations": [],
                "confidence_level": "Medium",
            }
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Graph Nodes
# ---------------------------------------------------------------------------

def planner_node(state: ResearchSystemState) -> ResearchSystemState:
    logger.info("=== PLANNER NODE ===")
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
    objective = state.get("research_objective", "")
    today = datetime.now().strftime("%Y-%m-%d")

    system_prompt = """You are a Research Planning Specialist. Create a JSON execution plan.

CRITICAL: Derive the date range from the user's query:
- "last one week" → 7 days back
- "last two weeks" → 14 days back
- "last month" → 30 days back
- No time period → default 7 days back

Return ONLY valid JSON:
{
    "search_keywords": ["keyword1", ...],
    "search_strategy": {
        "primary_sources": ["arxiv"],
        "categories": ["cs.AI", "cs.LG", "cs.CL"],
        "date_range": "YYYY-MM-DD to YYYY-MM-DD",
        "max_papers_per_source": 10
    },
    "focus_areas": ["area1", "area2"],
    "exclusions": []
}"""

    user_prompt = (
        f"Research Objective: {objective}\n"
        f"Today: {today}\n"
        f"7 days ago: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}\n"
        f"14 days ago: {(datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')}\n"
        f"30 days ago: {(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')}\n\n"
        "Generate the execution plan now."
    )

    try:
        response = call_llm(
            llm,
            [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)],
        )
        plan_text = response.content
        if "```json" in plan_text:
            s = plan_text.find("```json") + 7
            e = plan_text.find("```", s)
            plan_text = plan_text[s:e]
        elif "```" in plan_text:
            s = plan_text.find("```") + 3
            e = plan_text.find("```", s)
            plan_text = plan_text[s:e]
        plan = json.loads(plan_text.strip())
    except Exception as e:
        logger.error(f"Planning failed: {e}")
        fallback_start = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        plan = {
            "search_keywords": ["AGI", "artificial general intelligence"],
            "search_strategy": {
                "primary_sources": ["arxiv"],
                "categories": ["cs.AI", "cs.LG"],
                "date_range": f"{fallback_start} to {today}",
                "max_papers_per_source": 10,
            },
            "focus_areas": ["artificial general intelligence"],
            "exclusions": [],
        }

    if state.get("synthesis_data") is None:
        state["synthesis_data"] = {}
    state["synthesis_data"]["execution_plan"] = plan
    state["synthesis_data"]["plan_created_at"] = datetime.now().isoformat()
    return state


def discovery_node(state: ResearchSystemState) -> ResearchSystemState:
    logger.info("=== DISCOVERY NODE ===")
    plan = state.get("synthesis_data", {}).get("execution_plan", {})
    if not plan:
        state["discovered_papers"] = []
        return state

    llm = ChatOpenAI(model_name="gpt-4o-mini")
    agent_system_prompt = (
        "You are the Discovery Agent. Call discover_and_process_papers EXACTLY ONCE "
        "using 2-3 keywords, and the from_date/to_date from the plan."
    )
    agent = create_agent(
        model=llm,
        tools=DISCOVERY_TOOLS,
        system_prompt=agent_system_prompt,
    )

    date_range = plan.get("search_strategy", {}).get("date_range", "")
    from_date, to_date = None, None
    if " to " in date_range:
        parts = date_range.split(" to ")
        from_date, to_date = parts[0].strip(), parts[1].strip()

    max_papers = plan.get("search_strategy", {}).get("max_papers_per_source", 10)

    input_message = (
        f"EXECUTION PLAN:\n"
        f"Keywords: {plan.get('search_keywords', [])}\n"
        f"Date Range: {from_date} to {to_date}\n"
        f"Max Papers: {max_papers}\n\n"
        f'Call discover_and_process_papers with query, from_date="{from_date}", '
        f'to_date="{to_date}", max_papers={max_papers}.'
    )

    try:
        result = agent.invoke({"messages": [HumanMessage(content=input_message)]})
        discovered_papers = []
        for msg in result.get("messages", []):
            if type(msg).__name__ != "ToolMessage":
                continue
            try:
                content = (
                    json.loads(msg.content)
                    if isinstance(msg.content, str)
                    else msg.content
                )
                if isinstance(content, dict) and "processed_papers" in content:
                    discovered_papers = content["processed_papers"]
                    if state.get("synthesis_data") is None:
                        state["synthesis_data"] = {}
                    state["synthesis_data"]["discovery_metadata"] = {
                        "statistics": content.get("statistics", {}),
                        "search_metadata": content.get("search_metadata", {}),
                    }
                    break
            except (json.JSONDecodeError, TypeError):
                continue
        state["discovered_papers"] = discovered_papers
    except Exception as e:
        logger.error(f"Discovery failed: {e}")
        state["discovered_papers"] = []
        state.setdefault("errors", []).append(
            {"phase": "discovery", "error": str(e), "timestamp": datetime.now().isoformat()}
        )
    return state


def evaluation_node(state: ResearchSystemState) -> ResearchSystemState:
    logger.info("=== EVALUATION NODE ===")
    papers = state.get("discovered_papers", [])
    if not papers:
        state["evaluation_results"] = []
        return state

    llm = ChatOpenAI(model_name="gpt-4o-mini")
    system_msg = SystemMessage(
        content=(
            "You are an expert AGI evaluator. Return ONLY valid JSON. "
            "Keep reasoning strings under 100 characters."
        )
    )

    results = []
    total_score = 0.0

    for i, paper in enumerate(papers, 1):
        title = paper.get("title", "Unknown")
        metadata = paper.get("metadata", {})
        abstract = metadata.get("abstract", "")
        authors_raw = metadata.get("authors", [])
        author_names = [
            (a.get("name", "Unknown") if isinstance(a, dict) else a)
            for a in authors_raw
        ]

        if len(abstract) < 50:
            continue

        try:
            response = call_llm(
                llm,
                [system_msg, HumanMessage(content=get_agi_evaluation_prompt(title, abstract, author_names))],
            )
            eval_data = _parse_eval_json(response.content)
            if eval_data is None:
                continue

            param_scores = {
                k: v["score"]
                for k, v in eval_data.get("parameter_scores", {}).items()
                if isinstance(v, dict) and "score" in v
            }
            weighted_score, breakdown = calculate_agi_score(param_scores)

            results.append(
                {
                    "paper_id": paper.get("id", f"paper_{i}"),
                    "paper_title": title,
                    "paper_authors": author_names,
                    "paper_source": metadata.get("source", "unknown"),
                    "paper_url": paper.get("link", ""),
                    "evaluation_timestamp": datetime.now().isoformat(),
                    "agi_score": weighted_score,
                    "agi_classification": breakdown["classification"],
                    "parameter_scores": eval_data.get("parameter_scores", {}),
                    "overall_assessment": eval_data.get("overall_agi_assessment", ""),
                    "key_innovations": eval_data.get("key_innovations", []),
                    "limitations": eval_data.get("limitations", []),
                    "confidence_level": eval_data.get("confidence_level", "Medium"),
                    "score_breakdown": breakdown,
                }
            )
            total_score += weighted_score
        except Exception as e:
            logger.error(f"Error evaluating paper {i}: {e}")

    state["evaluation_results"] = results
    avg_score = round(total_score / len(results), 1) if results else 0
    eval_meta = {
        "total_papers": len(papers),
        "successful_evaluations": len(results),
        "avg_agi_score": avg_score,
        "score_distribution": {
            "high": len([r for r in results if r["agi_score"] >= 70]),
            "medium": len([r for r in results if 40 <= r["agi_score"] < 70]),
            "low": len([r for r in results if r["agi_score"] < 40]),
        },
    }
    if state.get("synthesis_data") is None:
        state["synthesis_data"] = {}
    state["synthesis_data"]["evaluation_metadata"] = eval_meta
    return state


def _generate_final_report(state: ResearchSystemState) -> str:
    results = state.get("evaluation_results", [])
    papers = state.get("discovered_papers", [])
    meta = state.get("synthesis_data", {}).get("evaluation_metadata", {})

    if not results:
        return (
            f"# AGI Research Analysis Report\n\n"
            f"**Objective:** {state.get('research_objective', 'N/A')}\n\n"
            f"No papers were successfully evaluated.\n"
        )

    sorted_results = sorted(results, key=lambda x: x.get("agi_score", 0), reverse=True)
    avg = meta.get("avg_agi_score", 0)
    dist = meta.get("score_distribution", {})

    report = (
        f"# AGI Research Analysis Report\n\n"
        f"**Research Objective:** {state.get('research_objective', 'N/A')}\n\n"
        f"**Papers discovered:** {len(papers)} | **Evaluated:** {len(results)} | "
        f"**Avg AGI score:** {avg:.1f}/100\n\n"
        f"High: {dist.get('high', 0)} | Medium: {dist.get('medium', 0)} | "
        f"Low: {dist.get('low', 0)}\n\n## Top Papers\n\n"
    )
    for i, p in enumerate(sorted_results[:5], 1):
        report += (
            f"### {i}. {p['paper_title']}\n"
            f"**AGI Score:** {p['agi_score']}/100 ({p['agi_classification']})\n"
            f"**Assessment:** {p.get('overall_assessment', 'N/A')}\n\n"
        )
    report += f"\n---\n*Generated: {datetime.now():%Y-%m-%d %H:%M:%S}*\n"
    return report


def supervisor_node(state: ResearchSystemState) -> ResearchSystemState:
    logger.info("=== SUPERVISOR NODE ===")
    phase = state.get("current_phase", ResearchPhase.INITIALIZATION)

    if phase == ResearchPhase.INITIALIZATION:
        if not state.get("request_id"):
            state["request_id"] = str(uuid.uuid4())
        state["current_phase"] = ResearchPhase.PLANNING

    elif phase == ResearchPhase.PLANNING:
        if state.get("synthesis_data", {}).get("execution_plan"):
            state["current_phase"] = ResearchPhase.DISCOVERY
        else:
            state["current_phase"] = ResearchPhase.COMPLETION
            state["final_report"] = "Failed to create execution plan."

    elif phase == ResearchPhase.DISCOVERY:
        if len(state.get("discovered_papers", [])) > 0:
            state["current_phase"] = ResearchPhase.EVALUATION
        else:
            state["current_phase"] = ResearchPhase.COMPLETION
            state["final_report"] = "No papers discovered."

    elif phase == ResearchPhase.EVALUATION:
        state["final_report"] = _generate_final_report(state)
        state["current_phase"] = ResearchPhase.COMPLETION

    return state


def route_next_phase(
    state: ResearchSystemState,
) -> Literal["planner", "discovery", "evaluation", "complete"]:
    phase = state.get("current_phase", ResearchPhase.INITIALIZATION)
    return {
        ResearchPhase.PLANNING: "planner",
        ResearchPhase.DISCOVERY: "discovery",
        ResearchPhase.EVALUATION: "evaluation",
    }.get(phase, "complete")


# ---------------------------------------------------------------------------
# Build Graph  ←  this is what langgraph dev exposes
# ---------------------------------------------------------------------------

def build_research_graph():
    g = StateGraph(ResearchSystemState)
    g.add_node("supervisor", supervisor_node)
    g.add_node("planner", planner_node)
    g.add_node("discovery", discovery_node)
    g.add_node("evaluation", evaluation_node)
    g.add_edge(START, "supervisor")
    g.add_conditional_edges(
        "supervisor",
        route_next_phase,
        {
            "planner": "planner",
            "discovery": "discovery",
            "evaluation": "evaluation",
            "complete": END,
        },
    )
    for n in ["planner", "discovery", "evaluation"]:
        g.add_edge(n, "supervisor")
    return g.compile()


# The variable `graph` is what langgraph.json points to.
graph = build_research_graph()
