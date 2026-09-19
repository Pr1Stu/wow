from __future__ import annotations

from datetime import date, datetime

from pydantic_ai import RunContext

from wow.agent.deps import WowDeps
from wow.contracts import EscalationRequest, TaskDraft
from wow.tools.idempotency import make_idempotency_key
from wow.tools.policy import ToolExecutionPolicy, execute_with_policy


async def get_user_context(ctx: RunContext[WowDeps]) -> dict[str, object]:
    """Get the current structured ZhiXUE user context."""
    policy: ToolExecutionPolicy = getattr(get_user_context, "_wow_policy")
    result = await execute_with_policy(
        policy, lambda: ctx.deps.zhixue.get_user_context(ctx.deps.user_id)
    )
    return result.model_dump(mode="json")


async def get_schedule(ctx: RunContext[WowDeps], on_date: date) -> list[dict[str, object]]:
    """Get the user's schedule for a specific date."""
    policy: ToolExecutionPolicy = getattr(get_schedule, "_wow_policy")
    result = await execute_with_policy(
        policy, lambda: ctx.deps.zhixue.get_schedule(ctx.deps.user_id, on_date)
    )
    return [item.model_dump(mode="json") for item in result]


async def get_deadlines(ctx: RunContext[WowDeps]) -> list[dict[str, object]]:
    """Get the user's current academic deadlines."""
    policy: ToolExecutionPolicy = getattr(get_deadlines, "_wow_policy")
    result = await execute_with_policy(
        policy, lambda: ctx.deps.zhixue.get_deadlines(ctx.deps.user_id)
    )
    return [item.model_dump(mode="json") for item in result]


async def create_task(
    ctx: RunContext[WowDeps], title: str, due_at: datetime | None = None
) -> dict[str, object]:
    """Create a ZhiXUE task. This is a low-risk, idempotent write."""
    if not ctx.run_id or not ctx.tool_call_id:
        raise RuntimeError("run_id and tool_call_id are required for side-effecting tools")
    policy: ToolExecutionPolicy = getattr(create_task, "_wow_policy")
    key = make_idempotency_key(ctx.run_id, ctx.tool_call_id, "create_task")
    draft = TaskDraft(title=title, due_at=due_at)
    result = await execute_with_policy(
        policy,
        lambda: ctx.deps.zhixue.create_task(
            ctx.deps.user_id, draft, idempotency_key=key
        ),
    )
    return result.model_dump(mode="json")


async def request_escalation(
    ctx: RunContext[WowDeps], reason: str, required_capabilities: list[str]
) -> dict[str, object]:
    """Request transfer to the full-featured agent. WOW policy decides whether it is granted."""
    request = EscalationRequest(reason=reason, required_capabilities=required_capabilities)
    ctx.deps.state.escalation_requests.append(request)
    return {
        "status": "requested",
        "note": "The deterministic WOW policy layer will decide after this lightweight run.",
    }
