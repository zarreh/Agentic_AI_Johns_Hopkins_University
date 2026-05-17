# Agentic AI Portfolio — Master Plan

**Owner:** Alireza Zarreh  
**Target:** [zarreh.ai](http://zarreh.ai) portfolio for advisory board, consulting engagements, and student education  
**Last updated:** 2026-05-16

---

## 1. Purpose & Goals

This plan defines how to convert the JHU Agentic AI curriculum (16 weeks, 3 courses) into a portfolio of **7 deployed prototype applications**, each demonstrating a distinct agentic AI capability in a real industry domain.

### Primary audience
- **Advisory board / board of directors** prospects who want to evaluate AI strategy expertise
- **Consulting clients** looking for an AI practitioner with hands-on system-building experience
- **JHU / academic students** learning agentic AI patterns through live working examples

### What "prototype app" means here
Each app is a **production-template deployment** — not a polished product, but a credible, running demo that shows:
- A real business problem solved with an agentic AI system
- Clean architecture (not just a notebook)
- Observable agent reasoning (trace/log viewer)
- Public URL at `<name>.zarreh.ai`

### Portfolio narrative — three pillars
The 7 apps are presented on zarreh.ai under three thematic pillars so the portfolio reads as a coherent point of view, not a list of demos:

| Pillar | Story | Apps |
|---|---|---|
| **Regulated Decision Automation** | High-stakes, rule-bound decisions where AI must be auditable and policy-grounded | P1 Insurance · P5 Mortgage · P4 FAIRHire |
| **Expert Reasoning Augmentation** | Specialist domains where AI extends — not replaces — expert judgment | P3 LexAgent · P6 Clinical Governance Lab · P2 Financial |
| **Multi-Agent Knowledge Work** | Collaborative agent systems for research and analysis | P7 Research Intelligence |

### Repository model
Each app is a **standalone GitHub repository** (not a monorepo). Reasons: clean separation for forks/citations from students; independent CI/CD; clear advisory-board reading.

Inside every repo there are **two tiers** so the same codebase serves both audiences:
- **`base/`** — Educational version that closely tracks the source notebook. Students can read it alongside the JHU material.
- **`pro/`** — Production extensions (additional tools, evaluations, guardrails, UX) layered on top. This is what advisors/clients see at the live URL.

Both tiers share the same `src/` core; the extensions are additive (feature flags or separate pipeline modules), never destructive.

---

## 2. Curriculum → Portfolio Mapping

The notebooks span three courses and 16 weeks. Many later notebooks extend earlier ones. The table below shows where each app originates and how the curriculum flows into it.

| Course | Week | Notebook | Role in portfolio |
|---|---|---|---|
| Course 1 | 3 | DSPy + RAG | Foundation for P2 |
| Course 1 | 4 | Project 1 — DualLens Analytics | Core of P2 |
| Course 2 | 6 | Agentic RAG — Auto Insurance (LangChain + Smolagents) | Foundation for P1 |
| Course 2 | 8 | FAIRHire Responsible Hiring Agent | Core of P4 |
| Course 2 | 8 | Responsible E-Commerce Chat Agent | Excluded (lower priority) |
| Course 2 | 7 | MCP / Goal & Utility Agents | Excluded (conceptual) |
| Course 3 | 9 | LexAgent for Rental Law Reasoning | Core of P3 |
| Course 3 | 10 | Autonomous Financial Analyst | Enhancement for P2 |
| Course 3 | 12 | AI Research Multi-Agent System | Core of P7 |
| Course 3 | 12 | Multi-Agent LinkedIn Post Creator | Core of P7 |
| Advanced | 13 | RL CrisisCaverns / Warehouse Navigation | Excluded (educational demo) |
| Advanced | 14 | Healthcare HITL Assistant | Core of P6 |
| Advanced | 14 | MS Risk Multi-Agent Screening | Core of P6 |
| Advanced | 15 | Senior Mortgage Underwriting System | Core of P5 |
| Advanced | 16 | Insurance Agent (teaching deployment) | Superseded by P1 |

---

## 3. The 7 Portfolio Apps

---

### P1 — Insurance Claim Processing Agent ✅ DEPLOYED

**URL:** https://claim-agent.zarreh.ai  
**Repo:** `projects/claim_process_agent/`  
**Status:** Production-ready. No further changes planned.

#### What it does
Automates end-to-end auto insurance claim adjudication: ingests a claim JSON, validates it against policy records, retrieves relevant policy language via semantic search, benchmarks repair costs against market prices via web search, and produces a structured coverage decision with full reasoning trace.

#### Curriculum origin
- Week 6: First agentic RAG prototype (LangChain + Smolagents variants, ChromaDB, `policy.pdf`)
- Week 16: Teaching deployment version (single-container Streamlit + LangGraph on AWS EC2)
- `claim_process_agent/`: Full production version built on top of weeks 6 and 16

#### Architecture
```
Streamlit UI (:8504) ──REST──► FastAPI Backend (:8000)
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              CSV Validation   ChromaDB RAG    DuckDuckGo
              (policy records) (policy PDF)   (price check)
                                    │
                          LangGraph or Smolagents
                          (switchable via Hydra)
```

#### Key technical features
- **Dual agentic pipeline**: LangGraph stateful graph + Smolagents autonomous agent, switchable via Hydra config
- **Pydantic schemas**: `ClaimInfo`, `ClaimDecision`, `PolicyQueries`, `PolicyRecommendation` — full type safety
- **5-node LangGraph workflow**: `parse_claim → validate_claim → check_policy → price_check → generate_recommendation → finalize_decision`
- **Real-time price check**: DuckDuckGo web search for repair cost benchmarking (inflation detection)
- **Full test suite**: API, pipelines, retrieval, schemas, validation (pytest)
- **CI/CD**: GitHub Actions
- **Docs**: MkDocs site at `claim-agent-docs.zarreh.ai`

#### Advisory angle
> "AI can automate high-volume, rule-bound insurance adjudication while maintaining full auditability — reducing manual review costs and eliminating inconsistent decisions."

---

### P2 — Autonomous Financial Analyst 🔧 EXISTS, NEEDS ENHANCEMENT

> **Tier model:** `base/` = current DualLens 4-tab dashboard + week 10 autonomous agent tab. `pro/` = Thesis-Testing mode (see below).

**URL:** TBD (e.g., `financial-analyst.zarreh.ai`)  
**Repo:** `projects/project_1_DualLens_Analytics/`  
**Status:** Streamlit dashboard and RAG pipeline are complete. Week 10 autonomous agent layer needs to be merged in.

#### What it does
A dual-lens investment analysis platform combining:
- **Quantitative**: Real-time stock prices, 3-year price history, key financial metrics (yfinance)
- **Qualitative**: RAG-powered Q&A over company AI strategy reports (PDF → ChromaDB)
- **Autonomous agent layer** *(to be added from week10)*: LLM agent that autonomously selects from 4 tools, generates natural-language investment summaries, and runs sentiment analysis on financial news

#### Curriculum origin
- Week 3: DSPy + RAG foundation (PDF → ChromaDB, structured extraction)
- Week 4 (Project 1): DualLens Analytics — 4-tab Streamlit dashboard (Dashboard, AI Q&A, Compare, Rankings)
- Week 10: Autonomous Financial Analyst — adds `get_stock_price`, `get_stock_history`, `financial_news_search`, `sentiment_analysis` tools via `AgentExecutor`

#### Enhancement task (base tier)
Integrate the week 10 autonomous agent as a new **"Agent Analysis" tab** in the existing Streamlit dashboard. The agent replaces the manual Rankings tab logic with a fully autonomous company comparison and investment recommendation.

#### Pro-tier extension — Thesis-Testing mode
Adds an **"AI Competitive Intelligence"** tab (renamed framing for advisory audience): the user states an investment thesis (e.g., *"NVIDIA's data-center moat is durable for 5+ years"*), and a multi-agent pipeline:
1. **Bull Agent** — argues *for* the thesis using quant data + PDF evidence
2. **Bear Agent** — argues *against* using same sources
3. **Judge Agent** — scores both arguments, identifies strongest evidence, and outputs a confidence-weighted verdict

This is the artifact shown to strategy/consulting buyers; the underlying RAG + agent stack is identical to the base tier.

#### Architecture (post-enhancement)
```
Streamlit (4 + 1 tabs)
 ├── Dashboard     → yfinance (real-time metrics, Plotly charts)
 ├── AI Q&A        → LangChain RAG → ChromaDB (company PDF reports)
 ├── Compare       → RAG + yfinance side-by-side
 ├── Rankings      → LLM-ranked composite scoring
 └── Agent [NEW]   → AgentExecutor with 4 tools (autonomous multi-step analysis)
```

#### Advisory angle
> "Modern investment research requires synthesizing structured financial data with unstructured strategic intelligence — exactly what RAG + agentic AI enables at scale."

---

### P3 — LexAgent: Rental Law Reasoning Assistant 🆕 TO BUILD

**URL:** TBD (e.g., `lexagent.zarreh.ai`)  
**Source notebook:** `designing_and_building_agentic_systems/week9/MLS_9_LexAgent_for_Rental_Law_Reasoning.ipynb`  
**Template:** Use `claim_process_agent/` as project structure template

#### What it does
A legal reasoning assistant for tenants and landlords. Users describe their situation (lease dispute, eviction notice, security deposit issue, etc.) and the agent retrieves relevant law sections and past case precedents, applies jurisdiction-aware reasoning, and produces a plain-language explanation of their rights and obligations.

#### Source data
- `designing_and_building_agentic_systems/week9/tenants_rights.pdf` — Tenant rights law corpus
- `designing_and_building_agentic_systems/week9/previous_cases.pdf` — Prior case decisions

#### Architecture
```
Streamlit UI
    │
    ▼
LangGraph Agent (ReAct loop)
 ├── Tool: retrieve_tenant_rights(query) → ChromaDB (tenants_rights.pdf)
 ├── Tool: retrieve_case_precedents(query) → ChromaDB (previous_cases.pdf)
 └── Tool: interpret_law(situation, retrieved_text) → LLM structured output
    │
    ▼
Output: Rights summary + applicable law sections + relevant precedents + confidence
```

#### Key features to build
- **Dual RAG retrieval**: Separate ChromaDB collections for statute law and case precedents
- **Jurisdiction-aware prompting**: System prompt enforces caveat that advice is general, not legal counsel
- **Structured output**: Applicable statutes, relevant cases, plain-language summary, confidence score
- **Responsible AI disclaimer**: Prominent disclaimer that this is educational, not legal advice
- **Sample scenarios**: Pre-loaded example situations (eviction, deposit, lease break, repairs)

#### Advisory angle
> "Legal AI reduces access barriers to justice. A properly guardrailed RAG agent can provide reliable first-level legal orientation at near-zero cost — a 100x accessibility improvement over traditional legal consultation."

---

### P4 — FAIRHire: Responsible AI Hiring Agent 🆕 TO BUILD FIRST

> **Tier model:** `base/` = the notebook's 4-step pipeline as a working app. `pro/` = Bias Audit Report + Red-Team Test Suite (see below).

**URL:** TBD (e.g., `fairhire.zarreh.ai`)  
**Source notebook:** `introduction_to_agnetic_ai_design/week8/W8_Rec_NB_RespAI_Hiring_Agent.ipynb`  
**Sample data:** `introduction_to_agnetic_ai_design/week8/sample_resumes/`  
**Template:** Use `claim_process_agent/` as project structure template

#### Why build this first
- Responsible AI is the highest-priority topic for enterprise AI buyers in 2025–2026
- Directly demonstrates the Responsible AI skill set most valued by advisory board search committees
- The notebook has a complete pipeline that maps cleanly to a deployable app
- Unique in the portfolio: the only app explicitly about AI governance and fairness

#### What it does
Evaluates candidate resumes for a given job description while enforcing ethical guardrails to prevent biased, discriminatory, or legally non-compliant hiring decisions. Produces transparent scoring with full reasoning trace.

#### Agent pipeline (from notebook)
```
Resume Input (PDF or text)
    │
    ▼
1. PARSE — Extract skills, experience, education (structured extraction, no PII leakage)
    │
    ▼
2. GUARDRAIL CHECK — Filter out protected attributes (gender, race, age, religion, etc.)
                     Enforce fairness constraints
                     Rule-based compliance checks (EEOC, GDPR)
    │
    ▼
3. SKILL SCORING — LLM-based evaluation against job description
                   Confidence score per dimension (technical, experience, culture)
    │
    ▼
4. TRANSPARENCY REPORT — Candidate scorecard + reasoning steps + evidence citations
                         Flagged guardrail activations + human review recommendation
```

#### Key features to build
- **Resume upload**: PDF or plain text input
- **Job description input**: Free-text or structured template
- **Guardrail dashboard**: Visual display of which fairness rules activated and why
- **Multi-candidate comparison**: Side-by-side scoring of up to 5 candidates
- **Explainability panel**: Every score tied to specific resume evidence
- **Human-in-the-loop gate**: High-stakes decisions (reject) always route to human review
- **Audit log**: Immutable record of all evaluations with timestamps

#### Pro-tier extensions
- **Bias Audit Report**: Pre-built A/B comparison — same 20 resumes scored with vs without guardrails, with score deltas visualized. Single most compelling advisory-board artifact in the portfolio.
- **Red-Team Test Suite**: Adversarial test cases (name-swap, pronoun-swap, implicit-age, school-prestige proxy) with pass/fail results visible in the UI. Demonstrates *evaluated* fairness, not just claimed fairness.

#### Stack
- LangChain / Smolagents for agent orchestration (notebook uses Smolagents)
- Pydantic schemas for structured output
- FastAPI backend + Streamlit frontend (from `claim_process_agent` template)
- `pypdf` for resume parsing
- ChromaDB for job description similarity (optional: match against historical successful hires)

#### Advisory angle
> "AI hiring tools that lack guardrails expose companies to regulatory risk and reputational damage. FAIRHire shows how to build AI-augmented recruitment that is both efficient and legally defensible — a pattern every enterprise deploying AI in HR needs."

---

### P5 — Senior Mortgage Underwriting System 🆕 TO BUILD

**URL:** TBD (e.g., `mortgage-agent.zarreh.ai`)  
**Source notebook:** `advanced_agentic_aI /week15/Senior_Mortgage_Underwriting_System_Solution_Notebook.ipynb`  
**Supporting files:**
- `underwriting_policies.pdf` — Policy document corpus
- `mortgage_test_cases.json` — 10+ pre-built test scenarios
- `architecture.drawio` — System architecture diagram

#### What it does
A multi-agent system that automates senior-level mortgage underwriting decisions. Mimics the workflow of an experienced credit analyst: evaluates loan applications against underwriting policies, assesses risk factors (DTI, LTV, credit history, property type), retrieves relevant policy language, and produces a structured underwriting decision with executive summary.

#### Multi-agent architecture (from notebook)
```
Coordinator Agent
 ├── Credit Analyst Agent — Evaluates borrower financial profile (DTI, LTV, credit score)
 ├── Policy Retrieval Agent — RAG over underwriting_policies.pdf (ChromaDB)
 ├── Risk Assessment Agent — Flags risk factors, checks regulatory thresholds
 └── Decision Agent — Synthesizes inputs, generates approval/denial/conditions decision
         │
         ▼
 Executive Summary Generator — 3–5 sentence plain-language summary for loan officer
```

#### Key features to build
- **Loan application form**: Web form with all standard mortgage application fields
- **Multi-agent trace viewer**: Show which agent ran, what it retrieved, how it reasoned
- **Policy grounding**: Every decision element cites the specific policy section it applies
- **Test scenario library**: Load any of the `mortgage_test_cases.json` scenarios in one click
- **Risk dashboard**: Visual scorecard (DTI ratio, LTV, credit tier, property risk)
- **Decision output**: Approve / Deny / Approve with conditions — with full audit trail

#### Advisory angle
> "Mortgage underwriting is manual, slow, and inconsistent across loan officers. A multi-agent system that grounds every decision in policy documents while maintaining full explainability is the blueprint for compliant AI automation in regulated financial services."

---

### P6 — Clinical AI Governance Lab 🆕 TO BUILD

> **Framing note:** Renamed from "MS Risk Screener" to **Clinical AI Governance Lab**. The application is positioned as a *governance demonstration* using Synthea synthetic data — not as a screening tool. This sidesteps regulatory perception risk while preserving the technical depth of the multi-agent + HITL architecture.
>
> **Tier model:** `base/` = the notebook's MS risk multi-agent pipeline on Synthea data. `pro/` = adjustable autonomy controller + governance audit dashboard.

**URL:** TBD (e.g., `ms-screener.zarreh.ai`)  
**Source notebooks:**
- `advanced_agentic_aI /week14/Agentic_AI_Interaction_Embodiment_MS_Risk_Lab.ipynb`
- `advanced_agentic_aI /week14/healthcare_hitl_assistant.ipynb`  
**Supporting files:**
- `advanced_agentic_aI /week14/healthcare.db` — SQLite hospital patient database
- `advanced_agentic_aI /week14/synthea_data/` — Synthea-generated patient records

#### What it does
A multi-agent decision-support prototype illustrating how AI agents can operate safely in regulated clinical contexts. Using **Synthea synthetic patient data**, the system demonstrates HITL design with **adjustable autonomy** — recommend-only, semi-autonomous, or auto-escalation — and exposes a governance dashboard tracking PHI handling, audit trails, and human override rates.

> **Disclaimer displayed prominently in UI:** This is an architectural demonstration using fully synthetic data (Synthea). It is not a medical device, does not diagnose any condition, and is not validated for clinical use. The purpose is to demonstrate AI governance patterns for healthcare.

#### Multi-agent roles (from notebook)
```
Coordinator (adjustable autonomy controller)
 ├── Retrieval Agent — Query patient records from healthcare.db / Synthea data
 ├── Phenotyping Agent — Score MS risk from structured data (symptoms, history, ICD codes)
 ├── Notes/Imaging Agent — Summarize unstructured clinical notes via LLM
 └── Safety & Governance Agent — Apply PHI handling rules, escalation thresholds, audit log
         │
         ▼
 Output: Risk tier (Low/Medium/High) + Evidence summary + Recommended action + Autonomy level
```

#### HITL autonomy levels
| Level | Trigger | Agent behavior |
|---|---|---|
| Recommend-only | High-risk decisions | Agent produces suggestion; clinician must act |
| Semi-autonomous | Routine low-risk findings | Agent drafts referral; human approves |
| Auto-escalate | Emergency indicators | Agent sends alert immediately; logs action |

#### Key features to build
- **Patient cohort dashboard**: Table of screened patients with risk scores and flags
- **Autonomy slider**: Clinician-configurable autonomy level (UI control)
- **Evidence panel**: Per-patient breakdown of which signals drove the risk score
- **HITL approval queue**: List of pending recommendations awaiting clinician review
- **Governance log**: Immutable audit trail of all agent actions and human overrides
- **Responsible AI indicators**: PHI handling status, confidence calibration, false-positive rate

#### Advisory angle
> "Healthcare AI that operates without human oversight is dangerous. FAIRHire showed governance in hiring; this shows it in clinical settings — HITL design, adjustable autonomy, and transparency as core architectural requirements, not afterthoughts."

---

### P7 — Research Intelligence 🆕 TO BUILD

**URL:** TBD (e.g., `research.zarreh.ai`)  
**Source notebooks:**
- `designing_and_building_agentic_systems/week12/MLS12_AI_Research_Multi_Agent_System.ipynb`
- `designing_and_building_agentic_systems/week12/research_graph.py` (pre-built LangGraph)

> **Scope decision:** The LinkedIn Post Creator notebook is **excluded**. Keeping P7 focused purely on research intelligence makes the advisory positioning sharper and avoids consumer-feel content generation diluting the message.
>
> **Tier model:** `base/` = the notebook's research pipeline (Supervisor → Researcher → Synthesizer → Evaluator). `pro/` = source-credibility scoring + contradiction detector.

#### What it does
Given a topic or research question, a multi-agent pipeline autonomously searches arxiv + web (Tavily), synthesizes findings, evaluates source quality, and produces a structured research report with citations, identified gaps, and a confidence-weighted summary.

#### Multi-agent architecture
```
Supervisor → Research Agent (Tavily + arxiv) → Synthesis Agent → Report Generator
                                                     │
                                              Evaluation Agent
                                         (source quality + coverage)
```

#### Pro-tier extensions
- **Source-credibility scoring**: Each source is graded (peer-reviewed / preprint / industry / blog / unknown) and the report's overall confidence is weighted accordingly
- **Contradiction detector**: A dedicated agent flags where retrieved sources disagree, and surfaces the disagreement explicitly in the report rather than silently picking one side

#### Key features to build
- **Topic input**: Free-text query or pre-set topic templates
- **Agent trace viewer**: Real-time streaming of each agent's reasoning step
- **Research report output**: Structured markdown with sources, key findings, gaps, contradictions
- **Export**: Download report as PDF or markdown

#### Stack
- LangGraph for orchestration (existing `research_graph.py` as starting point)
- Tavily search API (`TAVILY_API_KEY` in `config.json`)
- `arxiv` Python library
- FastAPI + Streamlit

#### Advisory angle
> "Knowledge work — research, analysis, content creation — is the highest-leverage target for agentic AI. Multi-agent systems that collaborate, critique, and iterate mirror the way expert human teams work, and can 10x the throughput of a research or communications function."

---

## 4. Build Sequence

Starting with **P4 FAIRHire** (highest advisory value; responsible AI is the top-of-mind enterprise concern; cleanest notebook → app mapping). After P4 the order is flexible — each app is a standalone repo, so building order does not create dependencies. Likely flow:

1. **P4 FAIRHire** — establishes the template repo, base/pro tier pattern, and shared infra
2. **P5 Mortgage Underwriting** — second new build to lock in the pattern
3. **P2 Financial Analyst** — enhance existing DualLens repo
4. **P3 LexAgent**
5. **P6 Clinical AI Governance Lab**
6. **P7 Research Intelligence** (fastest, since `research_graph.py` already exists)

---

## 5. Standard Project Structure

Each app is a **standalone repository** following this template (evolved from `claim_process_agent`, with stack refinements in §6):

```
<app_name>/                       # standalone GitHub repo
├── src/<app_name>/
│   ├── api/                      # FastAPI routes and schemas
│   ├── core/                     # Business logic (shared by base + pro)
│   ├── pipelines/
│   │   ├── base/                 # Educational pipeline — tracks notebook
│   │   └── pro/                  # Production extensions (additive)
│   ├── schemas/                  # Pydantic input/output models
│   ├── settings.py               # pydantic-settings config
│   └── observability.py          # LangSmith + Langfuse callback wiring
├── frontend/
│   ├── app.py                    # Streamlit entrypoint
│   └── components/               # Modular UI components (base + pro tabs)
├── data/                         # Sample inputs, vector store persist dir
├── tests/                        # pytest suite
├── evals/                        # DeepEval test sets (logged to Langfuse)
├── Dockerfile                    # Multi-stage build
├── docker-compose.yml            # Backend + frontend services
├── Makefile                      # install / run / test / docker-* / eval
├── pyproject.toml                # uv / hatchling
├── .env.example                  # secrets template (incl. LANGCHAIN_* + LANGFUSE_*)
└── README.md                     # base/pro explanation + advisory framing
```

A **feature flag** (`PORTFOLIO_TIER=base|pro` env var) selects which pipeline tier is active at runtime — the deployed `*.zarreh.ai` instance runs `pro`; the public repo defaults to `base` so student readers see the educational version first.

---

## 6. Shared Infrastructure & Stack Choices

The stack has been re-evaluated for GenAI-first ergonomics. Key changes from the original `claim_process_agent`:

| Concern | Choice | Rationale |
|---|---|---|
| LLM | OpenAI `gpt-4o-mini` default; provider-agnostic via LangChain | Cost-effective; easy to swap |
| Embeddings | OpenAI `text-embedding-3-small` | Cheaper + better than ada-002 |
| **Vector store** | **Qdrant** (primary) · ChromaDB (embedded fallback for small demos) | Qdrant: production-grade, Rust core, excellent filtering, generous free cloud tier; ChromaDB stays for ultra-light embedded demos |
| **Config** | **`pydantic-settings`** (replaces Hydra) | Hydra is overkill for GenAI apps; `pydantic-settings` is idiomatic Python 3.12, type-safe, env-var native, and is what the LangChain/LangGraph ecosystem uses |
| **Observability — dev** | **LangSmith** (private, SaaS) | Daily-driver tracing & debugging during build; native LangChain/LangGraph UX |
| **Observability — public** | **Langfuse** (self-hosted, single instance for all 7 apps) | Drives the public `evals.zarreh.ai` dashboard — LangSmith dashboards cannot be exposed publicly; Langfuse can. Each app emits traces to *both* via LangChain's multi-callback mechanism (~10 lines of config per app) |
| Eval framework | DeepEval (per-repo test sets) → results logged to Langfuse | Local CI gates + central visibility |
| Agent framework | LangGraph (default) · Smolagents where notebook uses it | Already established in curriculum |
| Logging | Loguru | Carry over from claim_process_agent |
| Secrets | `.env` per repo, never committed; `.env.example` template | Standard |
| Deployment | Docker Compose per app; each app at its own `*.zarreh.ai` subdomain | Independent lifecycle |
| Package mgmt | **`uv`** + `pyproject.toml` (hatchling backend) — replaces Poetry | Faster, already the workspace standard |
| Python version | 3.12+ | |

### Cross-cutting: dual observability
Each app sends traces to **two backends in parallel** via LangChain's callback mechanism:

1. **LangSmith** (private) — daily development, debugging, prompt iteration. SaaS, what most LangChain enterprises actually use.
2. **Langfuse** (self-hosted at `langfuse.zarreh.ai`, private endpoint) — production telemetry sink that feeds the **public** `evals.zarreh.ai` dashboard.

This split keeps the dev workflow ergonomic (LangSmith) while giving the portfolio a public-facing metrics story that LangSmith alone cannot deliver (its dashboards are workspace-internal). Both are wired via env vars; no code coupling between the two.

The public dashboard at `evals.zarreh.ai` shows aggregated metrics across the portfolio:
- Hallucination rate (DeepEval) per app
- Guardrail activation counts (P4, P5, P6)
- Avg tokens / latency / cost per request per app
- Trace samples (sanitized)

This is the single most differentiating asset for advisory-board audiences and **does not require coupling the repos** — it's a shared backend, not shared code.

### Cost / latency transparency
Each app card on zarreh.ai displays a small live badge: **avg tokens · avg latency · est. cost per request**, sourced from the Langfuse instance. Boards rarely see unit economics on AI demos; surfacing them positions the work as operationally serious.

---

## 7. Portfolio Presentation Strategy

### Per-app card on `zarreh.ai`
1. **Problem statement** (1–2 sentences: what pain does this solve?)
2. **Pillar badge** — Regulated Decision Automation / Expert Reasoning Augmentation / Multi-Agent Knowledge Work
3. **Live demo link** (`*.zarreh.ai`)
4. **Live ops badge** — avg tokens · latency · cost/request (from Langfuse)
5. **Architecture diagram** (simple flowchart)
6. **Tech stack badges**
7. **Key design decisions** (2–3 bullets on the interesting agentic patterns used)
8. **Base vs Pro** — short note on what's in the educational base tier vs the advisory pro tier
9. **Repo + source notebook** links
10. **CTA**: *"This pattern applied to your domain — let's talk."*

### Shared assets (built once, linked from every app)
- **`zarreh.ai/methodology`** — single page explaining the standard architecture (FastAPI + LangGraph + pydantic-settings + Qdrant + Langfuse + DeepEval). Removes the need to repeat stack details on every app card.
- **`evals.zarreh.ai`** — Langfuse-backed dashboard showing cross-portfolio evaluation metrics.
- **`docs.zarreh.ai`** — single central documentation site (one MkDocs project in its own repo), with a section per app pulling READMEs or curated content. Avoids running MkDocs per app.

### Advisory framing
> *"Each of these prototypes demonstrates a production-ready agentic AI pattern in a specific industry domain. The base tier mirrors the educational notebook so students can learn from it; the pro tier shows the additional engineering — evaluation, guardrails, governance, observability — required to deploy it in a regulated enterprise."*

---

## 8. Excluded Items (and why)

| Content | Reason excluded |
|---|---|
| Week 1–2: Shopping Cart, Password Manager, Prompt Engineering | Too elementary; target audience already understands basic LLM usage |
| Week 7: MCP / Goal-Utility Agents | Conceptual demonstrations without a standalone app domain |
| Week 13: RL CrisisCaverns / Warehouse Navigation | Educational RL demo; better presented as a blog post with the animated GIFs already in the repo |
| Week 8: Responsible E-Commerce Chat Agent | Covered thematically by FAIRHire (P4); can be added later as a lightweight extension |
| Week 12: Multi-Agent LinkedIn Post Creator | Consumer-feel content generation dilutes advisory positioning; P7 is research-only |

---

## 9. Key Files Reference

| App | Primary source notebook | Supporting data |
|---|---|---|
| P1 | `week6/MLS6_AgenticRAG_LangChain.ipynb` | `week6/policy.pdf`, `week6/coverage_data.csv` |
| P2 | `week4/JHU_AgenticAI_Project_1_Solution_Notebook.ipynb` | `week10/Companies-AI-Initiatives/` (PDF corpus) |
| P2 (enhance) | `week10/Autonomous_financial_analyst_Solution_Notebook.ipynb` | yfinance (live), Tavily (news) |
| P3 | `week9/MLS_9_LexAgent_for_Rental_Law_Reasoning.ipynb` | `week9/tenants_rights.pdf`, `week9/previous_cases.pdf` |
| P4 | `week8/W8_Rec_NB_RespAI_Hiring_Agent.ipynb` | `week8/sample_resumes/` |
| P5 | `week15/Senior_Mortgage_Underwriting_System_Solution_Notebook.ipynb` | `week15/underwriting_policies.pdf`, `week15/mortgage_test_cases.json` |
| P6 | `week14/Agentic_AI_Interaction_Embodiment_MS_Risk_Lab.ipynb` + `healthcare_hitl_assistant.ipynb` | `week14/healthcare.db`, `week14/synthea_data/` |
| P7 | `week12/Multi-Agent LinkedIn Post Creator.ipynb` + `MLS12_AI_Research_Multi_Agent_System.ipynb` | `week12/research_graph.py` |
