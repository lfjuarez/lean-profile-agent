"""Entry point: ``python -m profile_agent`` or the ``profile-agent`` console script."""

from __future__ import annotations

import os

import uvicorn


def main() -> None:
    uvicorn.run(
        "profile_agent.web:get_app",
        factory=True,
        host=os.environ.get("HOST", "0.0.0.0"),  # noqa: S104 - container entry point
        port=int(os.environ.get("PORT", "8080")),
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    main()
