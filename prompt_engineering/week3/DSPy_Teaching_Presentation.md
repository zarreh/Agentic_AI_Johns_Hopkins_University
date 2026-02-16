---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

<!--
To convert to PDF/PPTX:
- Use Marp CLI: marp DSPy_Teaching_Presentation.md --pdf
- Use VS Code with Marp extension
- Use reveal.js or any Markdown presentation tool
-->

# **Introduction to DSPy**
## Declarative Self-Improving Python

### Programming AI Systems, Not Prompts

JHU Agentic AI Course - Week 3

---

## 🎯 **Today's Learning Objectives**

By the end of this session, you will:

1. ✅ Understand **what DSPy is** and **why it matters**
2. ✅ Master **Signatures** (input/output contracts)
3. ✅ Work with **Modules** (Predict, ChainOfThought)
4. ✅ Build structured AI systems with **type safety**
5. ✅ Debug using **inspect_history()**
6. ✅ Compare DSPy to traditional prompt engineering

---

## 🤔 **The Problem: Traditional Prompt Engineering**

```python
# Fragile string manipulation
prompt = f"""
You are a support analyst. Extract these fields:
- Subject
- Priority (low/medium/high)
- Product mentioned
- Is sentiment negative?

Email: {email_text}

Output as JSON with keys: subject, priority, product, negative
"""

response = llm.invoke(prompt)
# Now parse JSON, handle errors, hope format is correct...
result = json.loads(response.content)  # 🤞 Fingers crossed!
```

---

## ❌ **What Goes Wrong?**

### **5 Critical Pain Points:**

1. **Brittle**: Change GPT-4 → Claude? Rewrite all prompts
2. **Unstructured**: Manual JSON parsing, format inconsistencies
3. **Not Reusable**: Copy-paste strings across projects
4. **Hard to Debug**: What failed? Prompt? Model? Parser?
5. **Doesn't Scale**: Each new task = start from scratch

### **Sound familiar?** 😩

---

## 💡 **The DSPy Solution**

> **DSPy is to AI programming what ORMs are to databases**

**Instead of:** Writing raw SQL strings
**You use:** Structured models (SQLAlchemy, Django ORM)

**Instead of:** Writing raw prompt strings
**You use:** Structured Signatures and Modules (DSPy)

---

## 🧠 **Mental Model: DSPy = PyTorch for Prompts**

| **PyTorch** | **DSPy** |
|-------------|----------|
| Define network architecture | Define Signatures + Modules |
| Auto-differentiation | Auto-prompt generation |
| Optimizers tune weights | Optimizers tune prompts |
| `loss.backward()` | `optimizer.compile()` |

**You focus on:** Architecture and logic
**DSPy handles:** Prompt engineering and optimization

---

## 📋 **What is DSPy?**

**DSPy (Declarative Self-improving Python)** is a framework for:

- **Programming** AI behavior as structured, reusable modules
- **Composing** complex pipelines from simple building blocks
- **Optimizing** prompts and model weights automatically
- **Evaluating** systems with metrics and data

### **Not:** A prompt library or chain framework
### **Is:** A programming paradigm for AI systems

---

## 🏗️ **DSPy Architecture: 5 Core Components**

```
┌─────────────┐
│  1. Data    │  Training/test datasets
└──────┬──────┘
       │
┌──────▼──────┐
│2. Signatures│  Input/output contracts (types)
└──────┬──────┘
       │
┌──────▼──────┐
│ 3. Modules  │  Predict, ChainOfThought, ReAct
└──────┬──────┘
       │
┌──────▼──────┐
│4. Optimizers│  BootstrapRS, MIPROv2, etc.
└──────┬──────┘
       │
┌──────▼──────┐
│5. Evaluation│  Metrics & performance testing
└─────────────┘
```

---

# **Part 1: Signatures**
## The Foundation of DSPy

---

## 🔖 **What is a Signature?**

