from __future__ import annotations

from dataclasses import dataclass, field

from wow.adapters.base import ZhixueAdapter
from wow.contracts import AgentStateDelta, EscalationRequest, MemoryCandidate
from wow.full_agent.base import FullAgentProvider


@dataclass
class RunState:
    memory_candidates: list[MemoryCandidate] = field(default_factory=list)
    escalation_requests: list[EscalationRequest] = field(default_factory=list)
    suggested_actions: list[dict[str, object]] = field(default_factory=list)
    context_updates: dict[str, object] = field(default_factory=dict)

    def to_delta(self) -> AgentStateDelta:
        return AgentStateDelta(
            memory_candidates=self.memory_candidates,
            escalation_requests=self.escalation_requests,
            suggested_actions=self.suggested_actions,
            context_updates=self.context_updates,
        )


@dataclass
class WowDeps:
    user_id: str
    zhixue: ZhixueAdapter
    full_agent: FullAgentProvider | None = None
    state: RunState = field(default_factory=RunState)
