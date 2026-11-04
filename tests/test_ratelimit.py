"""Per-client token buckets and a global daily cap."""

from __future__ import annotations

from profile_agent.ratelimit import DailyCap, TokenBucket


def test_bucket_allows_burst_then_blocks() -> None:
    now = [1000.0]
    bucket = TokenBucket(capacity=3, per_seconds=60, clock=lambda: now[0])
    assert all(bucket.allow("ip-a")[0] for _ in range(3))
    ok, retry = bucket.allow("ip-a")
    assert ok is False and 0 < retry <= 60


def test_bucket_refills_over_time() -> None:
    now = [0.0]
    bucket = TokenBucket(capacity=2, per_seconds=10, clock=lambda: now[0])
    bucket.allow("k")
    bucket.allow("k")
    assert bucket.allow("k")[0] is False
    now[0] += 5.0  # half the window refills one token
    assert bucket.allow("k")[0] is True
    assert bucket.allow("k")[0] is False


def test_buckets_are_per_key() -> None:
    bucket = TokenBucket(capacity=1, per_seconds=60, clock=lambda: 0.0)
    assert bucket.allow("a")[0] is True
    assert bucket.allow("b")[0] is True
    assert bucket.allow("a")[0] is False


def test_bucket_forgets_idle_keys() -> None:
    now = [0.0]
    bucket = TokenBucket(capacity=1, per_seconds=10, clock=lambda: now[0], max_keys=2)
    for key in ("a", "b", "c"):
        bucket.allow(key)
    assert len(bucket) <= 2


def test_daily_cap_resets_on_new_day() -> None:
    now = [0.0]
    cap = DailyCap(limit=2, clock=lambda: now[0])
    assert cap.allow() and cap.allow()
    assert cap.allow() is False
    now[0] += 86_400
    assert cap.allow() is True
