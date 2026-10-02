import time
import asyncio
import logging
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse

from .schemas import AgentActionState, JevReflexEvaluation
from .jev_client import jev_agent
from .engine import ReflexGateEngine
from .database import init_db, log_evaluation_background, get_analytics_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ReflexGate AI Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.warning(f"Could not initialize database (Make sure PostgreSQL is running): {e}")

@app.post("/v1/gate/evaluate")
async def evaluate_action(state: AgentActionState):
    start_time = time.perf_counter()
    
    try:
        prompt = f"Agent Action State:\n{state.model_dump_json()}"
        
        # Execute single-pass parallel query against Jev
        result = await jev_agent.run(prompt)
        jev_eval: JevReflexEvaluation = result.data
        
        end_time = time.perf_counter()
        jev_latency_ms = (end_time - start_time) * 1000
        
        # Run through Tri-Tier Decision Engine
        engine_decision = await ReflexGateEngine.evaluate_and_route(
            state=state, 
            jev_eval=jev_eval, 
            jev_latency_ms=jev_latency_ms
        )
        
        # Dispatch background logging task
        asyncio.create_task(
            log_evaluation_background(
                state.model_dump(),
                jev_eval.model_dump(),
                engine_decision
            )
        )
        
        return {
            "evaluation": jev_eval.model_dump(),
            "engine_decision": engine_decision,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error evaluating action: {e}")
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error during evaluation",
                "latency_ms": round(latency_ms, 2)
            }
        )

@app.get("/v1/analytics/stats")
async def get_stats():
    try:
        stats = await get_analytics_stats()
        return stats
    except Exception as e:
        logger.error(f"Error retrieving analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

@app.get("/v1/logs")
async def get_logs():
    try:
        from .database import get_recent_logs
        logs = await get_recent_logs(50)
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Error retrieving logs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve logs")
