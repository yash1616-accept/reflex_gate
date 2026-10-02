from reflexgate import ReflexGuard

print("🛡️ Initializing ReflexGate SDK Plugin...")
# Initialize the guard pointing to the local Docker gateway
guard = ReflexGuard(endpoint="http://localhost:8000")

print("\n🤖 Agent attempts to fetch a user profile...")
decision1 = guard.evaluate(
    agent_id="my-langchain-agent",
    proposed_tool="fetch_user",
    arguments={"user_id": 123}
)

if decision1.is_approved:
    print(f"✅ ACTION ALLOWED! ({decision1.reason}) - Took {decision1.latency_ms}ms")
else:
    print(f"🚫 ACTION BLOCKED! ({decision1.reason}) - Took {decision1.latency_ms}ms")


print("\n🤖 Agent attempts to drop a database table (Malicious!)...")
decision2 = guard.evaluate(
    agent_id="my-langchain-agent",
    proposed_tool="execute_sql",
    arguments={"query": "DROP TABLE users;"}
)

if decision2.is_approved:
    print(f"✅ ACTION ALLOWED! ({decision2.reason}) - Took {decision2.latency_ms}ms")
else:
    print(f"🚫 ACTION BLOCKED! ({decision2.reason}) - Took {decision2.latency_ms}ms")
