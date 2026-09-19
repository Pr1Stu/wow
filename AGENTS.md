# Repository instructions

## Project

WOW is a Python 3.13 agent runtime for Project ZhiXUE and bounded single-round tasks. Read `README.md` for setup and `docs/architecture.md` before changing runtime behavior or service boundaries.

## Layout

- `src/wow/api/`: FastAPI routes, request models, and SSE events.
- `src/wow/agent/`: lightweight orchestration and model gateway integration.
- `src/wow/tools/`: fixed tool registry, policy, and idempotency helpers.
- `src/wow/adapters/` and `src/wow/full_agent/`: integration boundaries.
- `src/wow/db/` and `migrations/`: independent runtime database and migrations.
- `profiles/*.yaml` and `prompts/*.md`: run configuration, resolved and hashed at run start.
- `tests/unit/`: unit tests; live model tests use the `live` marker.

## Development and verification

- Install dependencies with `uv sync --dev` when `uv` is available.
- Run the service with `uv run uvicorn wow.api.app:create_app --factory --reload`.
- Run unit tests with `uv run pytest tests/unit`.
- Run lint and type checks with `uv run ruff check .` and `uv run pyright`.
- Run `uv run pytest -m live` only when a real AI gateway is configured and live testing is intended.

## Engineering expectations

- Keep the tool universe fixed in code; profiles may expose only static subsets and must select models deterministically.
- Preserve the `ZhixueAdapter` boundary. ZhiXUE owns business data, long-term memory, and business-side idempotency; WOW owns its runtime state.
- Classify tool side effects as `read`, `low_risk_write`, or `high_risk_write`. Preserve approval handling for high-risk operations and stable idempotency keys for side effects.
- Keep model-provider credentials and fallback decisions in the AI gateway. Use the OpenAI-compatible Chat Completions protocol at that boundary.
- Treat the items marked TBD in `docs/architecture.md` as open design questions; do not invent settled behavior for them.
- Add or update focused tests for behavior changes. Before finishing, run the relevant checks and report any checks that could not run.
