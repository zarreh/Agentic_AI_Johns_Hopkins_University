# Agentic AI JHU - Course Repository

This repository contains Jupyter notebooks for the JHU Agentic AI course.

## Setup Instructions

### Prerequisites
- Python 3.12+ (detected: 3.12.10)
- uv package manager (installed at `~/.local/bin/uv`)

### Installation

All dependencies have been installed using `uv` in a virtual environment.

### Activation

To activate the virtual environment:

```bash
source .venv/bin/activate
```

Or use the provided script:

```bash
source activate.sh
```

### Dependencies

The following packages are installed:

**Week 1 - Shopping Cart Management:**
- gradio

**Week 2 & 3 - Prompt Engineering, DSPy, and RAG:**
- langchain-openai==0.3.24
- dspy==3.0.3
- langchain>=0.2.0 (and related packages)
- chromadb>=0.5.0
- tiktoken>=0.7.0
- pypdf>=4.0.0

**Data Science:**
- numpy
- pandas

### Running Notebooks

1. Activate the virtual environment (see above)
2. Start Jupyter:
   ```bash
   jupyter notebook
   ```
   or
   ```bash
   jupyter lab
   ```
3. Navigate to the desired week folder and open notebooks

### Configuration

Some notebooks require a `config.json` file with your OpenAI API credentials:

```json
{
  "API_KEY": "your-api-key-here",
  "OPENAI_API_BASE": "https://api.openai.com/v1"
}
```

Create this file in the same directory as the notebooks that need it.

## Repository Structure

```
week1/
  - MLS1_Shopping_Cart_Management.ipynb
  - MLS1_Shopping_Cart_Management_w_o_prompts.ipynb
  - MLS2_Password_Manager.ipynb

week2/
  - JHU_AgenticAI_MLS2_Prompt_Engineering_Fundamentals.ipynb
  - JHU_AgenticAI_MLS2_Prompt_Engineering_Fundamentals_HF.ipynb

week3/
  - Introduction_to_DSPy.ipynb
  - MLS_W3_RAG_&_dspyRAG___JHU_Agentic_AI.ipynb
```

## Updating Dependencies

To add new packages:

```bash
uv pip install package-name
```

To update requirements.txt:

```bash
uv pip freeze > requirements.txt
```

To reinstall from requirements.txt:

```bash
uv pip install -r requirements.txt
```
