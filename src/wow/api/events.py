from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AgentEventType(StrEnum):
    TOKEN_DELTA = "token_delta"
    RUN_STARTED = "run_started"
    TOOL_STARTED = "tool_started"
    TOOL_FINISHED = "tool_finished"
    APPROVAL_REQUIRED = "approval_required"
    ESCALATION_REQUESTED = "escalation_requested"
    ESCALATION_ACCEPTED = "escalation_accepted"
    MESSAGE_COMPLETED = "message_completed"
    FAILED = "failed"


PERSISTED_EVENT_TYPES = frozenset(
    event
    for event in AgentEventType
    if event is not AgentEventType.TOKEN_DELTA
)


class AgentEvent(BaseModel):
    event_id: str
    run_id: str
    sequence: int = Field(ge=0)
    type: AgentEventType
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def persisted(self) -> bool:
        return self.type in PERSISTED_EVENT_TYPES
