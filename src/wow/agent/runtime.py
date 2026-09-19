from __future__ import annotations

from uuid import uuid4

from pydantic_ai import UsageLimits

from wow.adapters.base import ZhixueAdapter
from wow.agent.deps import WowDeps
from wow.agent.factory import AgentFactory
from wow.contracts import AgentRunResult, UserResponse
from wow.full_agent.base import FullAgentProvider
from wow.profiles import ProfileStore


class AgentRuntime:
    def __init__(
        self,
        profiles: ProfileStore,
        agents: AgentFactory,
        zhixue: ZhixueAdapter,
        full_agent: FullAgentProvider | None = None,
    ) -> None:
        self.profiles = profiles
        self.agents = agents
        self.zhixue = zhixue
        self.full_agent = full_agent

    async def run(self, *, user_id: str, profile_name: str, prompt: str) -> AgentRunResult:
        resolved = self.profiles.load(profile_name)
        profile = resolved.profile
        run_id = str(uuid4())
        deps = WowDeps(user_id=user_id, zhixue=self.zhixue, full_agent=self.full_agent)
        agent = self.agents.create(resolved)
        result = await agent.run(
            prompt,
            deps=deps,
            run_id=run_id,
            usage_limits=UsageLimits(
                request_limit=profile.limits.max_steps,
                tool_calls_limit=profile.limits.max_tool_calls,
            ),
        )
        return AgentRunResult(
            run_id=run_id,
            response=UserResponse(text=result.output),
            state_delta=deps.state.to_delta(),
        )
