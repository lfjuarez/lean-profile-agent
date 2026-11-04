"""In-memory rate limiting: a token bucket per client key and a global daily cap.

Good enough for one Cloud Run instance serving a public demo. With several instances each one
keeps its own counters, which only makes the limits more generous, never unsafe.
"""

from __future__ import annotations

import threading
import time
from collections import OrderedDict
from collections.abc import Callable


class TokenBucket:
    def __init__(
        self,
        capacity: int,
        per_seconds: float,
        clock: Callable[[], float] = time.monotonic,
        max_keys: int = 10_000,
    ) -> None:
        self.capacity = capacity
        self.per_seconds = per_seconds
        self.rate = capacity / per_seconds
        self.clock = clock
        self.max_keys = max_keys
        self._state: OrderedDict[str, tuple[float, float]] = OrderedDict()  # key -> (tokens, t)
        self._lock = threading.Lock()

    def __len__(self) -> int:
        return len(self._state)

    def allow(self, key: str) -> tuple[bool, float]:
        """Return ``(allowed, retry_after_seconds)``."""
        now = self.clock()
        with self._lock:
            tokens, last = self._state.get(key, (float(self.capacity), now))
            tokens = min(float(self.capacity), tokens + (now - last) * self.rate)
            if tokens >= 1.0:
                tokens -= 1.0
                allowed, retry = True, 0.0
            else:
                allowed, retry = False, (1.0 - tokens) / self.rate
            self._state[key] = (tokens, now)
            self._state.move_to_end(key)
            while len(self._state) > self.max_keys:
                self._state.popitem(last=False)
        return allowed, retry


class DailyCap:
    """Global counter that resets every 24 hours (relative to the first call)."""

    def __init__(self, limit: int, clock: Callable[[], float] = time.time) -> None:
        self.limit = limit
        self.clock = clock
        self._count = 0
        self._window_start = clock()
        self._lock = threading.Lock()

    @property
    def count(self) -> int:
        return self._count

    def allow(self) -> bool:
        now = self.clock()
        with self._lock:
            if now - self._window_start >= 86_400:
                self._window_start = now
                self._count = 0
            if self._count >= self.limit:
                return False
            self._count += 1
            return True
