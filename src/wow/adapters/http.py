from __future__ import annotations

from datetime import date

import httpx

from wow.contracts import Deadline, MemoryCandidate, ScheduleItem, TaskDraft, TaskRecord, UserContext


class HttpZhixueAdapter:
    """Draft v1 HTTP implementation of the independently versioned ZhiXUE contract."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get_user_context(self, user_id: str) -> UserContext:
        response = await self.client.get(f"/internal/wow/v1/users/{user_id}/context")
        response.raise_for_status()
        return UserContext.model_validate(response.json())

    async def get_schedule(self, user_id: str, on_date: date) -> list[ScheduleItem]:
        response = await self.client.get(
            f"/internal/wow/v1/users/{user_id}/schedule", params={"date": on_date.isoformat()}
        )
        response.raise_for_status()
        return [ScheduleItem.model_validate(item) for item in response.json()]

    async def get_deadlines(self, user_id: str) -> list[Deadline]:
        response = await self.client.get(f"/internal/wow/v1/users/{user_id}/deadlines")
        response.raise_for_status()
        return [Deadline.model_validate(item) for item in response.json()]

    async def create_task(
        self, user_id: str, task: TaskDraft, *, idempotency_key: str
    ) -> TaskRecord:
        response = await self.client.post(
            f"/internal/wow/v1/users/{user_id}/tasks",
            json=task.model_dump(mode="json"),
            headers={"Idempotency-Key": idempotency_key},
        )
        response.raise_for_status()
        return TaskRecord.model_validate(response.json())

    async def submit_memory_candidates(
        self, user_id: str, candidates: list[MemoryCandidate]
    ) -> None:
        response = await self.client.post(
            f"/internal/wow/v1/users/{user_id}/memory-candidates",
            json=[candidate.model_dump(mode="json") for candidate in candidates],
        )
        response.raise_for_status()
