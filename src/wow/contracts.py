from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

CONTRACT_VERSION = "v1"


class AuthContext(BaseModel):
    """Authentication material resolved by the ZhiXUE integration layer."""

    user_id: str
    subject: str | None = None
    claims: dict[str, Any] = Field(default_factory=dict)


class UserContext(BaseModel):
    user_id: str
    facts: dict[str, Any] = Field(default_factory=dict)
    preferences: dict[str, Any] = Field(default_factory=dict)
    academic_state: dict[str, Any] = Field(default_factory=dict)


class ScheduleItem(BaseModel):
    id: str
    title: str
    starts_at: datetime
    ends_at: datetime
    location: str | None = None


class Deadline(BaseModel):
    id: str
    title: str
    due_at: datetime
    course_id: str | None = None


class TaskDraft(BaseModel):
    title: str
    due_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskRecord(TaskDraft):
    id: str


class MemoryCandidate(BaseModel):
    kind: str
    content: dict[str, Any]
    confidence: float = Field(ge=0, le=1)
    source_run_id: str


class EscalationRequest(BaseModel):
    reason: str
    required_capabilities: list[str] = Field(default_factory=list)


class UserResponse(BaseModel):
    type: Literal["text"] = "text"
    text: str


class AgentStateDelta(BaseModel):
    memory_candidates: list[MemoryCandidate] = Field(default_factory=list)
    escalation_requests: list[EscalationRequest] = Field(default_factory=list)
    suggested_actions: list[dict[str, Any]] = Field(default_factory=list)
    context_updates: dict[str, Any] = Field(default_factory=dict)


class AgentRunResult(BaseModel):
    run_id: str
    response: UserResponse
    state_delta: AgentStateDelta
