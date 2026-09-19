from __future__ import annotations

from datetime import date
from typing import Protocol

from wow.contracts import Deadline, MemoryCandidate, ScheduleItem, TaskDraft, TaskRecord, UserContext


class ZhixueAdapter(Protocol):
    async def get_user_context(self, user_id: str) -> UserContext: ...

    async def get_schedule(self, user_id: str, on_date: date) -> list[ScheduleItem]: ...

    async def get_deadlines(self, user_id: str) -> list[Deadline]: ...

    async def create_task(
        self, user_id: str, task: TaskDraft, *, idempotency_key: str
    ) -> TaskRecord: ...

    async def submit_memory_candidates(
        self, user_id: str, candidates: list[MemoryCandidate]
    ) -> None: ...
