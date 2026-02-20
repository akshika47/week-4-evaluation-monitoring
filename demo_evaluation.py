#!/usr/bin/env python3
"""
Demo Script: Evaluation and Monitoring with Langfuse

This script demonstrates the complete evaluation pipeline:
1. Loads golden dataset
2. Runs research assistant with evaluation
3. Shows results and Langfuse dashboard links
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(".env")
if not env_path.exists():
    env_path = Path("../.env")
if not env_path.exists():
    env_path = Path("../../.env")
load_dotenv(env_path)

from eval_system import GoldenDataset, RuleBasedValidator, LLMJudge
from research_assistant_with_eval import research_assistant_with_eval, run_golden_dataset_eval
from langfuse import Langfuse
from langchain_openai import ChatOpenAI

# Initialize
langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
langfuse = Langfuse() if os.getenv("LANGFUSE_PUBLIC_KEY") else None

def main():
    print("=" * 70)
    print("🚀 Week 4: Evaluation & Monitoring Demo")
    print("=" * 70)
    print()
    
    # Step 1: Load golden dataset
    print("📚 Step 1: Loading Golden Dataset...")
    try:
        dataset = GoldenDataset("golden_dataset.json")
        print(f"   ✅ Loaded {len(dataset.test_cases)} test cases")
        print(f"   Dataset: {dataset.name} (v{dataset.version})")
    except Exception as e:
        print(f"   ❌ Error loading dataset: {e}")
        return
    
    print()
    
    # Step 2: Single query demo
    print("🔍 Step 2: Single Query Evaluation...")
    print("-" * 70)
    
    test_query = "What are the key benefits of RAG?"
    print(f"Query: {test_query}")
    
    result = research_assistant_with_eval(
        query=test_query,
        expected_topics=["grounding", "reduced hallucination", "up-to-date info"],
        expected_not=["fine-tuning"]
    )
    
    print(f"\nAnswer: {result.get('answer', '')[:150]}...")
    
    # Show validation
    validation = result.get("validation", {})
    if validation:
        print(f"\nValidation: {'✅ Passed' if validation.get('valid') else '❌ Failed'}")
        if validation.get('errors'):
            print(f"   Errors: {', '.join(validation['errors'])}")
    
    # Show evaluation
    evaluation = result.get("evaluation", {})
    if evaluation:
        print(f"\nLLM-as-Judge Evaluation:")
        print(f"   Overall Score: {evaluation.get('overall', 0.0):.2f}")
        scores = evaluation.get('scores', {})
        if scores:
            print(f"   Scores: {scores}")
    
    print()
    
    # Step 3: Run golden dataset evaluation
    print("📊 Step 3: Running Golden Dataset Evaluation...")
    print("-" * 70)
    
    try:
        eval_results = run_golden_dataset_eval()
        
        # Summary
        total = len(eval_results)
        passed = sum(1 for r in eval_results if r["passed"])
        validation_passed = sum(1 for r in eval_results if r["validation_passed"])
        
        print(f"\n📈 Evaluation Summary:")
        print(f"   Total test cases: {total}")
        print(f"   Validation passed: {validation_passed}/{total} ({validation_passed/total*100:.1f}%)")
        print(f"   Score threshold passed: {passed}/{total} ({passed/total*100:.1f}%)")
        
        print(f"\n📋 Detailed Results:")
        for r in eval_results[:5]:  # Show first 5
            status = "✅" if r["passed"] else "❌"
            val_status = "✅" if r["validation_passed"] else "❌"
            print(f"   {status} {r['test_id']}: Score {r['score']:.2f} (min: {r['min_score']:.2f}) | Validation: {val_status}")
        
        if len(eval_results) > 5:
            print(f"   ... and {len(eval_results) - 5} more test cases")
        
    except Exception as e:
        print(f"   ❌ Error running evaluation: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Step 4: Langfuse dashboard info
    print("🔗 Step 4: Langfuse Dashboard")
    print("-" * 70)
    print(f"   📊 Dashboard URL: {langfuse_host}")
    print(f"   💡 All traces, scores, and metrics are logged there!")
    print(f"   💡 Check the 'Traces' section to see individual executions")
    print(f"   💡 Check the 'Scores' section to see evaluation metrics")
    print(f"   💡 Check the 'Datasets' section to manage golden datasets")
    
    print()
    print("=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Open Langfuse dashboard to explore traces")
    print("2. Add more test cases to golden_dataset.json")
    print("3. Run weekly evaluations to track quality over time")
    print("4. Use eval results to improve your prompts")


if __name__ == "__main__":
    main()