A **Signature** declaratively specifies:
- **What inputs** the module receives
- **What outputs** it should produce
- **Types and constraints** for each field

### **Think of it as:**
- Function signature in typed languages
- API contract specification
- Schema for LLM behavior

---

## 📝 **Signature Example: Sentiment Analysis**

```python
class SentimentAnalysis(dspy.Signature):
    """Analyze the sentiment of a given sentence."""

    # Input: the text to analyze
    sentence: str = dspy.InputField()

    # Output: positive or negative sentiment
    sentiment: bool = dspy.OutputField(
        desc="True if positive, False if negative"
    )
```

**Key components:**
- `InputField()` = what LLM receives
- `OutputField()` = what LLM produces
- `desc` = guidance for the model

---

## 🎫 **Real Example: Support Ticket Extraction**

```python
from typing import Literal

class SupportEmail(dspy.Signature):
    # Input: raw email text
    email: str = dspy.InputField()

    # Outputs: structured fields
    subject: str = dspy.OutputField(
        desc="Subject line of the email"
    )

    priority: Literal["low", "medium", "high"] = dspy.OutputField()

    product: str = dspy.OutputField(
        desc="Product mentioned, or empty string if unknown"
    )

    negative_sentiment: bool = dspy.OutputField(desc="True/False")
```

---

## 🎨 **Supported Data Types**

### **Basic Types:**
- `str`, `int`, `float`, `bool`

### **Complex Types:**
- `list[str]`, `dict[str, int]`
- `Optional[float]`
- `Literal["option1", "option2", "option3"]`

### **DSPy Types:**
- `dspy.Image`, `dspy.History`

### **Custom Types:**
- Any `pydantic.BaseModel` subclass

---

## ✅ **Why Signatures Matter**

### **Traditional Approach:**
```python
"Extract subject, priority, product, and sentiment from email..."
# Vague, unstructured, no validation
```

### **DSPy Approach:**
```python
class SupportEmail(dspy.Signature):
    email: str = dspy.InputField()
    subject: str = dspy.OutputField()
    priority: Literal["low", "medium", "high"] = dspy.OutputField()
```

**Benefits:**
✅ Self-documenting
✅ Type-safe
✅ Auto-validated
✅ IDE autocomplete

---

# **Part 2: Modules**
## Building Blocks of AI Behavior

---

## 🧩 **What are Modules?**

**Modules** implement LLM behavior using Signatures:

| Module | Purpose |
|--------|---------|
| `dspy.Predict` | Basic prediction (most common) |
| `dspy.ChainOfThought` | Step-by-step reasoning |
| `dspy.ProgramOfThought` | Generates code to solve tasks |
| `dspy.ReAct` | Uses tools/actions to fulfill task |
| `dspy.MultiChainComparison` | Compares multiple outputs |

**Think:** Building blocks like LEGO pieces that snap together

---

## 🔮 **Module 1: dspy.Predict**

**The simplest module** - just makes a prediction

```python
# Define signature
class SupportEmail(dspy.Signature):
    email: str = dspy.InputField()
    subject: str = dspy.OutputField()
    priority: Literal["low", "medium", "high"] = dspy.OutputField()

# Create predictor from signature
extract_ticket = dspy.Predict(SupportEmail)

# Use it!
result = extract_ticket(email="Customer complaint about defective product...")

print(result.subject)    # Auto-extracted!
print(result.priority)   # Validated to be low/medium/high
```

---

## 🧠 **Module 2: dspy.ChainOfThought**

**Adds reasoning transparency** - shows LLM's thinking

```python
class LoanRisk(dspy.Signature):
    applicant_profile: str = dspy.InputField()
    loan_risk: Literal["low", "medium", "high"] = dspy.OutputField()
    approved: bool = dspy.OutputField()

# Use ChainOfThought instead of Predict
risk_checker = dspy.ChainOfThought(LoanRisk)

result = risk_checker(applicant_profile="Credit score: 680, Income: $92k...")

print(result.reasoning)   # 🎯 SEE THE LLM'S LOGIC!
print(result.loan_risk)   # "medium"
print(result.approved)    # False
```

