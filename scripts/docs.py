#!/usr/bin/env python3
"""Build or preview the API docs for the transitmatters package with pdoc.

Usage:
    python scripts/docs.py            # serve at http://localhost:8080, reloading on change
    python scripts/docs.py -o site    # write static HTML to site/

Takes the same options as the `pdoc` command.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator

import pdoc.__main__
import pdoc.render_helpers

PACKAGE = "transitmatters"
GENERATED_MODELS = f"{PACKAGE}._generated.models."

_module_candidates = pdoc.render_helpers.module_candidates


def module_candidates(identifier: str, current_module: str) -> Iterator[str]:
    # pdoc links a type only to where it's documented on the current page or
    # in a parent package of the module that defines it. Models are defined
    # in transitmatters._generated.models.* but documented in the sibling
    # transitmatters.models, so without this, return types show their private
    # path and don't link.
    yield from _module_candidates(identifier, current_module)
    if identifier.startswith(GENERATED_MODELS):
        yield f"{PACKAGE}.models"


def main() -> None:
    pdoc.render_helpers.module_candidates = module_candidates
    pdoc.__main__.cli([*sys.argv[1:], PACKAGE])


if __name__ == "__main__":
    main()
