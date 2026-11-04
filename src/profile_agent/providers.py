"""Alternative chat backends over OpenAI-compatible endpoints (OpenRouter, Gemini).

Same contract as ``AnthropicBackend``: ``stream(system, messages)`` yields text and sets
``stop_reason``. Selected with ``PROFILE_PROVIDER`` (anthropic | openrouter | gemini).
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import Iterator
from typing import Any

import httpx

from .chat import AnthropicBackend, Backend, ChatError

log = logging.getLogger(__name__)

PROVIDERS: dict[str, dict[str, str]] = {
    "openrouter": {
        "url": "https://openrouter.ai/api/v1/chat/completions",
        "key_env": "OPENROUTER_API_KEY",
        "model_env": "OPENROUTER_MODEL",
        "default_model": "dots-studio/dots-3-note-preview:free",
    },
    "gemini": {
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
        "key_env": "GEMINI_API_KEY",
        "model_env": "GEMINI_MODEL",
        "default_model": "gemini-flash-lite-latest",
    },
}


RETRIES = 2


class OpenAICompatBackend:
    def __init__(self, provider: str, model: str | None = None, max_tokens: int = 4000) -> None:
        cfg = PROVIDERS[provider]
        self.provider = provider
        self.url = cfg["url"]
        self.key_env = cfg["key_env"]
        self.model = model or os.environ.get(cfg["model_env"]) or cfg["default_model"]
        self.max_tokens = max_tokens
        self.stop_reason: str | None = None

    def _read(self, r: Any) -> Iterator[str]:
        for line in r.iter_lines():
            if not line.startswith("data: "):
                continue
            data = line[6:].strip()
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            for choice in chunk.get("choices") or []:
                piece = (choice.get("delta") or {}).get("content")
                if piece:
                    yield piece
                if choice.get("finish_reason"):
                    self.stop_reason = choice["finish_reason"]

    def stream(self, system: str, messages: list[dict[str, Any]]) -> Iterator[str]:
        key = os.environ.get(self.key_env)
        if not key:
            raise ChatError("not_configured")
        self.stop_reason = None
        body = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "stream": True,
            "messages": [{"role": "system", "content": system}, *messages],
        }
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        if self.provider == "openrouter":
            headers["X-Title"] = "lean-profile-agent"
        try:
            for attempt in range(RETRIES + 1):
                with httpx.stream("POST", self.url, json=body, headers=headers, timeout=60.0) as r:
                    if r.status_code in (429, 503) and attempt < RETRIES:
                        # free tiers throttle bursts; nothing was streamed yet, so retry is safe
                        time.sleep(2.0 * (attempt + 1))
                        continue
                    if r.status_code == 429:
                        raise ChatError("busy")
                    if r.status_code in (401, 403):
                        raise ChatError("not_configured")
                    if r.status_code >= 400:
                        log.warning(
                            "%s status %s: %s", self.provider, r.status_code, r.read()[:300]
                        )
                        raise ChatError("busy" if r.status_code >= 500 else "unavailable")
                    yield from self._read(r)
                    return
        except httpx.HTTPError as exc:
            raise ChatError("unavailable") from exc


def backend_from_env(provider: str | None = None) -> Backend:
    provider = (provider or os.environ.get("PROFILE_PROVIDER") or "anthropic").lower()
    if provider == "anthropic":
        return AnthropicBackend()
    if provider in PROVIDERS:
        return OpenAICompatBackend(provider)
    raise ValueError(f"unknown PROFILE_PROVIDER {provider!r}")