**Magic:** `reasoning` field appears automatically!

---

## 🔍 **ChainOfThought: What Happens?**

DSPy automatically:

1. Adds a `reasoning` output field to your signature
2. Prompts the LLM to "think step by step"
3. Returns the reasoning along with your requested outputs

**You get:**
- Transparency into LLM decision-making
- Better quality outputs (reasoning improves accuracy)
- Debuggability (see where logic went wrong)

---

## 🎯 **Hands-On: Support Email Demo**

```python
# Sample email
email = """
Subject: Missing accessories in package

Hi support,
I just received my order #12345 but the charging cable
for my SmartWatch Pro is missing. This is very frustrating!
Please send the missing item ASAP.
"""

# Extract structured data
result = extract_ticket(email=email)

print(f"Subject: {result.subject}")
print(f"Priority: {result.priority}")
print(f"Product: {result.product}")
print(f"Negative Sentiment: {result.negative_sentiment}")
```

---

## 📊 **Expected Output**

```
Subject: Missing accessories in package
Priority: high
Product: SmartWatch Pro
Negative Sentiment: True
```

### **No JSON parsing! No error handling! Just works!** ✨

---

## 🔬 **Debugging with inspect_history()**

**The secret weapon** for understanding what DSPy does:

```python
# After running predictions
dspy.inspect_history()
```

**Shows you:**
1. The actual prompt DSPy generated
2. The LLM's raw response
3. How DSPy parsed the response

**This is your "aha!" moment:** See how DSPy turns signatures into prompts!

---

## 📸 **inspect_history() Output Example**

```
================================
Prompt:
================================
You are a helpful assistant.

Extract the following from the email:
- subject: Subject line of the email
- priority: One of: low, medium, high
- product: Product mentioned, or empty string if unknown
- negative_sentiment: True/False

Email: [customer email here]

================================
Response:
================================
subject: Missing accessories in package
priority: high
product: SmartWatch Pro
negative_sentiment: True
```

---

# **Part 3: Inline Signatures**
## Quick Prototyping

---

## ⚡ **Inline Signatures**

For simple tasks, skip the class definition:

```python
class SimpleQA(dspy.Module):
    def __init__(self):
        # Inline signature: "input1, input2 -> output"
        self.predictor = dspy.Predict("question -> response")

    def forward(self, question):
        result = self.predictor(question=question)
        return result.response

# Use it
qa = SimpleQA()
answer = qa("What is DSPy?")
```

**Good for:** Rapid prototyping, simple tasks
**Use class signatures for:** Production code, complex types

---

# **Part 4: Real-World Example**
## Financial Risk Assessment

---

## 🏦 **Use Case: Loan Approval**

**Business need:** Assess loan applications automatically

**Traditional approach:**
```python
prompt = f"""
Analyze this loan application and determine:
1. Risk level (low/medium/high)
2. Should we approve?

Profile: {profile}
"""
# Parse response, hope for consistent format...
```

**Problems:** Inconsistent outputs, no reasoning, hard to audit

---

## 💼 **DSPy Solution: Structured Assessment**

```python
class LoanRisk(dspy.Signature):
    """Assess loan application risk."""

    applicant_profile: str = dspy.InputField()

    loan_risk: Literal["low", "medium", "high"] = dspy.OutputField()

    approved: bool = dspy.OutputField(
        desc="Should we approve this loan?"
    )

# Use ChainOfThought for transparency
risk_checker = dspy.ChainOfThought(LoanRisk)
```

---

## 📋 **Sample Application**

