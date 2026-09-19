# wow

A super-lightweight but full-featured agent runtime built for Project ZhiXUE and bounded single-round tasks.

## Status

WOW is in bootstrap development. The first implementation intentionally keeps orchestration small:

- FastAPI service boundary
- Pydantic AI lightweight orchestration
- OpenAI-compatible Chat Completions through a configurable self-hosted gateway
- fixed, profile-scoped tools
- deterministic tool risk / timeout / retry policy
- independent PostgreSQL runtime state
- `ZhixueAdapter` contract instead of direct access to the ZhiXUE database
- `FullAgentProvider` boundary for escalation to the Cloudflare-based full agent

The full-agent queue/ingress transport, high-risk approval persistence, run-queue persistence, and several session details remain deliberately TBD.

## Development

```bash
uv sync --dev
cp .env.example .env
uv run uvicorn wow.api.app:create_app --factory --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/healthz
```

Run unit tests:

```bash
uv run pytest tests/unit
```

Live model tests are isolated behind the `live` marker:

```bash
uv run pytest -m live
```

## Configuration

Profiles live in `profiles/*.yaml`; prompts live in `prompts/*.md`. A run resolves and hashes its profile/prompt at run start so a single run never changes configuration mid-flight.
