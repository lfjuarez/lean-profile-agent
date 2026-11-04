from __future__ import annotations

import pytest

from profile_agent.kb import KnowledgeBase, load_kb


@pytest.fixture(scope="session")
def kb_en() -> KnowledgeBase:
    return load_kb("en")


@pytest.fixture(scope="session")
def kb_es() -> KnowledgeBase:
    return load_kb("es")