```python
profile = """
Name: Mark Rivera
Credit score: 680
Annual income: $92,000
Existing debt: $40,000
Requested loan: $25,000
Employment: 3 years at current job
"""

result = risk_checker(applicant_profile=profile)

print(f"Risk Level: {result.loan_risk}")
print(f"Approved: {result.approved}")
print(f"\nReasoning:\n{result.reasoning}")
```

---

## 📊 **Sample Output**

```
Risk Level: medium
Approved: False

Reasoning:
The applicant has a moderate credit score of 680, which is
acceptable but not excellent. With $40k existing debt and
$92k income, their debt-to-income ratio is concerning.
Adding a $25k loan would increase this ratio significantly.
While employment stability is positive (3 years), the overall
financial picture presents medium risk. Recommend requesting
a co-signer or smaller loan amount.
```

**Auditable, explainable, structured!** ✅

---

# **Part 5: DSPy vs Alternatives**
## Why Choose DSPy?

---

## 🥊 **DSPy vs LangChain**

| Feature | LangChain | DSPy |
|---------|-----------|------|
| **Paradigm** | Chains & templates | Signatures & modules |
| **Prompts** | Manual strings | Auto-generated |
| **Outputs** | Unstructured | Typed & validated |
| **Optimization** | Manual tuning | Built-in optimizers |
| **Debugging** | Print statements | `inspect_history()` |
| **Best for** | Quick prototypes | Production systems |

**Summary:** LangChain = glue code. DSPy = optimization framework.

---

## 🥊 **DSPy vs Instructor/Pydantic AI**

| Feature | Instructor | DSPy |
|---------|------------|------|
| **Focus** | Structured outputs | Full pipelines |
| **Optimization** | None | Built-in |
| **Modules** | No | Yes (composable) |
| **Reasoning** | Manual | `ChainOfThought` |
| **Evaluation** | External | Integrated |

**Summary:** Instructor = structured parsing. DSPy = complete framework.

---

## 🥊 **DSPy vs Raw Prompting**

| Feature | Raw Prompts | DSPy |
|---------|-------------|------|
| **Maintenance** | Rewrite per model | Signatures portable |
| **Reusability** | Copy-paste | Import modules |
| **Type Safety** | None | Full validation |
| **Testing** | Manual | Systematic |
| **Optimization** | Trial & error | Automated |
| **Collaboration** | Share docs | Share code |

**Summary:** Raw prompting = assembly code. DSPy = high-level language.

---

# **Part 6: Key Advantages**
## Why DSPy Matters

---

## 🎯 **Advantage 1: Separation of Concerns**

```
┌─────────────┐
│  Signature  │  WHAT to do (business logic)
└──────┬──────┘
       │
┌──────▼──────┐
│   Module    │  HOW to do it (implementation)
└──────┬──────┘
       │
┌──────▼──────┐
│  Optimizer  │  Make it BETTER (auto-improvement)
└─────────────┘
```

**Like MVC architecture for AI systems**

---

## 🛡️ **Advantage 2: Type Safety**

```python
# Traditional: anything goes 🤷
response = llm.invoke("Extract priority...")
priority = response.content  # Could be anything!

# DSPy: validated at runtime ✅
class Ticket(dspy.Signature):
    email: str = dspy.InputField()
    priority: Literal["low", "medium", "high"] = dspy.OutputField()

result = extract(email="...")
# result.priority is GUARANTEED to be low/medium/high
```

**No more:** "LLM returned 'urgent' but we only handle low/medium/high!"

---

## 🔧 **Advantage 3: Composability**

```python
# Build complex systems from simple parts
class RAGSystem(dspy.Module):
    def __init__(self):
        self.retriever = dspy.Retrieve(...)
        self.generator = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        context = self.retriever(question)
        answer = self.generator(context=context, question=question)
        return answer

# Modules snap together like LEGO!
```

---

## 🚀 **Advantage 4: Optimization Ready**

