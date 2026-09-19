from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WOW_", env_file=".env", extra="ignore")

    env: str = "development"
    database_url: str = "postgresql+asyncpg://wow:wow@localhost:5432/wow"

    ai_gateway_base_url: str = "https://ai.example.com/v1"
    ai_gateway_api_key: SecretStr | None = None
    ai_gateway_mtls_cert: Path | None = None
    ai_gateway_mtls_key: Path | None = None
    ai_gateway_ca_bundle: Path | None = None

    zhixue_base_url: str = "http://localhost:8080"
    zhixue_service_token: SecretStr | None = None

    profiles_dir: Path = Path("profiles")
    prompts_dir: Path = Path("prompts")

    dev_auth: bool = False

    @property
    def gateway_client_cert(self) -> tuple[str, str] | None:
        if self.ai_gateway_mtls_cert is None and self.ai_gateway_mtls_key is None:
            return None
        if self.ai_gateway_mtls_cert is None or self.ai_gateway_mtls_key is None:
            raise ValueError("both WOW_AI_GATEWAY_MTLS_CERT and WOW_AI_GATEWAY_MTLS_KEY are required")
        return (str(self.ai_gateway_mtls_cert), str(self.ai_gateway_mtls_key))


@lru_cache
def get_settings() -> Settings:
    return Settings()
