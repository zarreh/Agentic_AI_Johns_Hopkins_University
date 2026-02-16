# DSPy Teaching Materials Guide

This folder contains comprehensive teaching materials for Week 3 of the JHU Agentic AI course, focused on **DSPy (Declarative Self-improving Python)**.

---

## 📁 **Files in This Folder**

### **1. Notebooks (Hands-On Learning)**
- `Introduction_to_DSPy.ipynb` - Interactive notebook with exercises
- `MLS_W3_RAG_&_dspyRAG___JHU_Agentic_AI.ipynb` - RAG implementation comparison

### **2. Teaching Materials (Instructor Resources)**
- `DSPy_Teaching_Presentation.md` - Complete slide deck (this document)
- `DSPy_Cheat_Sheet.md` - Student reference guide
- `TEACHING_GUIDE.md` - This file (instructor guide)

### **3. Data**
- `HBR_How_Apple_Is_Organized_For_Innovation.pdf` - Sample document for RAG exercises

---

## 🎓 **How to Use These Materials**

### **Option 1: Full Lecture (90-120 minutes)**

**Structure:**
1. **Presentation** (45-60 min): Use `DSPy_Teaching_Presentation.md`
2. **Break** (10 min)
3. **Hands-On Lab** (40-50 min): Work through `Introduction_to_DSPy.ipynb`
4. **Q&A** (10 min)

**Distribution:**
- Share `DSPy_Cheat_Sheet.md` at the start for reference
- Have students open `Introduction_to_DSPy.ipynb` during hands-on portion

---

### **Option 2: Flipped Classroom (Async + Sync)**

**Before Class (Async):**
- Students read `DSPy_Cheat_Sheet.md`
- Students watch a pre-recorded walkthrough of the presentation
- Students attempt `Introduction_to_DSPy.ipynb` exercises

**During Class (60 min):**
1. **Quick Recap** (10 min): Key concepts from presentation
2. **Live Coding** (20 min): Build a DSPy system together
3. **Group Exercise** (20 min): Teams solve a problem using DSPy
4. **Discussion** (10 min): Share solutions and learnings

---

### **Option 3: Workshop Format (2-3 hours)**

**Part 1: Introduction (30 min)**
- Present slides 1-40 from presentation
- Focus on "Why DSPy?" and core concepts

**Part 2: Basic Concepts (45 min)**
- Signatures and Modules (slides 41-80)
- Students follow along in notebook
- Complete Exercise 1: Support Email Classification

**Break (15 min)**

**Part 3: Advanced Patterns (45 min)**
- ChainOfThought, Custom Modules (slides 81-110)
- Students work on Exercise 2: Financial Risk Assessment
- Introduction to RAG with DSPy

**Part 4: Capstone Project (45 min)**
- Students build their own DSPy system
- Suggested projects:
  - Resume screener
  - Product review analyzer
  - Document Q&A system
  - News article classifier

---

## 🎯 **Converting the Presentation**

### **To PDF (for distribution):**
```bash
# Using Marp CLI (recommended)
marp DSPy_Teaching_Presentation.md --pdf

# Or use VS Code with Marp extension
# File > Export Slide Deck > PDF
```

### **To PowerPoint:**
```bash
# Using Marp CLI
marp DSPy_Teaching_Presentation.md --pptx

# Or convert via Pandoc
pandoc DSPy_Teaching_Presentation.md -o DSPy_Presentation.pptx
```

### **To HTML (interactive web presentation):**
```bash
# Using Marp
marp DSPy_Teaching_Presentation.md --html

# Or use reveal.js
# Just open in a Markdown presentation tool
```

### **To Google Slides:**
1. Convert to PPTX first (see above)
2. Upload to Google Drive
3. Open with Google Slides

---

## 🎬 **Presentation Tips**

### **Opening Hook (Slides 1-10)**
- **Start with pain**: Show the messy traditional prompt engineering code
- **Ask the audience**: "Who has struggled with LLM outputs not matching expectations?"
- **Set expectations**: By end of session, they'll build structured AI systems

### **Core Teaching (Slides 11-100)**
- **Live demo**: Don't just show slides—run code!
- **Use `inspect_history()`**: This is the "aha!" moment for students
- **Pause for questions**: After each major section
- **Show failures**: Deliberately make mistakes to demonstrate debugging