```python
# DSPy can automatically improve your system
from dspy.teleprompt import BootstrapFewShot

# Define metric
def accuracy_metric(example, prediction):
    return example.answer == prediction.answer

# Auto-optimize!
optimizer = BootstrapFewShot(metric=accuracy_metric)
optimized_system = optimizer.compile(
    student=my_system,
    trainset=training_data
)

# optimized_system now has better prompts!
```

**You don't tune prompts. DSPy does it for you.** 🤖

---

## 🐛 **Advantage 5: Debugging & Transparency**

```python
# See EXACTLY what happened
dspy.inspect_history()

# For ChainOfThought modules
print(result.reasoning)  # See the thinking process

# For any module
print(result)  # Pretty-printed structured output
```

**No more black boxes!**

---

## 🌍 **Advantage 6: Model Portability**

```python
# Works with any LLM
lm = dspy.LM(model='openai/gpt-4o-mini')      # OpenAI
lm = dspy.LM(model='anthropic/claude-3-5')   # Anthropic
lm = dspy.LM(model='ollama/llama3.2')        # Local

dspy.configure(lm=lm)

# Same code works with ALL models!
# DSPy adapts prompts automatically
```

**Future-proof your AI systems**

---

# **Part 7: Practical Workflow**
## How to Build with DSPy

---

## 📝 **Step-by-Step Workflow**

### **1. Define the Task**
What inputs? What outputs? What types?

### **2. Create Signature**
```python
class MyTask(dspy.Signature):
    input_field: str = dspy.InputField()
    output_field: bool = dspy.OutputField()
```

### **3. Choose Module**
`Predict`? `ChainOfThought`? Custom?

### **4. Test & Inspect**
Run examples, use `inspect_history()`

### **5. Optimize** (advanced)
Use optimizers to improve performance

---

## 🎓 **Example: Sentiment Analysis**

```python
# 1. Define task
class SentimentTask(dspy.Signature):
    """Determine if a review is positive or negative."""
    review: str = dspy.InputField()
    is_positive: bool = dspy.OutputField()

# 2. Create predictor
classifier = dspy.Predict(SentimentTask)

# 3. Test
result = classifier(review="This product is amazing!")
print(result.is_positive)  # True

# 4. Inspect
dspy.inspect_history()

# 5. Use in production
def classify_reviews(reviews):
    return [classifier(review=r).is_positive for r in reviews]
```

---

# **Part 8: Common Patterns**
## Best Practices

---

## ✅ **Best Practice 1: Descriptive Field Names**

```python
# ❌ Bad: vague names
class Task(dspy.Signature):
    input: str = dspy.InputField()
    output: str = dspy.OutputField()

# ✅ Good: descriptive names
class SummarizeArticle(dspy.Signature):
    article_text: str = dspy.InputField()
    concise_summary: str = dspy.OutputField()
```

**Field names guide the LLM!** Choose wisely.

---

## ✅ **Best Practice 2: Use Descriptions**

```python
# ❌ Minimal
priority: str = dspy.OutputField()

# ✅ Guided
priority: Literal["low", "medium", "high"] = dspy.OutputField(
    desc="Urgency level: low=can wait, medium=this week, high=urgent"
)
```

**The `desc` parameter is your guidance to the LLM**

---

## ✅ **Best Practice 3: Type Constraints**

```python
# ❌ Too loose
sentiment: str = dspy.OutputField()  # Could be anything!

# ✅ Constrained
sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField()

# ✅ Even better
sentiment: bool = dspy.OutputField(desc="True if positive")
```

**Narrow types = more reliable outputs**

---

## ✅ **Best Practice 4: Modular Design**

