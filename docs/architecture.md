┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                CLIENT / AGENT SWARM LAYER                               │
│  (LangChain / CrewAI / AutoGen / Browser-Use / Custom Python State Machines)           │
└──────────────────────────────────────────┬──────────────────────────────────────────────┘
                                           │ HTTP/gRPC (Action Payload State)
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 REFLEXGATE INGRESS PROXY                                │
│  - FastAPI / Cloudflare Workers API Gateway                                            │
│  - API Key Auth, Rate Limiting, Request Sanitization                                    │
└──────────────────────────────────────────┬──────────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                             PARALLEL JEV EVALUATION ENGINE                              │
│  - Invokes `TypeSafeModel('typesafe:jev-latest')`                                       │
│  - Concurrent Pass: Noul (Malicious?), Score (Risk 1-5), Choice (Execution Route)        │
└──────────────────────────────────────────┬──────────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           RLCD CALIBRATION & THRESHOLD ROUTER                           │
│  - Computes Joint Confidence $C_{joint} = C_{choice} \times C_{score}$                  │
│  - Applies Decision Matrix (Fast-Path vs. System 2 Escalation vs. Block)               │
└──────────────────────┬───────────────────────────────────────────┬──────────────────────┘
                       │                                           │
       (Escalation Triggered)                             (Decision Logging)
                       │                                           │
                       ▼                                           ▼
┌───────────────────────────────────────┐       ┌─────────────────────────────────────────┐
│    SYSTEM 2 REASONING FALLBACK        │       │       ANALYTICS & AUDIT STORE           │
│  - GPT-4o / Claude 3.5 Sonnet         │       │  - PostgreSQL / ClickHouse              │
│  - Generates CoT reasoning when       │       │  - Ingests real-time metrics, costs,    │
│    Jev signals uncertainty.           │       │    and latency logs.                    │
└───────────────────────────────────────┘       └────────────────────┬────────────────────┘
                                                                     │
                                                                     ▼
                                                ┌─────────────────────────────────────────┐
                                                │      NEXT.JS 15 CONTROL DASHBOARD       │
                                                │  - Real-time SLA monitoring             │
                                                │  - Dynamic threshold tuning             │
                                                └─────────────────────────────────────────┘