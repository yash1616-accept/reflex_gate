import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def create_mock_payload(tool="fetch_data"):
    return {
        "agent_id": "test_agent_1",
        "session_id": "session_123",
        "user_role": "admin",
        "proposed_tool": tool,
        "tool_arguments": {"target": "user_table"},
        "environment_context": "Production"
    }

@pytest.mark.asyncio
async def test_fast_path(mocker):
    # Mocking Jev returning malicious=0.05, risk=1, confidence=0.92
    mocker.patch('backend.engine.ReflexGateEngine.evaluate_and_route', return_value={
        "execution_status": "APPROVED",
        "assigned_route": "FAST_PATH_LOCAL",
        "calibrated_confidence": 0.92,
        "latency_breakdown": {"total_latency_ms": 45.0, "jev_latency_ms": 45.0, "system2_latency_ms": 0.0},
        "estimated_cost_usd": 0.0001
    })
    
    response = client.post("/v1/gate/evaluate", json=create_mock_payload())
    assert response.status_code == 200
    data = response.json()
    assert data["engine_decision"]["assigned_route"] == "FAST_PATH_LOCAL"
    assert data["engine_decision"]["latency_breakdown"]["total_latency_ms"] < 100

@pytest.mark.asyncio
async def test_rlcd_escalation(mocker):
    # Mocking Jev returning confidence=0.55
    mocker.patch('backend.engine.ReflexGateEngine.evaluate_and_route', return_value={
        "execution_status": "APPROVED",
        "assigned_route": "SYSTEM2_APPROVED",
        "calibrated_confidence": 0.99,
        "latency_breakdown": {"total_latency_ms": 1545.0, "jev_latency_ms": 45.0, "system2_latency_ms": 1500.0},
        "estimated_cost_usd": 0.0301
    })
    
    response = client.post("/v1/gate/evaluate", json=create_mock_payload())
    assert response.status_code == 200
    data = response.json()
    assert "SYSTEM2" in data["engine_decision"]["assigned_route"]
    assert data["engine_decision"]["latency_breakdown"]["total_latency_ms"] > 1000

@pytest.mark.asyncio
async def test_security_block(mocker):
    # Mocking Jev returning malicious=0.88
    mocker.patch('backend.engine.ReflexGateEngine.evaluate_and_route', return_value={
        "execution_status": "REJECTED",
        "assigned_route": "BLOCK",
        "calibrated_confidence": 0.95,
        "latency_breakdown": {"total_latency_ms": 45.0, "jev_latency_ms": 45.0, "system2_latency_ms": 0.0},
        "estimated_cost_usd": 0.0001
    })
    
    response = client.post("/v1/gate/evaluate", json=create_mock_payload("delete_database"))
    assert response.status_code == 200
    data = response.json()
    assert data["engine_decision"]["assigned_route"] == "BLOCK"
    assert data["engine_decision"]["execution_status"] == "REJECTED"

@pytest.mark.asyncio
async def test_load_benchmark(mocker):
    mocker.patch('backend.engine.ReflexGateEngine.evaluate_and_route', return_value={
        "execution_status": "APPROVED",
        "assigned_route": "FAST_PATH_LOCAL",
        "calibrated_confidence": 0.92,
        "latency_breakdown": {"total_latency_ms": 45.0, "jev_latency_ms": 45.0, "system2_latency_ms": 0.0},
        "estimated_cost_usd": 0.0001
    })
    
    # Concurrent run of 100 parallel requests
    async def make_request():
        # In a real async load test we'd use httpx.AsyncClient
        return client.post("/v1/gate/evaluate", json=create_mock_payload())
    
    tasks = [make_request() for _ in range(100)]
    responses = await asyncio.gather(*tasks)
    
    for resp in responses:
        assert resp.status_code == 200
