from __future__ import annotations

from pydantic_ai import Agent

from wow.agent.deps import WowDeps
from wow.agent.model import GatewayModelFactory
from wow.profiles import ResolvedProfile
from wow.tools.registry import tools_for_profile


class AgentFactory:
    def __init__(self, models: GatewayModelFactory) -> None:
        self.models = models

    def create(self, resolved: ResolvedProfile) -> Agent[WowDeps, str]:
        profile = resolved.profile
        return Agent(
            self.models.create(profile.model),
            deps_type=WowDeps,
            output_type=str,
            instructions=resolved.instructions,
            tools=tools_for_profile(profile.tools),
        )
