"""
Research Assistant with Evaluation and Langfuse Integration
Extends the Week 3 research assistant with evaluation capabilities.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langfuse.decorators import observe, langfuse_context
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load environment variables
env_path = Path(".env")
if not env_path.exists():
    env_path = Path("../.env")
if not env_path.exists():
    env_path = Path("../../.env")
load_dotenv(env_path)

from eval_system import RuleBasedValidator, LLMJudge, GoldenDataset

# Initialize components
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) if os.getenv("OPENAI_API_KEY") else None
validator = RuleBasedValidator()
judge = LLMJudge(llm=llm)


@observe()
def research_assistant(query: str) -> dict:
    """
    Simple research assistant that answers queries.
    Automatically traced by Langfuse via @observe decorator.
    """
    if not query or not query.strip():
        return {
            "answer": "Please provide a valid query.",
            "sources": [],
            "error": True
        }
    
    if not llm:
        return {
            "answer": "[Mock] Research summary about the query. This is a placeholder response.",
            "sources": ["mock-source-1", "mock-source-2"],
            "error": False
        }
    
    # Simple research prompt
    prompt = f"""You are a research assistant. Answer the following query concisely and accurately.

Query: {query}

Provide a clear, factual answer. If you reference specific information, mention that it comes from your training data."""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    
    # Get current trace ID for scoring
    trace_id = langfuse_context.get_current_trace_id()
    
    result = {
        "answer": response.content,
        "sources": ["training_data"],  # Simplified for demo
        "error": False
    }
    
    # Validate response
    validation_result = validator.validate_response(result)
    
    # Log validation to Langfuse
    if trace_id:
        from langfuse import Langfuse
        langfuse = Langfuse()
        langfuse.score(
            trace_id=trace_id,
            name="rule_based_validation",
            value=1.0 if validation_result["valid"] else 0.0,
            comment=f"Validation errors: {', '.join(validation_result['errors']) if validation_result['errors'] else 'None'}"
        )
    
    # If validation fails, add errors to result
    if not validation_result["valid"]:
        result["validation_errors"] = validation_result["errors"]
    
    return result


@observe()
def research_assistant_with_eval(query: str, expected_topics: list = None, expected_not: list = None) -> dict:
    """
    Research assistant with full evaluation pipeline.
    Includes rule-based validation and LLM-as-judge scoring.
    """
    # Get the research result
    result = research_assistant(query)
    
    # Get trace ID for scoring
    trace_id = langfuse_context.get_current_trace_id()
    
    # Run LLM-as-judge evaluation if we have a response
    if result.get("answer") and not result.get("error"):
        eval_result = judge.evaluate(
            query=query,
            response=result["answer"],
            expected_topics=expected_topics or [],
            expected_not=expected_not or [],
            trace_id=trace_id
        )
        result["evaluation"] = eval_result
    
    return result


def run_golden_dataset_eval(dataset_path: str = "golden_dataset.json"):
    """
    Run evaluation on golden dataset.
    Returns results for all test cases.
    """
    dataset = GoldenDataset(dataset_path)
    results = []
    
    for test_case in dataset.get_all_cases():
        query = test_case.get("query", "")
        expected_topics = test_case.get("expected_topics", [])
        expected_not = test_case.get("expected_not", [])
        min_score = test_case.get("min_score", 0.0)
        
        # Run research assistant with evaluation
        result = research_assistant_with_eval(
            query=query,
            expected_topics=expected_topics,
            expected_not=expected_not
        )
        
        # Check if meets minimum score
        eval_score = result.get("evaluation", {}).get("overall", 0.0)
        passed = eval_score >= min_score
        
        results.append({
            "test_id": test_case.get("id"),
            "query": query,
            "passed": passed,
            "score": eval_score,
            "min_score": min_score,
            "result": result
        })
    
    return results


if __name__ == "__main__":
    # Example usage
    print("Testing Research Assistant with Evaluation...")
    
    # Single query test
    result = research_assistant_with_eval(
        query="What are the key benefits of RAG?",
        expected_topics=["grounding", "reduced hallucination"],
        expected_not=["fine-tuning"]
    )
    
    print("\nResult:")
    print(f"Answer: {result.get('answer', '')[:200]}...")
    print(f"Evaluation: {result.get('evaluation', {})}")
    
    # Run golden dataset evaluation
    print("\n\nRunning Golden Dataset Evaluation...")
    eval_results = run_golden_dataset_eval()
    
    print(f"\nEvaluated {len(eval_results)} test cases")
    passed = sum(1 for r in eval_results if r["passed"])
    print(f"Passed: {passed}/{len(eval_results)}")
    
    print("\nCheck your Langfuse dashboard to see traces and scores!")

