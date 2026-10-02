import requests
from typing import Dict, Any, Optional

class EvaluationDecision:
    def __init__(self, data: Dict[str, Any]):
        decision = data.get("engine_decision", {})
        self.status = decision.get("execution_status", "UNKNOWN")
        self.route = decision.get("assigned_route", "UNKNOWN")
        self.latency_ms = decision.get("latency_breakdown", {}).get("total_latency_ms", 0.0)

    @property
    def is_approved(self) -> bool:
        return self.status == "APPROVED"

    @property
    def is_blocked(self) -> bool:
        return self.status == "REJECTED"
        
    @property
    def reason(self) -> str:
        return f"Routed via {self.route}"

class ReflexGuard:
    """
    Lightweight SDK client to connect your autonomous agents to the ReflexGate firewall.
    """
    def __init__(self, endpoint: str = "http://localhost:8000"):
        self.endpoint = endpoint.rstrip("/")
        
    def evaluate(self, 
                 agent_id: str, 
                 proposed_tool: str, 
                 arguments: Dict[str, Any], 
                 context: str = "",
                 session_id: str = "default_session",
                 user_role: str = "agent") -> EvaluationDecision:
        
        payload = {
            "agent_id": agent_id,
            "session_id": session_id,
            "user_role": user_role,
            "proposed_tool": proposed_tool,
            "tool_arguments": arguments,
            "environment_context": context
        }
        
        try:
            response = requests.post(f"{self.endpoint}/v1/gate/evaluate", json=payload, timeout=15.0)
            response.raise_for_status()
            return EvaluationDecision(response.json())
        except requests.exceptions.RequestException as e:
            # Fail-safe posture: Block if gateway is unreachable
            return EvaluationDecision({
                "engine_decision": {
                    "execution_status": "REJECTED",
                    "assigned_route": "GATEWAY_UNREACHABLE"
                }
            })