```python
# Break complex tasks into modules
class ExtractEntities(dspy.Signature):
    text: str = dspy.InputField()
    entities: list[str] = dspy.OutputField()

class ClassifyIntent(dspy.Signature):
    text: str = dspy.InputField()
    intent: Literal["question", "complaint", "feedback"] = dspy.OutputField()

# Compose them
class ProcessMessage(dspy.Module):
    def __init__(self):
        self.extract = dspy.Predict(ExtractEntities)
        self.classify = dspy.Predict(ClassifyIntent)

    def forward(self, message):
        entities = self.extract(text=message).entities
        intent = self.classify(text=message).intent
        return {"entities": entities, "intent": intent}
```

---

# **Part 9: Advanced Topics**
## Beyond the Basics

---

## 🔬 **Advanced: Custom Modules**

```python
class CustomRAG(dspy.Module):
    def __init__(self, retriever):
        self.retriever = retriever
        self.generator = dspy.ChainOfThought("context, question -> answer")

    def forward(self, question):
        # Custom retrieval logic
        docs = self.retriever.get_relevant_documents(question)
        context = "\n".join([d.page_content for d in docs])

        # Generate with context
        result = self.generator(context=context, question=question)

        return dspy.Prediction(
            answer=result.answer,
            reasoning=result.reasoning,
            sources=docs
        )
```

---

## 📊 **Advanced: Evaluation**

```python
# Define what "good" means
def answer_correctness(example, prediction):
    return example.answer.lower() == prediction.answer.lower()

# Evaluate on test set
from dspy.evaluate import Evaluate

evaluator = Evaluate(
    devset=test_dataset,
    metric=answer_correctness,
    num_threads=4
)

score = evaluator(my_module)
print(f"Accuracy: {score}")
```

---

## 🎯 **Advanced: Optimization**

```python
from dspy.teleprompt import BootstrapFewShot

# Automatically find best prompts
optimizer = BootstrapFewShot(
    metric=answer_correctness,
    max_bootstrapped_demos=4,
    max_labeled_demos=8
)

# Compile optimized version
optimized_module = optimizer.compile(
    student=my_module,
    trainset=training_data
)

# optimized_module now has better prompts!
```

**This is DSPy's superpower: auto-optimization**

---

# **Part 10: Hands-On Exercise**
## Build Your First DSPy System

---

## 🛠️ **Exercise: Email Classifier**

**Goal:** Build a system that categorizes customer emails

**Requirements:**
1. Input: email text
2. Outputs:
   - Category: "billing", "technical", "general"
   - Urgency: 1-5 scale
   - Needs human review: yes/no

**Time:** 15 minutes

---

## 🎯 **Exercise Solution Template**

```python
from typing import Literal

# TODO: Define signature
class EmailClassifier(dspy.Signature):
    # Your code here
    pass

# TODO: Create predictor
classifier = dspy.Predict(EmailClassifier)

# TODO: Test with sample email
sample_email = """
I've been trying to access my account for 2 hours but
keep getting error 503. This is blocking my work!
"""

result = classifier(email=sample_email)

# TODO: Print results and inspect
print(result)
dspy.inspect_history()
```

---

## ✅ **Exercise Solution**

```python
class EmailClassifier(dspy.Signature):
    """Classify customer support emails."""

    email: str = dspy.InputField()

    category: Literal["billing", "technical", "general"] = dspy.OutputField()

    urgency: int = dspy.OutputField(
        desc="Urgency level from 1 (low) to 5 (critical)"
    )

    needs_human_review: bool = dspy.OutputField(
        desc="True if complex and needs human attention"
    )

classifier = dspy.ChainOfThought(EmailClassifier)  # Use CoT for reasoning!
```

---

# **Part 11: Key Takeaways**
## What You've Learned

---

## 🎓 **Key Takeaways**

### **1. Signatures Define Contracts**
Input/output types with descriptions guide LLM behavior

### **2. Modules Implement Behavior**
`Predict`, `ChainOfThought`, etc. use signatures to perform tasks

### **3. Type Safety Prevents Errors**
`Literal[]`, `bool`, structured types = validated outputs

### **4. Inspect for Understanding**
`inspect_history()` reveals what DSPy is doing

