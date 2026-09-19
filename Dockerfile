FROM python:3.13-slim AS runtime

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml README.md ./
COPY src ./src
COPY profiles ./profiles
COPY prompts ./prompts
RUN uv sync --no-dev --no-editable

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

CMD ["uvicorn", "wow.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
