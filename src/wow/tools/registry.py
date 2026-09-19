from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from pydantic_ai import Tool

from wow.tools.core import create_task, get_deadlines, get_schedule, get_user_context, request_escalation
from wow.tools.policy import RiskLevel, ToolExecutionPolicy


@dataclass(frozen=True)
class RegisteredTool:
    function: Callable[..., Any]
    policy: ToolExecutionPolicy

    def as_pydantic_tool(self) -> Tool[Any]:
        setattr(self.function, "_wow_policy", self.policy)
        return Tool(
            self.function,
            takes_ctx=True,
            requires_approval=self.policy.requires_confirmation,
            retries=0,
        )


TOOL_REGISTRY: dict[str, RegisteredTool] = {
    "get_user_context": RegisteredTool(
        get_user_context,
        ToolExecutionPolicy(risk_level=RiskLevel.READ, timeout_seconds=3, max_retries=1),
    ),
    "get_schedule": RegisteredTool(
        get_schedule,
        ToolExecutionPolicy(risk_level=RiskLevel.READ, timeout_seconds=3, max_retries=1),
    ),
    "get_deadlines": RegisteredTool(
        get_deadlines,
        ToolExecutionPolicy(risk_level=RiskLevel.READ, timeout_seconds=3, max_retries=1),
    ),
    "create_task": RegisteredTool(
        create_task,
        ToolExecutionPolicy(
            risk_level=RiskLevel.LOW_RISK_WRITE,
            timeout_seconds=5,
            max_retries=1,
            undoable=True,
        ),
    ),
    "request_escalation": RegisteredTool(
        request_escalation,
        ToolExecutionPolicy(risk_level=RiskLevel.READ, timeout_seconds=1, max_retries=0),
    ),
}


def tools_for_profile(names: list[str]) -> list[Tool[Any]]:
    unknown = sorted(set(names) - TOOL_REGISTRY.keys())
    if unknown:
        raise ValueError(f"unknown tools in profile: {unknown}")
    return [TOOL_REGISTRY[name].as_pydantic_tool() for name in names]
