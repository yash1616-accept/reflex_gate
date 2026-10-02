import time
from typing import Dict, Any
from .schemas import AgentActionState, JevReflexEvaluation
from .config import settings
from .system2_fallback import review_with_system2

class ReflexGateEngine:
    @staticmethod
    async def evaluate_and_route(
        state: AgentActionState,
        jev_eval: JevReflexEvaluation,
        jev_latency_ms: float
    ) -> Dict[str, Any]:
        # In a real setup, confidence would be parsed from Jev response metadata
        # For this prototype, we'll simulate an extraction or assume high confidence unless escalated
        confidence = 0.85 
        
        rlcd_threshold = settings.DEFAULT_RLCD_THRESHOLD
        
        system2_latency_ms = 0.0
        route = ""
        status = ""
        cost_usd = 0.0001 # Base Jev fast-path cost estimation
        
        # Tier 4 (Hard Stop)
        if jev_eval.is_malicious_or_jailbreak >= 0.65 or jev_eval.recommended_route == "BLOCK_IMMEDIATELY":
            status = "REJECTED"
            route = "BLOCK"
            
        # Tier 3 (Human in Loop)
        elif jev_eval.risk_score >= 4 or jev_eval.recommended_route == "REQUIRE_HUMAN_APPROVAL":
            status = "PENDING"
            route = "HUMAN_IN_THE_LOOP"
            
        # Tier 2 (System 2 Escalation)
        elif confidence < rlcd_threshold or jev_eval.recommended_route == "ESCALATE_TO_SYSTEM2":
            start_time = time.perf_counter()
            
            s2_result = await review_with_system2(state)
            
            system2_latency_ms = (time.perf_counter() - start_time) * 1000
            
            status = s2_result["status"]
            route = s2_result["route"]
            cost_usd += 0.0300 # System 2 (GPT-4o) estimated cost penalty
            confidence = 0.99 # Calibrated high confidence after System 2 review
            
        # Tier 1 (Fast Path)
        elif jev_eval.is_malicious_or_jailbreak < 0.20 and jev_eval.risk_score <= 2 and confidence >= rlcd_threshold:
            status = "APPROVED"
            route = "FAST_PATH_LOCAL"
            
        else:
            # Fallback catch-all
            status = "PENDING"
            route = "ESCALATE_TO_SYSTEM2"
            
        total_latency_ms = jev_latency_ms + system2_latency_ms
        
        return {
            "execution_status": status,
            "assigned_route": route,
            "calibrated_confidence": confidence,
            "latency_breakdown": {
                "jev_latency_ms": round(jev_latency_ms, 2),
                "system2_latency_ms": round(system2_latency_ms, 2),
                "total_latency_ms": round(total_latency_ms, 2)
            },
            "estimated_cost_usd": cost_usd
        }
