import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ReflexAuditLog(Base):
    __tablename__ = "reflex_audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String, index=True, nullable=False)
    session_id = Column(String, nullable=False)
    
    proposed_tool = Column(String, nullable=False)
    tool_arguments = Column(JSONB, nullable=False)
    
    noul_malicious_prob = Column(Float, nullable=False)
    score_risk_level = Column(Integer, nullable=False)
    choice_route = Column(String, nullable=False)
    
    rlcd_confidence = Column(Float, nullable=False)
    final_execution_route = Column(String, nullable=False)
    
    total_latency_ms = Column(Float, nullable=False)
    jev_latency_ms = Column(Float, nullable=False)
    system2_latency_ms = Column(Float, nullable=False)
    
    cost_usd = Column(Numeric(10, 8), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
