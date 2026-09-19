import hashlib


def make_idempotency_key(run_id: str, tool_call_id: str, tool_name: str) -> str:
    payload = f"wow:v1:{run_id}:{tool_call_id}:{tool_name}".encode()
    return "wow_" + hashlib.sha256(payload).hexdigest()
