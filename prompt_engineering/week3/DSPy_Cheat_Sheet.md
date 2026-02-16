# DSPy Quick Reference Guide

**Version:** Week 3 - JHU Agentic AI Course
**Purpose:** Handy reference for DSPy concepts and code patterns

---

## 🚀 **Setup (Copy-Paste Ready)**

```python
import dspy
import os
import json
from typing import Literal, Optional

# Load API key from config.json
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
```

---

## 📋 **Signature Patterns**

### **Basic Signature**
```python
class TaskName(dspy.Signature):
    """Describe what this task does."""

    # Inputs
    input_field: str = dspy.InputField()

    # Outputs
    output_field: str = dspy.OutputField()
```

### **With Descriptions**
```python
class EmailClassifier(dspy.Signature):
    email: str = dspy.InputField()
    category: str = dspy.OutputField(
        desc="One of: billing, technical, general"
    )
```

### **With Type Constraints**
```python
class SentimentAnalysis(dspy.Signature):
    text: str = dspy.InputField()
    sentiment: Literal["positive", "negative", "neutral"] = dspy.OutputField()
    confidence: float = dspy.OutputField(desc="0.0 to 1.0")
```

### **Multiple Inputs/Outputs**
```python
class SupportTicket(dspy.Signature):
    # Multiple inputs
    email: str = dspy.InputField()
    customer_tier: str = dspy.InputField()

    # Multiple outputs
    priority: Literal["low", "medium", "high"] = dspy.OutputField()
    category: str = dspy.OutputField()
    needs_escalation: bool = dspy.OutputField()
```

---

## 🧩 **Module Patterns**

### **Using dspy.Predict**
```python
# Create predictor from signature
predictor = dspy.Predict(MySignature)

# Use it
result = predictor(input_field="some value")
print(result.output_field)
```

### **Using dspy.ChainOfThought**
```python
# Adds automatic reasoning
reasoner = dspy.ChainOfThought(MySignature)

result = reasoner(input_field="some value")
print(result.reasoning)      # See the thinking!
print(result.output_field)   # Get the result
```

### **Inline Signature (Quick Prototyping)**
```python
# No class needed
predictor = dspy.Predict("question -> answer")
result = predictor(question="What is DSPy?")
print(result.answer)
```

---

## 🏗️ **Custom Module Pattern**

```python
class MyCustomModule(dspy.Module):
    def __init__(self):
        # Initialize any predictors/components
        self.step1 = dspy.Predict(Signature1)
        self.step2 = dspy.ChainOfThought(Signature2)

    def forward(self, input_param):
        # Implement logic
        intermediate = self.step1(field=input_param)
        final = self.step2(field=intermediate.output)
        return final

# Use it
my_module = MyCustomModule()
result = my_module(input_param="value")
```

---

## 🔍 **Debugging Tools**

### **Inspect History**
```python
# After running predictions
dspy.inspect_history()

# Shows:
# - Generated prompts
# - LLM responses
# - Parsing details
```

### **Print Prediction**
```python
result = predictor(input="...")
print(result)  # Pretty-printed structured output
```

### **Access Individual Fields**
```python
print(result.field_name)       # Access specific field
print(result.reasoning)        # For ChainOfThought modules
print(dir(result))             # See all available fields
```

---

## 📊 **Common Data Types**

| Type | Usage | Example |
|------|-------|---------|
| `str` | Text | `name: str` |
| `int` | Integers | `count: int` |
| `float` | Decimals | `score: float` |
| `bool` | True/False | `is_valid: bool` |
| `Literal[...]` | Specific options | `Literal["A", "B", "C"]` |
| `list[str]` | List of strings | `tags: list[str]` |
| `Optional[...]` | May be None | `Optional[str]` |

---

## ✅ **Best Practices Checklist**

- [ ] Use descriptive field names (not just "input"/"output")
- [ ] Add `desc` parameter to guide the LLM
- [ ] Use type constraints (`Literal`, `bool`) for predictable outputs
- [ ] Test with `inspect_history()` to see generated prompts
- [ ] Use `ChainOfThought` for complex reasoning tasks
- [ ] Use `Predict` for simple, fast tasks
- [ ] Create custom modules for reusable pipelines
- [ ] Add docstrings to your signatures

---

## 🎯 **Common Use Cases**

### **1. Classification**
```python
class Classifier(dspy.Signature):
    text: str = dspy.InputField()
    category: Literal["cat1", "cat2", "cat3"] = dspy.OutputField()

classifier = dspy.Predict(Classifier)
result = classifier(text="...")
```

### **2. Extraction**
```python
class Extractor(dspy.Signature):
    document: str = dspy.InputField()
    entities: list[str] = dspy.OutputField(desc="Named entities found")
    dates: list[str] = dspy.OutputField()

extractor = dspy.Predict(Extractor)
result = extractor(document="...")
```

### **3. Question Answering**
```python
class QA(dspy.Signature):
    context: str = dspy.InputField()
    question: str = dspy.InputField()
    answer: str = dspy.OutputField(desc="Based only on context")

qa = dspy.ChainOfThought(QA)  # Use CoT for better answers
result = qa(context="...", question="...")
```

