from __future__ import annotations

import hashlib
from datetime import timedelta
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator


class ContextPolicy(BaseModel):
    compact_threshold: int = 32_000
    recent_raw_budget: int = 12_000
    summary_budget: int = 4_000


class RunLimits(BaseModel):
    max_steps: int = Field(default=6, ge=1)
    max_tool_calls: int = Field(default=8, ge=0)
    max_escalations: int = Field(default=1, ge=0)


class AgentProfile(BaseModel):
    name: str
    version: int = Field(ge=1)
    model: str
    prompt: str
    tools: list[str] = Field(default_factory=list)
    session_ttl: str = "2h"
    context: ContextPolicy = Field(default_factory=ContextPolicy)
    limits: RunLimits = Field(default_factory=RunLimits)

    @field_validator("tools")
    @classmethod
    def unique_tools(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("profile tools must be unique")
        return value

    def ttl(self) -> timedelta:
        raw = self.session_ttl.strip().lower()
        if raw.endswith("m"):
            return timedelta(minutes=int(raw[:-1]))
        if raw.endswith("h"):
            return timedelta(hours=int(raw[:-1]))
        if raw.endswith("d"):
            return timedelta(days=int(raw[:-1]))
        raise ValueError(f"unsupported session_ttl: {self.session_ttl!r}")


class ResolvedProfile(BaseModel):
    profile: AgentProfile
    instructions: str
    profile_hash: str
    prompt_hash: str


class ProfileStore:
    def __init__(self, profiles_dir: Path, prompts_dir: Path) -> None:
        self.profiles_dir = profiles_dir
        self.prompts_dir = prompts_dir

    def names(self) -> list[str]:
        return sorted(path.stem for path in self.profiles_dir.glob("*.yaml"))

    def load(self, name: str) -> ResolvedProfile:
        profile_path = self.profiles_dir / f"{name}.yaml"
        raw_text = profile_path.read_text(encoding="utf-8")
        raw: dict[str, Any] = yaml.safe_load(raw_text)
        raw.setdefault("name", name)
        profile = AgentProfile.model_validate(raw)
        if profile.name != name:
            raise ValueError(f"profile name mismatch: requested={name!r}, config={profile.name!r}")

        prompt_path = self.prompts_dir / profile.prompt
        instructions = prompt_path.read_text(encoding="utf-8").strip()
        prompt_hash = hashlib.sha256(instructions.encode()).hexdigest()
        normalized = profile.model_dump_json(exclude_none=False)
        profile_hash = hashlib.sha256(normalized.encode()).hexdigest()
        return ResolvedProfile(
            profile=profile,
            instructions=instructions,
            profile_hash=profile_hash,
            prompt_hash=prompt_hash,
        )
