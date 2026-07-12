# WorkflowGym Phase 5: Rule-Based Agent Runner

Phase 5 implements the first agent.

The implementation lives in:

```text
backend/app/agents/rule_based_agent.py
```

## What The Agent Does

The rule-based agent loads a scenario and calls tools in this order:

1. `get_customer`
2. `get_invoice`
3. `get_usage_events`
4. `get_contract_terms`
5. `compare_usage_to_invoice`

After each tool call, it stores an `AgentStep`.

## Why This Agent Is Rule-Based

This project will eventually support LLM-powered agents.

But the first milestone intentionally avoids LLMs so you can prove the simulator works:

- Tool calls work.
- Traces are stored.
- Final answers are structured.
- Evaluation works.

Once this deterministic runner works, replacing it with an LLM runner becomes much safer.

## Final Answer Shape

The agent produces:

```json
{
  "decision": "invoice_incorrect",
  "cause": "duplicate_usage_events",
  "explanation": "...",
  "evidence": []
}
```

This is stored on `AgentRun.final_answer`.

## What You Should Understand

- `AgentRun` represents one full attempt.
- `AgentStep` represents one tool call.
- The trace is stored while the agent runs, not reconstructed later.
- The final answer is structured JSON.
- The rule-based agent is a scaffold for a future LLM agent.
