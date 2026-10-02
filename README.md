<div align="center">
  <img src="https://via.placeholder.com/150x150.png?text=ReflexGate" alt="ReflexGate Logo" width="120" />
  <h1>ReflexGate 🛡️</h1>
  <p><strong>The Enterprise-Grade Safety Firewall for Autonomous AI Agents</strong></p>

  [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
  [![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)](https://fastapi.tiangolo.com)
  [![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs)](https://nextjs.org)
</div>

<br />

## 🚀 What is ReflexGate?

As AI agents move from chat interfaces to **autonomous task execution** (executing code, querying databases, handling money), the risk of rogue actions, prompt injections, and cascading failures skyrockets.

**ReflexGate is a blazingly fast, standalone safety gateway.** It sits between your AI Agents (LangChain, CrewAI, AutoGen) and your infrastructure. Every tool call your agent attempts must pass through ReflexGate.

### Key Features
- ⚡ **Zero-Latency Fast Path:** Safe actions are approved in `<50ms` using local SLMs (Small Language Models).
- 🧠 **System 2 Escalation:** Ambiguous or high-risk intents are routed to a frontier model (GPT-4o/Claude 3.5) for deep semantic reasoning.
- 📊 **Real-Time Next.js Dashboard:** Monitor live telemetry, view agent escalation rates, and track money saved by preventing rogue API calls.
- 🐘 **PostgreSQL Audit Log:** 100% of agent activity is durably logged asynchronously for compliance and forensic analysis.

---

## 🏗️ Architecture

```mermaid
graph TD
    A[Autonomous Agent (CrewAI/LangChain)] -->|Proposed Tool Call| B(ReflexGate Ingress - Port 8000)
    B --> C{Tier 1: Local SLM}
    C -->|< 0.20 Risk| D[Fast Path APPROVED <50ms]
    C -->|> 0.65 Risk| E[BLOCKED]
    C -->|Ambiguous| F{Tier 2: System 2 GPT-4o}
    F -->|Safe Intent| D
    F -->|Malicious Intent| E
    B -.->|Async Fire-and-Forget| G[(PostgreSQL Audit Log)]
    G --> H[Next.js Analytics Dashboard - Port 3001]
```

---

## 💻 Quick Start (Docker)

You can launch the entire stack (PostgreSQL, FastAPI Gateway, Next.js Control Plane) with a single command.

```bash
# Clone the repository
git clone https://github.com/yourusername/reflexgate.git
cd reflexgate

# Launch the Enterprise Cluster
docker-compose up -d --build
```

### Accessing the System
- **API Gateway:** `http://localhost:8000`
- **Analytics Dashboard:** `http://localhost:3001`

---

## 🔌 Using the Python Plugin (SDK)

ReflexGate is designed to be easily plugged into existing systems. Install our lightweight SDK:

```bash
pip install reflexgate-sdk
```

Wrap your agent's execution logic:

```python
from reflexgate import ReflexGuard

guard = ReflexGuard(endpoint="http://localhost:8000")

# Before your agent runs a tool:
decision = guard.evaluate(
    agent_id="finance-bot-v2",
    proposed_tool="refund_transaction",
    arguments={"tx_id": "9999", "amount": 500.00},
    context="Customer requested refund"
)

if decision.is_approved:
    execute_tool()
else:
    alert_security_team(decision.reason)
```

---

## 🧑‍💻 Running the Live Demo

Want to see it in action or show it to stakeholders? We included a Live Traffic Simulator.
With the Docker cluster running, open the dashboard at `http://localhost:3001/dashboard`, then run:

```bash
python demo_client.py
```
Watch the live charts and audit logs populate in real-time as the engine evaluates 15 simultaneous agents!

---

## 📜 License

ReflexGate is licensed under the Apache 2.0 License. See `LICENSE` for more details. For Enterprise support and SLAs, please contact us.
