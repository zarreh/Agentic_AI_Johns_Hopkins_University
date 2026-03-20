# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A three-course JHU Agentic AI curriculum delivered as Jupyter notebooks, progressing from prompt engineering fundamentals through advanced agentic system design.

## Environment Setup

- Package manager: `uv` (at `~/.local/bin/uv`). Do NOT use pip directly.
- Python 3.12+ required.
- Activate venv before running anything: `source .venv/bin/activate` or `source activate.sh`

### Package Management
```bash
uv pip install package-name
uv pip freeze > requirements.txt
uv pip install -r requirements.txt
```

### Running Notebooks
```bash
jupyter notebook   # or: jupyter lab
```

## Configuration

Notebooks load API keys from `config.json` (git-ignored). Copy `config.json.example`:
```json
{
  "API_KEY": "your-openai-api-key-here",
  "OPENAI_API_BASE": "https://api.openai.com/v1",
  "TAVILY_API_KEY": "tvly-dev-xxxxxxxxxxxxxx"
}
```

Place `config.json` in the root and/or the individual week directory if a notebook references it locally. Notebooks load it with:
```python
import json
with open('config.json') as f:
    config = json.load(f)
```

## Repository Structure

Three courses plus two full projects:

```
prompt_engineering/          # Course 1
├── week1/                   # Gradio UI apps (shopping cart, password manager)
├── week2/                   # Prompt engineering (OpenAI + HuggingFace variants)
├── week3/                   # DSPy + RAG with ChromaDB
└── week4/                   # Project 1 (learner + solution notebooks)

introduction_to_agnetic_ai_design/   # Course 2
├── week6/                   # Agentic RAG (LangChain + Smolagents variants)
├── week7/                   # MCP, goal-based/utility-based agents
└── week8/                   # Ethics, responsible AI hiring/e-commerce agents

Designing and Building Agentic Systems/  # Course 3
├── week9/                   # LangGraph basics, ReAct vs Plan-and-Execute, LexAgent
├── week10/                  # (placeholder)
└── week11/                  # (placeholder)

projects/
├── project_1_DualLens_Analytics/   # Full project with src/, tests/, Docker, CI/CD
└── claim_process_agent/            # Claims processing agent with frontend
```

## Key Frameworks by Course

| Course | Frameworks |
|--------|-----------|
| Course 1 (weeks 1–4) | Gradio, DSPy, ChromaDB, LangChain |
| Course 2 (weeks 6–8) | LangChain, Smolagents, MCP |
| Course 3 (weeks 9+) | LangGraph, DeepEval |

Core shared dependencies: `langchain-openai==0.3.24`, `dspy==3.0.3`, `chromadb==1.4.1`, `smolagents==1.24.0`, `langgraph==1.1.3`, `deepeval==3.9.2`

## Architecture Notes

- **Notebooks are self-contained** — each week's notebooks include setup, context, and teardown. Some weeks have multiple variants (e.g., OpenAI vs HuggingFace, with/without prompts, enhanced vs standard Smolagents).
- **RAG pattern (week 3+)**: DSPy modules → LangChain text splitters → ChromaDB vector store → PDF source documents stored alongside notebooks.
- **Agentic patterns (week 9)**: LangGraph for stateful graph-based agents; ReAct vs rigid Plan-and-Execute comparison; domain-specific agents (LexAgent for rental law) backed by local PDF corpora.
- **Projects** follow standard Python project layout (`src/`, `tests/`, `pyproject.toml`, Docker) and are intended to become standalone repositories (listed in `.gitignore`).
- **DeepEval** artifacts land in `.deepeval/` (git-ignored) — used for evaluation in week 9+.
