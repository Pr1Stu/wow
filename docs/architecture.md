# Architecture baseline

WOW is an independent service and repository. It owns lightweight agent orchestration and runtime state, not ZhiXUE business data or long-term user memory.

## Core path

```text
Mobile -> ZhiXUE auth context -> WOW -> AI Gateway -> model provider
                                  |
                                  | -> ZhixueAdapter -> ZhiXUE internal API
                                  \ -> escalation policy -> FullAgentProvider -> Cloudflare full agent
```

The AI wire protocol is OpenAI-compatible Chat Completions. Provider credentials and provider fallback belong to the gateway. WOW is designed for mature machine-to-machine authentication to the gateway, with mTLS as the baseline direction.

## Runtime rules

- Pydantic AI provides lightweight orchestration.
- Tool universe is fixed in code; profiles expose only static subsets.
- Profile selects model deterministically.
- Tool side effects are classified as `read`, `low_risk_write`, or `high_risk_write`.
- High-risk tools require approval; approval persistence remains TBD.
- Tool timeout/retry policy is per-tool.
- Side-effect calls carry stable idempotency keys; ZhiXUE enforces business-side idempotency.
- The model may request escalation, but deterministic WOW policy decides whether it is granted.
- Long-term memory is returned to ZhiXUE as candidates; WOW does not own it.
- Context compaction starts at 32k tokens and uses a separately configured cheap summarizer model.
- Same-session runs are serialized; explicit interrupt requests use best-effort cancellation and never imply rollback.

## Transport and persistence

- FastAPI, REST commands, SSE events.
- Semantic SSE events are persisted/replayable; token deltas are ephemeral.
- WOW uses an independent PostgreSQL database through SQLAlchemy async/asyncpg and Alembic.
- Chat-history ownership stays in the ZhiXUE main project; WOW session messages are transient runtime data.

## Explicit TBDs

- Mobile -> WOW authentication details (follow ZhiXUE main project).
- High-risk approval-state ownership/persistence.
- WOW -> Cloudflare full-agent ingress/queue transport.
- Run queue persistence.
- Multi-session policy per user.
- Cross-run retention of tool results.
- Whether/how `state_delta` fields are automatically written back.
