# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a course repository for JHU Agentic AI, containing Jupyter notebooks organized by week covering topics from basic agent development to advanced prompt engineering, DSPy, and RAG systems.

## Environment Setup

### Package Manager
This project uses `uv` as the package manager (installed at `~/.local/bin/uv`). Do NOT use pip directly.

### Virtual Environment
Always activate the virtual environment before running any code:
```bash
source .venv/bin/activate
# or
source activate.sh
```

### Python Version
Python 3.12+ is required.

## Common Commands

### Package Management
```bash
# Install a new package
uv pip install package-name

# Update requirements.txt after installing packages
uv pip freeze > requirements.txt

# Reinstall from requirements.txt
uv pip install -r requirements.txt
```

### Running Notebooks
```bash
# Start Jupyter Notebook
jupyter notebook

# Start Jupyter Lab
jupyter lab
```

## Configuration

### API Keys (config.json)
Many notebooks require OpenAI API credentials in a `config.json` file. Use `config.json.example` as a template:
```json
{
  "API_KEY": "your-openai-api-key-here",
  "OPENAI_API_BASE": "https://api.openai.com/v1"
}
```

This file should be created in:
- The root directory for general use
- Individual week directories if notebooks reference it locally

## Repository Structure

```
prompt_engineering/
├── week1/     # Shopping Cart Management, Password Manager (using Gradio)
├── week2/     # Prompt Engineering Fundamentals (OpenAI, HuggingFace)
└── week3/     # DSPy Introduction and RAG systems
```

### Week-by-Week Content

**Week 1**: Basic agentic applications using Gradio for UI
- Shopping cart management systems
- Password manager implementations

**Week 2**: Prompt engineering fundamentals
- Two variants: OpenAI-based and HuggingFace-based
- Practical prompt engineering techniques for business scenarios

**Week 3**: Advanced frameworks
- Introduction to DSPy (structured prompting framework)
- RAG (Retrieval Augmented Generation) implementation with DSPy
- Uses ChromaDB for vector storage
- PDF processing with pypdf

## Key Dependencies by Week

**Week 1**: `gradio`

**Week 2 & 3**:
- `langchain-openai==0.3.24` - Primary LangChain integration
- `dspy==3.0.3` - DSPy framework for structured prompting
- `langchain>=0.2.0` and related packages (community, core, text-splitters)
- `chromadb>=0.5.0` - Vector database for RAG
- `tiktoken>=0.7.0` - Token counting
- `pypdf>=4.0.0` - PDF processing

## Architecture Notes

### Notebook Organization
- Notebooks are self-contained with markdown explanations
- Business context typically provided at the beginning
- Code cells often include inline documentation
- Some notebooks have variant versions (e.g., with/without prompts, different LLM providers)

### Configuration Pattern
Notebooks load configuration from `config.json` using:
```python
import json
with open('config.json') as f:
    config = json.load(f)
```

### Week 3 RAG Architecture
- Uses DSPy for structured prompting and optimization
- ChromaDB for vector storage and retrieval
- PDF documents loaded from local files (e.g., `HBR_How_Apple_Is_Organized_For_Innovation.pdf`)
- Text splitting with LangChain text splitters
- Embedding and retrieval pipeline built with DSPy modules
