from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import httpx
from fastapi import FastAPI

from wow.adapters.http import HttpZhixueAdapter
from wow.agent.factory import AgentFactory
from wow.agent.model import GatewayModelFactory
from wow.agent.runtime import AgentRuntime
from wow.api.routes import router
from wow.config import get_settings
from wow.profiles import ProfileStore


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    headers: dict[str, str] = {}
    if settings.zhixue_service_token is not None:
        headers["Authorization"] = f"Bearer {settings.zhixue_service_token.get_secret_value()}"
    zhixue_http = httpx.AsyncClient(
        base_url=settings.zhixue_base_url,
        headers=headers,
        timeout=15,
    )
    models = GatewayModelFactory(settings)
    profiles = ProfileStore(settings.profiles_dir, settings.prompts_dir)
    runtime = AgentRuntime(
        profiles=profiles,
        agents=AgentFactory(models),
        zhixue=HttpZhixueAdapter(zhixue_http),
    )
    app.state.settings = settings
    app.state.profiles = profiles
    app.state.runtime = runtime
    try:
        yield
    finally:
        await models.aclose()
        await zhixue_http.aclose()


def create_app() -> FastAPI:
    app = FastAPI(title="WOW", version="0.1.0", lifespan=lifespan)
    app.include_router(router)
    return app
