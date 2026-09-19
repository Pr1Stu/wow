from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from enum import StrEnum
from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class RiskLevel(StrEnum):
    READ = "read"
    LOW_RISK_WRITE = "low_risk_write"
    HIGH_RISK_WRITE = "high_risk_write"


class ToolExecutionPolicy(BaseModel):
    risk_level: RiskLevel
    requires_confirmation: bool = False
    undoable: bool = False
    timeout_seconds: float = Field(default=5, gt=0)
    max_retries: int = Field(default=0, ge=0)


async def execute_with_policy(policy: ToolExecutionPolicy, operation: Callable[[], Awaitable[T]]) -> T:
    last_error: Exception | None = None
    for attempt in range(policy.max_retries + 1):
        try:
            async with asyncio.timeout(policy.timeout_seconds):
                return await operation()
        except Exception as exc:
            last_error = exc
            if attempt >= policy.max_retries:
                raise
    assert last_error is not None
    raise last_error
