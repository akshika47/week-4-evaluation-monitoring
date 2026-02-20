# Week 4: Evaluation, Monitoring & Shipping

## The Difference Between a Demo and a Product

This week you'll learn how to make your AI systems production-ready with evaluation, observability, and monitoring using Langfuse.

## 📚 What You'll Learn

1. **Evaluation Fundamentals** — Golden datasets, rule-based checks, LLM-as-judge
2. **Langfuse Integration** — Tracing, scoring, and observability
3. **Monitoring & Quality Tracking** — Detecting silent degradation
4. **Production Readiness** — Fallbacks, validation, and safe deployment

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the `week-4` directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

Get your keys:
- **OpenAI**: https://platform.openai.com/api-keys
- **Langfuse**: https://cloud.langfuse.com (free tier available)

### 3. Run the Notebook

```bash
jupyter notebook week4_notebook.ipynb
```

Or run the demo script:

```bash
python demo_evaluation.py
```

## 📁 Files

- `week4_notebook.ipynb` - Main interactive notebook with all examples
- `eval_system.py` - Evaluation system classes (GoldenDataset, RuleBasedValidator, LLMJudge)
- `research_assistant_with_eval.py` - Research assistant with evaluation integration
- `golden_dataset.json` - Sample golden dataset with test cases
- `demo_evaluation.py` - Demo script showing complete evaluation pipeline
- `requirements.txt` - Python dependencies

## 🎯 Key Concepts

### Golden Datasets
Version-controlled test cases that represent known-good behavior. Your source of truth for evaluation.

### Rule-Based Validation
Fast, deterministic checks that catch 80% of issues:
- Format validation (JSON structure, required fields)
- Length validation (min/max tokens)
- Safety checks (no PII, no banned content)
- Grounding checks (sources present)

### LLM-as-Judge
Use an LLM to score response quality with a rubric. Always validate against human judgments!

### Langfuse Integration
- Automatic tracing with `@observe` decorator
- Manual scoring with `langfuse.score()`
- Full observability dashboard

## 📊 Langfuse Dashboard

After running the notebook or demo script, check your Langfuse dashboard:
- **Traces**: See full execution trees
- **Scores**: Track quality metrics over time
- **Datasets**: Manage golden datasets
- **Analytics**: Cost, latency, and quality trends

## 🎓 Learning Objectives

By the end of this week, you will:

- ✅ Understand why evaluation is mandatory, not optional
- ✅ Build a golden dataset for your system
- ✅ Implement rule-based validation checks
- ✅ Use LLM-as-judge for quality scoring
- ✅ Integrate Langfuse for full observability
- ✅ Monitor quality over time

## 🔗 Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [LangGraph Evaluation Patterns](https://langchain-ai.github.io/langgraph/how-tos/evaluation/)
- [Langfuse Cloud](https://cloud.langfuse.com)

## 💡 Tips

1. **Start with rule-based checks** - They're fast, free, and catch most issues
2. **Grow your golden dataset** - Add test cases as you find bugs
3. **Validate LLM-as-judge** - Always compare to human judgments
4. **Check Langfuse regularly** - Set up alerts for quality degradation
5. **Version your datasets** - Treat them like code

---

**Happy Building!** 🚀

