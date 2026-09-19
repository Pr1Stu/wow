from __future__ import annotations

from typing import Literal, Protocol

from pydantic import BaseModel, Field


class FullAgentRequest(BaseModel):
    user_id: str
    source_run_id: str
    task: str
    required_capabilities: list[str] = Field(default_factory=list)
    context_ref: str | None = None


class FullAgentStatus(BaseModel):
    task_id: str
    state: Literal["queued", "running", "completed", "failed", "cancelled"]
    result_ref: str | None = None
    error: str | None = None


class FullAgentProvider(Protocol):
    async def submit(self, task: FullAgentRequest) -> str: ...
    async def status(self, task_id: str) -> FullAgentStatus: ...
    async def cancel(self, task_id: str) -> None: ...