### **Hands-On Practice (Slides 101-120)**
- **Provide starter code**: Don't make them type everything
- **Pair programming**: Have students work in pairs
- **Walk around**: Help struggling students individually
- **Share solutions**: Have students present their approaches

### **Closing (Slides 121-130)**
- **Recap key points**: Signatures, Modules, Type Safety
- **Connect to next session**: Preview optimizers and advanced topics
- **Resource sharing**: Point to docs, Discord, GitHub

---

## 🎨 **Customization Guide**

### **Adding Your Own Examples**
The presentation is in Markdown, so it's easy to add slides:

```markdown
---

## Your New Slide Title

Your content here...

- Bullet points
- Code examples

```python
# Code blocks
```

---
```

### **Adjusting for Time Constraints**

**60-minute version**: Skip slides 100-120 (advanced topics)
**45-minute version**: Skip slides 80-120 (focus on basics only)
**30-minute version**: Use slides 1-60 (overview and demo only)

### **Adding Interactive Elements**

```markdown
---

## 🎮 **Quick Poll**

**Raise your hand if you've:**
1. Spent >1 hour crafting a prompt
2. Had an LLM return invalid JSON
3. Wished there was a better way

---
```

### **Adding Your Branding**
Edit the YAML frontmatter:

```yaml
---
marp: true
theme: your-custom-theme
backgroundColor: #your-color
backgroundImage: url('your-logo.svg')
---
```

---

## 📊 **Assessing Student Understanding**

### **Quick Check Questions (Throughout)**

**After Signatures:**
- "What's the difference between InputField and OutputField?"
- "Why use Literal instead of str?"

**After Modules:**
- "When would you use ChainOfThought vs Predict?"
- "What does inspect_history() show us?"

**After Hands-On:**
- "How is DSPy different from traditional prompting?"
- "What problem does DSPy solve for production systems?"

### **Exit Ticket (End of Session)**
```
1. Define a Signature in your own words
2. Name one advantage of DSPy over raw prompting
3. Write a one-sentence summary of what you learned today
```

---

## 🎯 **Learning Outcomes Assessment**

By the end, students should be able to:

- [ ] **Define** what DSPy is and its purpose
- [ ] **Create** a Signature with proper input/output fields
- [ ] **Use** dspy.Predict and dspy.ChainOfThought modules
- [ ] **Debug** using inspect_history()
- [ ] **Explain** advantages over traditional prompt engineering
- [ ] **Build** a simple structured AI system independently

---

## 💡 **Common Student Questions & Answers**

### **Q: "Do I need to know prompt engineering first?"**
**A:** No! That's the beauty of DSPy—it abstracts prompt engineering away. Focus on defining what you want (signatures), not how to ask for it.

### **Q: "Can I mix DSPy with LangChain?"**
**A:** Yes! You can use LangChain for data loading/retrieval and DSPy for the LLM interactions. See the RAG notebook for examples.

### **Q: "What if the LLM doesn't follow my signature?"**
**A:**
1. Add more specific `desc` parameters
2. Use type constraints (Literal, bool)
3. Use ChainOfThought for better reasoning
4. Try optimizers (advanced topic)

### **Q: "Is this only for OpenAI models?"**
**A:** No! DSPy works with any LLM: OpenAI, Anthropic, local models (Ollama), HuggingFace, etc. Just change the model parameter.

### **Q: "What about production deployment?"**
**A:** DSPy is production-ready. Many companies use it. The structured outputs and type safety make it MORE reliable than raw prompts.

### **Q: "How is this different from Instructor or Pydantic AI?"**
**A:** Those focus on structured outputs only. DSPy is a full framework with modules, composition, and optimization.

---

## 🔧 **Technical Setup for Teaching**

### **Before Class Checklist:**

- [ ] Test all code examples in both notebooks
- [ ] Verify `config.json` setup instructions work
- [ ] Ensure API keys work (test with a simple call)
- [ ] Convert presentation to your preferred format
- [ ] Print/share the cheat sheet
- [ ] Prepare live coding environment (Jupyter/VS Code)
- [ ] Have backup examples ready in case of API issues

### **Recommended Tools:**

**For Presentation:**
- Marp for VS Code (Markdown slides)
- reveal.js (web-based presentations)
- Deckset (Mac, Markdown to slides)

