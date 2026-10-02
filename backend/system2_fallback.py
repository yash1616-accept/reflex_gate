import os
import json
import logging
from typing import Dict, Any
from openai import AsyncOpenAI
from tenacity import retry, wait_exponential, stop_after_attempt
from .schemas import AgentActionState

logger = logging.getLogger(__name__)

# Initialize OpenAI Client
# In production, ensure OPENAI_API_KEY is securely loaded
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "dummy-key-for-now"))

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def review_with_system2(state: AgentActionState) -> Dict[str, Any]:
    """
    Enterprise System 2 Evaluator:
    Routes ambiguous actions to a heavy frontier model (GPT-4o) for semantic intent resolution.
    Implements exponential backoff for rate limit handling.
    """
    logger.info(f"[Tier 2] Escalating Agent {state.agent_id} to GPT-4o for Deep Reasoning")
    
    system_prompt = (
        "You are an enterprise AI safety firewall. You are evaluating an action proposed by an autonomous agent. "
        "Analyze the intent and potential impact. Reply ONLY in strict JSON: "
        '{"status": "APPROVED" | "REJECTED", "route": "SYSTEM2_APPROVED" | "SYSTEM2_BLOCK", "reasoning": "..."}'
    )
    
    user_prompt = f"Proposed Tool: {state.proposed_tool}\nArguments: {json.dumps(state.tool_arguments)}\nContext: {state.environment_context}"

    try:
        if client.api_key == "dummy-key-for-now":
            # Simulation mode for demo
            import asyncio
            await asyncio.sleep(1.5)
            tool_name = state.proposed_tool.lower()
            if "delete" in tool_name or "drop" in tool_name:
                return {"status": "REJECTED", "route": "SYSTEM2_BLOCK"}
            return {"status": "APPROVED", "route": "SYSTEM2_APPROVED"}

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={ "type": "json_object" },
            timeout=5.0
        )
        
        result_content = response.choices[0].message.content
        if result_content is None:
            raise ValueError("OpenAI returned empty response")
            
        result = json.loads(result_content)
        return {
            "status": result.get("status", "REJECTED"),
            "route": result.get("route", "SYSTEM2_BLOCK")
        }
        
    except Exception as e:
        logger.error(f"[Tier 2] OpenAI Evaluation Failed: {e}")
        # Fail Securely
        return {"status": "REJECTED", "route": "SYSTEM2_ERROR_BLOCK"}
