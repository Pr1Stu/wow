from wow.tools.idempotency import make_idempotency_key


def test_idempotency_key_is_stable_and_call_specific() -> None:
    first = make_idempotency_key("run-1", "call-1", "create_task")
    same = make_idempotency_key("run-1", "call-1", "create_task")
    other = make_idempotency_key("run-1", "call-2", "create_task")
    assert first == same
    assert first != other
    assert first.startswith("wow_")
