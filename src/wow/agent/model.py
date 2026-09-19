from __future__ import annotations

import httpx
from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from wow.config import Settings


class GatewayModelFactory:
    """Build OpenAI Chat Completions models against WOW's self-hosted gateway."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        verify: bool | str = True
        if settings.ai_gateway_ca_bundle is not None:
            verify = str(settings.ai_gateway_ca_bundle)
        self.http_client = httpx.AsyncClient(
            timeout=60,
            verify=verify,
            cert=settings.gateway_client_cert,
        )
        api_key = (
            settings.ai_gateway_api_key.get_secret_value()
            if settings.ai_gateway_api_key is not None
            else "mtls-authenticated"
        )
        self.openai_client = AsyncOpenAI(
            base_url=settings.ai_gateway_base_url,
            api_key=api_key,
            max_retries=0,
            http_client=self.http_client,
        )
        self.provider = OpenAIProvider(openai_client=self.openai_client)

    def create(self, model_name: str) -> OpenAIChatModel:
        return OpenAIChatModel(model_name, provider=self.provider)

    async def aclose(self) -> None:
        await self.openai_client.close()