### **4. Summarization**
```python
class Summarize(dspy.Signature):
    document: str = dspy.InputField()
    summary: str = dspy.OutputField(desc="2-3 sentence summary")

summarizer = dspy.Predict(Summarize)
result = summarizer(document="...")
```

### **5. Structured Data Extraction**
```python
class ExtractInfo(dspy.Signature):
    text: str = dspy.InputField()
    name: str = dspy.OutputField()
    age: int = dspy.OutputField()
    city: str = dspy.OutputField()

extractor = dspy.Predict(ExtractInfo)
result = extractor(text="John is 25 and lives in NYC")
```

---

## 🔄 **Workflow**

```
1. Define what you want
   ↓
2. Create Signature (input/output types)
   ↓
3. Choose Module (Predict, ChainOfThought, etc.)
   ↓
4. Test with examples
   ↓
5. Inspect with dspy.inspect_history()
   ↓
6. Refine signature/descriptions
   ↓
7. Use in production
```

---

## 🆚 **Quick Comparison**

### **Traditional vs DSPy**

| Task | Traditional | DSPy |
|------|-------------|------|
| **Prompting** | Manual strings | Auto-generated from signatures |
| **Parsing** | JSON/regex | Automatic type validation |
| **Changes** | Rewrite prompts | Modify signature |
| **Debugging** | Print/logs | `inspect_history()` |
| **Reuse** | Copy-paste | Import modules |

---

## 🎓 **Module Comparison**

| Module | When to Use | Output |
|--------|-------------|--------|
| `Predict` | Simple, fast predictions | Just outputs |
| `ChainOfThought` | Need reasoning/explanation | Outputs + reasoning |
| `ProgramOfThought` | Generate code to solve | Outputs + code |
| `ReAct` | Use external tools | Outputs + actions |
| `MultiChainComparison` | Compare multiple solutions | Best output |

---

## 🐛 **Troubleshooting**

### **Problem: LLM not following signature**
```python
# Add more specific descriptions
field: str = dspy.OutputField(
    desc="Must be exactly one of: option1, option2, option3"
)

# Or use Literal type
field: Literal["option1", "option2", "option3"] = dspy.OutputField()
```

### **Problem: Need to see what's happening**
```python
# Always use inspect_history() first!
dspy.inspect_history()
```

### **Problem: Inconsistent outputs**
```python
# Use ChainOfThought for more reliable reasoning
predictor = dspy.ChainOfThought(MySignature)
```

### **Problem: Want to customize prompt**
```python
# Use optimizers (advanced) or add class docstring
class MySignature(dspy.Signature):
    """This detailed docstring guides the LLM's behavior."""
    ...
```

---

## 💡 **Pro Tips**

1. **Start simple**: Use `dspy.Predict` with inline signatures first
2. **Add complexity gradually**: Move to class signatures, then custom modules
3. **Use ChainOfThought liberally**: The reasoning helps a lot
4. **Inspect everything**: `dspy.inspect_history()` is your friend
5. **Type constraints are powerful**: `Literal[]` prevents many errors
6. **Descriptive names matter**: Field names guide the LLM
7. **Test incrementally**: Don't build everything then test
8. **Read the generated prompts**: They're educational!

---

## 📞 **Common Errors & Solutions**

### **Error: "Field X not found"**
```python
# Check field name spelling in signature and usage
result = predictor(input_field="...")  # Must match signature!
```

### **Error: Type validation failed**
```python
# LLM returned wrong type
# Solution: Add clearer description or use Literal
priority: Literal["low", "medium", "high"] = dspy.OutputField(
    desc="Must be exactly: low, medium, or high"
)
```

### **Error: Module not found**
```python
# Forgot to inherit from dspy.Module
class MyModule(dspy.Module):  # Don't forget this!
    ...
```

---

## 🔗 **Useful Links**

- **DSPy Website:** https://dspy.ai/
- **GitHub Repo:** https://github.com/stanfordnlp/dspy
- **Documentation:** https://dspy-docs.vercel.app/
- **Discord:** Ask questions in the community
- **Examples:** Check `/examples` in the repo

---

## 📝 **Template: Complete Working Example**

```python
import dspy
import os
import json
from typing import Literal

# === SETUP ===
with open('config.json') as f:
    config = json.load(f)
    os.environ['OPENAI_API_KEY'] = config['API_KEY']

lm = dspy.LM(model='openai/gpt-4o-mini', temperature=0)
dspy.configure(lm=lm)

# === DEFINE SIGNATURE ===
class EmailClassifier(dspy.Signature):
    """Classify customer support emails."""

    email: str = dspy.InputField()
    category: Literal["billing", "technical", "general"] = dspy.OutputField()
    priority: Literal["low", "medium", "high"] = dspy.OutputField()

# === CREATE PREDICTOR ===
classifier = dspy.ChainOfThought(EmailClassifier)

# === TEST ===
test_email = """
I can't login to my account and I'm getting error 503.
This is urgent as I need to submit my work today!
"""

result = classifier(email=test_email)

# === VIEW RESULTS ===
print(f"Category: {result.category}")
print(f"Priority: {result.priority}")
print(f"Reasoning: {result.reasoning}")

# === DEBUG ===
dspy.inspect_history()
```

---

**Keep this guide handy during development!** 🚀
