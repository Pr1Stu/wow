from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Request, status

from wow.agent.runtime import AgentRuntime
from wow.api.models import RunRequest, RunResponse
from wow.profiles import ProfileStore

router = APIRouter()


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/v1/profiles")
async def profiles(request: Request) -> dict[str, list[str]]:
    store: ProfileStore = request.app.state.profiles
    return {"profiles": store.names()}


@router.post("/v1/runs", response_model=RunResponse)
async def create_run(
    body: RunRequest,
    request: Request,
    x_wow_user_id: str | None = Header(default=None),
) -> RunResponse:
    # Production identity resolution deliberately follows the ZhiXUE main project (TBD).
    # The header is enabled only for local bootstrap testing.
    if not request.app.state.settings.dev_auth:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="ZhiXUE authentication integration is not configured",
        )
    if not x_wow_user_id:
        raise HTTPException(status_code=401, detail="X-Wow-User-Id is required in dev auth mode")

    runtime: AgentRuntime = request.app.state.runtime
    try:
        result = await runtime.run(
            user_id=x_wow_user_id,
            profile_name=body.profile,
            prompt=body.prompt,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="unknown agent profile") from exc
    return RunResponse.model_validate(result)
