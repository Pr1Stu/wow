from pathlib import Path

from wow.profiles import ProfileStore


def test_chat_profile_loads() -> None:
    root = Path(__file__).resolve().parents[2]
    store = ProfileStore(root / "profiles", root / "prompts")
    resolved = store.load("chat")
    assert resolved.profile.context.compact_threshold == 32_000
    assert resolved.profile.model == "wow-chat"
    assert "request_escalation" in resolved.profile.tools
    assert len(resolved.prompt_hash) == 64
    assert len(resolved.profile_hash) == 64
