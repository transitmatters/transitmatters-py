"""Setup for the docs examples, run with `tox -e examples` (see tox.toml)."""

from __future__ import annotations

from typing import Any

import pytest


@pytest.hookimpl(optionalhook=True)  # only pytest-markdown-docs defines this hook
def pytest_markdown_docs_globals() -> dict[str, Any]:
    """Names the README and docstring snippets use without defining."""
    from transitmatters import Line, TransitMatters

    return {"Line": Line, "tm": TransitMatters()}
