import json
from typing import Dict, Any
from .schemas import JevReflexEvaluation, AgentActionState
from .config import settings

class Tier1LocalEvaluator:
    """
    Enterprise Tier 1 Fast-Path Evaluator.
    In a real production environment, this wraps an ONNX-optimized SLM or DeBERTa classification model.
    For this demo, it acts as a deterministic ultra-fast intent classifier.
    """
    
    async def run(self, prompt: str) -> Any:
        # We parse the prompt string to extract the state for the simulation
        # The engine passes str(state.model_dump())
        import ast
        try:
            state_dict = ast.literal_eval(prompt)
        except Exception:
            state_dict = {}

        tool_name = str(state_dict.get('proposed_tool', '')).lower()
        args = str(state_dict.get('tool_arguments', '')).lower()
        
        # Simulate ONNX Classification
        is_malicious = 0.05
        risk_score = 1
        route = "ALLOW_FAST_PATH"
        
        # Malicious intent detection
        if "drop" in args or "delete" in args or "truncate" in args:
            is_malicious = 0.99
            risk_score = 5
            route = "BLOCK_IMMEDIATELY"
            
        # Ambiguous actions (triggers System 2)
        elif "refund" in tool_name or "transfer" in tool_name or "update" in tool_name:
            is_malicious = 0.15
            risk_score = 3
            route = "ESCALATE_TO_SYSTEM2"

        # Mocking the result wrapper that pydantic-ai would normally provide
        class ResultWrapper:
            def __init__(self, data):
                self.data = data
                
        return ResultWrapper(
            JevReflexEvaluation(
                is_malicious_or_jailbreak=is_malicious,
                risk_score=risk_score,
                recommended_route=route
            )
        )

# Export the agent
jev_agent = Tier1LocalEvaluator()
