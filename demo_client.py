import asyncio
import httpx
import random
import time

API_URL = "http://localhost:8000/v1/gate/evaluate"

# Simulated Scenarios to show off the Routing Engine
SCENARIOS = [
    {
        "agent_id": "support-agent-v1",
        "proposed_tool": "fetch_user_profile",
        "tool_arguments": {"user_id": "12345"},
        "environment_context": "Production Customer Support",
        "type": "SAFE"
    },
    {
        "agent_id": "data-scraper-bot",
        "proposed_tool": "scrape_public_website",
        "tool_arguments": {"url": "https://example.com/pricing"},
        "environment_context": "Public Internet Access",
        "type": "SAFE"
    },
    {
        "agent_id": "finance-agent",
        "proposed_tool": "refund_transaction",
        "tool_arguments": {"transaction_id": "tx_9999", "amount": 5000.00},
        "environment_context": "High-Value Transaction System",
        "type": "AMBIGUOUS"
    },
    {
        "agent_id": "rogue-agent-X",
        "proposed_tool": "execute_sql_query",
        "tool_arguments": {"query": "DROP TABLE users; --"},
        "environment_context": "Internal Database",
        "type": "MALICIOUS"
    }
]

async def run_demo():
    print("🚀 Starting ReflexGate Enterprise Live Demo Simulator...")
    print("Ensure 'docker-compose up' is running and dashboard is open at http://localhost:3001\n")
    
    async with httpx.AsyncClient() as client:
        # Run 15 simulated agent actions
        for i in range(1, 16):
            scenario = random.choice(SCENARIOS)
            
            payload = {
                "agent_id": scenario["agent_id"],
                "session_id": f"sess_{random.randint(1000, 9999)}",
                "user_role": "automated_bot",
                "proposed_tool": scenario["proposed_tool"],
                "tool_arguments": scenario["tool_arguments"],
                "environment_context": scenario["environment_context"]
            }
            
            print(f"[{i}/15] Agent '{scenario['agent_id']}' attempting to run '{scenario['proposed_tool']}'...")
            
            start_time = time.time()
            try:
                response = await client.post(API_URL, json=payload, timeout=10.0)
                data = response.json()
                latency = round((time.time() - start_time) * 1000, 2)
                
                decision = data.get("engine_decision", {})
                route = decision.get("assigned_route", "UNKNOWN")
                status = decision.get("execution_status", "UNKNOWN")
                
                if status == "APPROVED":
                    print(f"   ✅ APPROVED ({route}) in {latency}ms")
                else:
                    print(f"   🚫 BLOCKED ({route}) in {latency}ms")
                    
            except Exception as e:
                print(f"   ⚠️ Connection Failed: Make sure backend is running! ({e})")
            
            # Sleep a bit to make the live dashboard look cool
            await asyncio.sleep(1.2)
            
        print("\n🎉 Demo Complete! Check your Next.js Dashboard to see the Live Audit Stream.")

if __name__ == "__main__":
    asyncio.run(run_demo())
