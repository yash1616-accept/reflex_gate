import os
import logging
from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, func, desc
from .models import ReflexAuditLog, Base

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgrespassword@db:5432/reflexgate")

# Enterprise Connection Pooling Configuration
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    pool_size=20,
    max_overflow=50,
    pool_recycle=1800 # Recycle connections every 30 mins to prevent stale drops
)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def log_evaluation_background(state_dict: Dict[str, Any], jev_eval_dict: Dict[str, Any], engine_decision: Dict[str, Any]):
    try:
        async with AsyncSessionLocal() as session:
            log_entry = ReflexAuditLog(
                agent_id=state_dict.get("agent_id", ""),
                session_id=state_dict.get("session_id", ""),
                proposed_tool=state_dict.get("proposed_tool", ""),
                tool_arguments=state_dict.get("tool_arguments", {}),
                noul_malicious_prob=jev_eval_dict.get("is_malicious_or_jailbreak", 0.0),
                score_risk_level=jev_eval_dict.get("risk_score", 0),
                choice_route=jev_eval_dict.get("recommended_route", ""),
                rlcd_confidence=engine_decision.get("calibrated_confidence", 0.0),
                final_execution_route=engine_decision.get("assigned_route", ""),
                total_latency_ms=engine_decision["latency_breakdown"]["total_latency_ms"],
                jev_latency_ms=engine_decision["latency_breakdown"]["jev_latency_ms"],
                system2_latency_ms=engine_decision["latency_breakdown"]["system2_latency_ms"],
                cost_usd=engine_decision.get("estimated_cost_usd", 0.0)
            )
            session.add(log_entry)
            await session.commit()
    except Exception as e:
        logger.error(f"Database insertion failed: {e}")

async def get_recent_logs(limit: int = 50) -> List[Dict[str, Any]]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(ReflexAuditLog).order_by(desc(ReflexAuditLog.created_at)).limit(limit)
        )
        logs = result.scalars().all()
        return [
            {
                "id": str(log.id),
                "agent": log.agent_id,
                "tool": log.proposed_tool,
                "risk": log.score_risk_level,
                "confidence": log.rlcd_confidence,
                "route": "Fast Path" if "FAST_PATH" in log.final_execution_route else ("System 2" if "SYSTEM2" in log.final_execution_route else "Blocked"),
                "time": log.created_at.strftime("%H:%M:%S") if log.created_at else ""
            }
            for log in logs
        ]

async def get_analytics_stats() -> Dict[str, Any]:
    async with AsyncSessionLocal() as session:
        total_requests = await session.scalar(select(func.count(ReflexAuditLog.id))) or 0
        avg_total_latency = float(await session.scalar(select(func.avg(ReflexAuditLog.total_latency_ms))) or 0.0)
        avg_jev_latency = float(await session.scalar(select(func.avg(ReflexAuditLog.jev_latency_ms))) or 0.0)
        total_cost = float(await session.scalar(select(func.sum(ReflexAuditLog.cost_usd))) or 0.0)
        
        routes = await session.execute(
            select(ReflexAuditLog.final_execution_route, func.count(ReflexAuditLog.id)).group_by(ReflexAuditLog.final_execution_route)
        )
        route_distribution = {route: count for route, count in routes.all()}
        
        baseline_cost = total_requests * 0.03
        estimated_savings = baseline_cost - total_cost

        return {
            "total_requests": total_requests,
            "avg_total_latency_ms": round(avg_total_latency, 2),
            "avg_jev_latency_ms": round(avg_jev_latency, 2),
            "route_distribution": route_distribution,
            "total_cost_usd": round(total_cost, 4),
            "estimated_savings_usd": round(estimated_savings, 4)
        }
