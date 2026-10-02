from pydantic import BaseModel
from typing import Dict, Any, Literal

class AgentActionState(BaseModel):
    agent_id: str
    session_id: str
    user_role: str
    proposed_tool: str
    tool_arguments: Dict[str, Any]
    environment_context: str

class JevReflexEvaluation(BaseModel):
    is_malicious_or_jailbreak: float
    risk_score: int
    recommended_route: Literal["ALLOW_FAST_PATH", "ESCALATE_TO_SYSTEM2", "REQUIRE_HUMAN_APPROVAL", "BLOCK_IMMEDIATELY"]