**For Live Coding:**
- Jupyter Lab (clean, professional)
- VS Code with Jupyter extension (good for showing inspect_history)
- Google Colab (no local setup needed)

**For Screen Sharing:**
- Increase font size in terminal/notebook
- Use presenter mode if available
- Have zoom/screenshare tested beforehand

---

## 📚 **Additional Resources to Share**

### **Official DSPy Resources:**
- Website: https://dspy.ai/
- GitHub: https://github.com/stanfordnlp/dspy
- Documentation: https://dspy-docs.vercel.app/
- Discord: [Link in GitHub repo]

### **Recommended Reading:**
- DSPy paper: "Compiling Declarative Language Model Calls"
- Blog posts on dspy.ai
- Example projects in GitHub `/examples`

### **Video Tutorials:**
- [Link DSPy intro videos if available]
- Conference talks on DSPy
- Community tutorials

---

## 🎁 **Bonus Activities**

### **Challenge 1: Build a Competitor**
**Time:** 20-30 minutes
**Task:** Take the traditional prompt engineering example from slide 3 and recreate it in DSPy
**Goal:** Experience the difference firsthand

### **Challenge 2: Extend the Support Email**
**Time:** 15-20 minutes
**Task:** Add new fields to the SupportEmail signature:
- Estimated resolution time
- Department to route to
- Similar past tickets

### **Challenge 3: Chain Multiple Modules**
**Time:** 30 minutes
**Task:** Build a pipeline:
1. Classify email intent
2. Extract entities
3. Generate response draft
**Goal:** Learn module composition

---

## 📝 **Feedback Collection**

### **During Session:**
- Use polls/quizzes to check understanding
- Ask "fist to five" confidence checks
- Monitor chat/questions for confusion points

### **After Session:**
- Google Form survey
- Key questions:
  - What was most valuable?
  - What was most confusing?
  - What would you like more depth on?
  - Rate your confidence building DSPy systems (1-5)

---

## 🚀 **Next Steps for Students**

### **Immediate (Next 24 hours):**
1. Complete all exercises in `Introduction_to_DSPy.ipynb`
2. Build one DSPy system for your own use case
3. Share in class Discord/forum

### **This Week:**
1. Work through `MLS_W3_RAG_&_dspyRAG___JHU_Agentic_AI.ipynb`
2. Compare traditional RAG to DSPy RAG
3. Experiment with optimizers (if ready)

### **For Advanced Students:**
- Contribute to DSPy GitHub
- Try building custom modules
- Implement evaluation metrics
- Explore BootstrapFewShot optimizer

---

## 🎓 **Instructor Notes**

### **Key Pedagogical Strategies:**

1. **Contrast Learning**: Always show traditional approach vs DSPy
2. **Incremental Complexity**: Start simple (Predict), add features (ChainOfThought)
3. **Transparency**: Use `inspect_history()` liberally to demystify
4. **Hands-On First**: After explaining concept, have students try it
5. **Real-World Context**: Use business scenarios students can relate to

### **Common Pitfalls to Avoid:**

- ❌ Showing optimizers too early (overwhelming)
- ❌ Not demonstrating failures (students need to see debugging)
- ❌ Going too fast through signatures (they're foundational)
- ❌ Skipping `inspect_history()` (it's the "aha" moment)
- ❌ Not relating back to prompt engineering pain points

### **Success Indicators:**

- ✅ Students use `inspect_history()` without prompting
- ✅ Students ask about custom modules
- ✅ Students debug their own signature issues
- ✅ Students compare DSPy favorably to alternatives
- ✅ Students start building their own projects

---

## 📞 **Support & Questions**

For teaching-specific questions about these materials:
- Review the presentation notes
- Check the cheat sheet for quick references
- Refer to the official DSPy docs for technical details

For student technical issues:
- Point them to `DSPy_Cheat_Sheet.md` first
- Use `inspect_history()` to debug together
- Check GitHub issues for known problems
- Ask in DSPy Discord community

---

**Good luck with your DSPy teaching!** 🎉

Remember: You're not just teaching a framework—you're teaching a new way of thinking about AI programming. Focus on the paradigm shift, and the code will follow.

---

**Last Updated:** 2026-01-30
**Version:** 1.0
**Maintainer:** JHU Agentic AI Course Team
