# Low-Level Design (LLD): ReflexGate AI Enterprise

## 1. Interface Specifications

### `POST /v1/gate/evaluate`
**Request Payload:**
```json
{
  "agent_id": "string",
  "session_id": "string",
  "user_role": "string",
  "proposed_tool": "string",
  "tool_arguments": {"key": "value"},
  "environment_context": "string"
}
```
**Response Payload:**
```json
{
  "status": "success",
  "evaluation": {
    "is_malicious_or_jailbreak": 0.05,
    "risk_score": 1,
    "recommended_route": "ALLOW_FAST_PATH"
  },
  "engine_decision": {
    "execution_status": "APPROVED",
    "assigned_route": "FAST_PATH_LOCAL",
    "calibrated_confidence": 0.95,
    "latency_breakdown": {
        "jev_latency_ms": 42.1,
        "system2_latency_ms": 0.0,
        "total_latency_ms": 42.1
    },
    "estimated_cost_usd": 0.0001
  }
}
```

## 2. Component Implementation Details

### 2.1 Abstract Evaluator Interface (`evaluator.py`)
To remove hardcoded mock logic, we introduce an abstract base class `BaseEvaluator` that enforces the implementation of `async def evaluate(state: AgentActionState) -> JevReflexEvaluation`.
- **LocalONNXEvaluator (Tier 1):** Uses ONNX Runtime for CPU/GPU-optimized inference of a BERT/DistilRoBERTa classification model. This entirely replaces the mock `jev_agent`.
- **System2Evaluator (Tier 2):** Implements asynchronous HTTP calls to OpenAI using `httpx` and `pydantic-ai` models.

### 2.2 Database Layer Optimization (`database.py`)
- **Connection Pooling:** `asyncpg` uses a configured connection pool (`min_size=10`, `max_size=100`) to handle high concurrency.
- **Indexing:** B-Tree indices applied to `agent_id`, `final_execution_route`, and `created_at` in PostgreSQL to heavily optimize querying for the Control Plane analytics.

### 2.3 System 2 Fallback Implementation (`system2.py`)
- Implements exponential backoff and retry logic using the `tenacity` library to handle OpenAI API rate limits gracefully.
- Prompts are dynamically and strictly constructed, injecting the `proposed_tool` and `tool_arguments` into a structured evaluation chain.

## 3. Real-Time Frontend Integration
- **State Management:** The Next.js frontend transitions from static dummy arrays to using `SWR` (Stale-While-Revalidate) to poll the `GET /v1/analytics/stats` endpoint every 3 seconds.
- **Log Stream Optimization:** To handle thousands of logs efficiently without crushing the browser DOM, the Live Audit Stream implements UI virtualization using `react-window` or `@tanstack/react-virtual`.