### **5. Composability Enables Scale**
Build complex systems from simple modules

---

## 💡 **The Paradigm Shift**

### **Old Way:**
"Let me spend 2 hours crafting the perfect prompt..."

### **New Way:**
"Let me define what I want (signature), then let DSPy figure out how to get it"

### **The Power:**
**You become an AI system architect, not a prompt engineer**

---

## 🚀 **Next Steps**

### **Immediate:**
1. ✅ Complete the hands-on exercises in the notebook
2. ✅ Experiment with different modules (Predict vs ChainOfThought)
3. ✅ Use `inspect_history()` liberally to understand behavior

### **Soon:**
1. Build a multi-module pipeline (e.g., RAG system)
2. Learn about optimizers (BootstrapFewShot, MIPROv2)
3. Create evaluation metrics for your use case

### **Advanced:**
1. Contribute to DSPy community
2. Build custom modules for your domain
3. Optimize production systems with DSPy

---

## 📚 **Resources**

### **Official:**
- **Website:** https://dspy.ai/
- **GitHub:** https://github.com/stanfordnlp/dspy
- **Docs:** https://dspy-docs.vercel.app/

### **Community:**
- Discord: Active community for questions
- Examples: Check the `/examples` folder in repo
- Paper: "DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines"

### **Your Notebook:**
`Introduction_to_DSPy.ipynb` - Work through all examples!

---

## ❓ **Common Questions**

**Q: Do I need to learn prompt engineering first?**
A: No! That's the point. DSPy abstracts it away.

**Q: Can I use my existing prompts with DSPy?**
A: You can, but you'll get more value from signatures.

**Q: What if my LLM doesn't follow the signature?**
A: Use optimizers to improve adherence, or add more guidance in `desc`.

**Q: Is DSPy production-ready?**
A: Yes! Used by Stanford, companies, and researchers.

**Q: How does it compare to AutoGPT/LangGraph?**
A: Different focus. DSPy = optimization framework. Those = agent frameworks.

---

## 🎯 **Final Thought**

> **"DSPy doesn't replace your AI skills—it amplifies them."**

You still need to:
- Understand your problem
- Design good architectures
- Choose appropriate modules
- Evaluate results

**DSPy handles:**
- Prompt engineering
- Output parsing
- Type validation
- Optimization

**Focus on what matters: solving problems, not crafting prompts.**

---

## 🙏 **Thank You!**

### **Let's Build Better AI Systems Together**

**Questions?**

**Now:** Open `Introduction_to_DSPy.ipynb` and let's code!

---

<!-- End of Presentation -->

## 📎 **Appendix: Quick Reference**

### **Common Signatures**
```python
# Classification
class Classify(dspy.Signature):
    text: str = dspy.InputField()
    label: Literal["A", "B", "C"] = dspy.OutputField()

# Q&A
class QA(dspy.Signature):
    context: str = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

# Summarization
class Summarize(dspy.Signature):
    document: str = dspy.InputField()
    summary: str = dspy.OutputField(desc="Concise summary in 2-3 sentences")
```

---

## 📎 **Appendix: Common Modules**

```python
# Basic prediction
predictor = dspy.Predict(MySignature)

# With reasoning
reasoner = dspy.ChainOfThought(MySignature)

# With multiple attempts
multitry = dspy.MultiChainComparison(MySignature)

# With tool use
agent = dspy.ReAct(MySignature)
```

---

## 📎 **Appendix: Setup Code**

```python
import dspy
import os
import json

# Load API key
with open('config.json') as f:
    config = json.load(f)
    os.environ['OPENAI_API_KEY'] = config['API_KEY']

# Configure LLM
lm = dspy.LM(
    model='openai/gpt-4o-mini',
    temperature=0,
    api_key=os.environ['OPENAI_API_KEY']
)

dspy.configure(lm=lm)

# Now you're ready to use DSPy!
```
