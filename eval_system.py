"""
Evaluation System for Research Assistant
Implements golden datasets, rule-based validation, and LLM-as-judge scoring.
"""

import json
import re
from typing import Dict, List, Optional, Any
from pathlib import Path
from langfuse import Langfuse
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class GoldenDataset:
    """Manages golden dataset test cases."""
    
    def __init__(self, dataset_path: str):
        """Load golden dataset from JSON file."""
        with open(dataset_path, 'r') as f:
            self.data = json.load(f)
        self.test_cases = self.data.get('test_cases', [])
        self.name = self.data.get('name', 'unknown')
        self.version = self.data.get('version', '1.0.0')
    
    def get_test_case(self, test_id: str) -> Optional[Dict]:
        """Get a specific test case by ID."""
        for case in self.test_cases:
            if case.get('id') == test_id:
                return case
        return None
    
    def get_all_cases(self) -> List[Dict]:
        """Get all test cases."""
        return self.test_cases
    
    def get_cases_by_category(self, category: str) -> List[Dict]:
        """Get test cases by category."""
        return [case for case in self.test_cases if case.get('category') == category]


class RuleBasedValidator:
    """Fast, deterministic validation checks."""
    
    def __init__(self):
        self.errors = []
    
    def validate_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate response against rule-based checks.
        Returns dict with 'valid' (bool) and 'errors' (list).
        """
        self.errors = []
        
        # Format check
        if not isinstance(response, dict):
            self.errors.append("Response must be a dictionary")
            return {"valid": False, "errors": self.errors}
        
        # Required fields check
        if "answer" not in response:
            self.errors.append("Missing 'answer' field")
        elif not isinstance(response.get("answer"), str):
            self.errors.append("'answer' field must be a string")
        
        # Length check
        answer = response.get("answer", "")
        if len(answer) < 10:
            self.errors.append("Response too short (minimum 10 characters)")
        if len(answer) > 5000:
            self.errors.append("Response too long (maximum 5000 characters)")
        
        # Grounding check (if sources field exists)
        if "sources" in response:
            sources = response.get("sources", [])
            if not isinstance(sources, list):
                self.errors.append("'sources' must be a list")
            elif len(sources) == 0 and answer:
                self.errors.append("No sources cited for response")
        
        # Safety check - basic PII detection
        if self._contains_pii(answer):
            self.errors.append("Potential PII detected in response")
        
        # Safety check - banned content (basic)
        if self._contains_banned_content(answer):
            self.errors.append("Banned content detected")
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors
        }
    
    def _contains_pii(self, text: str) -> bool:
        """Basic PII detection - email and phone patterns."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if re.search(email_pattern, text) or re.search(phone_pattern, text):
            return True
        return False
    
    def _contains_banned_content(self, text: str) -> bool:
        """Basic banned content check."""
        banned_words = ["hack", "exploit", "bypass"]  # Very basic example
        text_lower = text.lower()
        for word in banned_words:
            if word in text_lower:
                return True
        return False


class LLMJudge:
    """LLM-as-judge for quality evaluation."""
    
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize with optional LLM (uses gpt-4o-mini by default)."""
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0)
        try:
            self.langfuse = Langfuse()
        except:
            self.langfuse = None
    
    def evaluate(
        self,
        query: str,
        response: str,
        expected_topics: List[str] = None,
        expected_not: List[str] = None,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluate response quality using LLM-as-judge.
        Returns scores and reasoning.
        """
        expected_topics = expected_topics or []
        expected_not = expected_not or []
        
        rubric = """Score this response on a scale of 1-5 for each dimension:

1. **Relevance** (1-5): Does the response directly address the query?
2. **Accuracy** (1-5): Is the information factually correct?
3. **Completeness** (1-5): Are key points covered?
4. **Grounding** (1-5): Are claims supported by sources or evidence?

Return your evaluation as JSON with this structure:
{
  "scores": {
    "relevance": 4,
    "accuracy": 5,
    "completeness": 3,
    "grounding": 4
  },
  "reasoning": "Brief explanation of scores",
  "overall": 4.0
}

Calculate overall as the average of the four scores."""

        # Build evaluation prompt
        eval_prompt = f"""Query: {query}

Response to evaluate:
{response}

Expected topics to cover: {', '.join(expected_topics) if expected_topics else 'None specified'}
Topics that should NOT appear: {', '.join(expected_not) if expected_not else 'None specified'}

Evaluate the response according to the rubric above."""

        messages = [
            SystemMessage(content=rubric),
            HumanMessage(content=eval_prompt)
        ]
        
        try:
            judge_response = self.llm.invoke(messages)
            judge_text = judge_response.content
            
            # Parse JSON from response
            scores = self._parse_scores(judge_text)
            
            # Log scores to Langfuse if trace_id provided
            if trace_id and self.langfuse:
                for score_name, score_value in scores.get("scores", {}).items():
                    self.langfuse.score(
                        trace_id=trace_id,
                        name=f"llm_judge_{score_name}",
                        value=float(score_value),
                        comment=scores.get("reasoning", "")
                    )
                
                # Log overall score
                self.langfuse.score(
                    trace_id=trace_id,
                    name="llm_judge_overall",
                    value=float(scores.get("overall", 0)),
                    comment=scores.get("reasoning", "")
                )
            
            return scores
            
        except Exception as e:
            return {
                "scores": {},
                "reasoning": f"Error during evaluation: {str(e)}",
                "overall": 0.0,
                "error": str(e)
            }
    
    def _parse_scores(self, text: str) -> Dict[str, Any]:
        """Parse scores from LLM response."""
        # Try to extract JSON from response
        json_match = re.search(r'\{[^{}]*"scores"[^{}]*\{[^{}]*\}[^{}]*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Fallback: try to find overall score
        overall_match = re.search(r'"overall":\s*(\d+\.?\d*)', text)
        overall = float(overall_match.group(1)) if overall_match else 0.0
        
        return {
            "scores": {},
            "reasoning": text[:200],
            "overall": overall
        }


class LangfuseTracer:
    """Wrapper for easy Langfuse integration."""
    
    def __init__(self):
        """Initialize Langfuse client."""
        try:
            self.langfuse = Langfuse()
        except:
            self.langfuse = None
    
    def get_current_trace_id(self) -> Optional[str]:
        """Get current trace ID from context."""
        try:
            from langfuse.decorators import langfuse_context
            return langfuse_context.get_current_trace_id()
        except:
            return None
    
    def score_trace(
        self,
        trace_id: str,
        name: str,
        value: float,
        comment: str = ""
    ):
        """Score a trace."""
        if self.langfuse:
            self.langfuse.score(
                trace_id=trace_id,
                name=name,
                value=value,
                comment=comment
            )

