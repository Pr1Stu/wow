from pydantic import BaseModel, Field

from wow.contracts import AgentRunResult


class RunRequest(BaseModel):
    profile: str = "chat"
    prompt: str = Field(min_length=1, max_length=64_000)
    interrupt: bool = False


class RunResponse(AgentRunResult):
    pass


class ErrorResponse(BaseModel):
    code: str
    message: str
    retryable: bool = False
    run_id: str | None = None
