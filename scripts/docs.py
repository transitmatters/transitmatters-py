#!/usr/bin/env python3
"""Build or preview the API docs for the transitmatters package with pdoc.

Usage:
    python scripts/docs.py            # serve at http://localhost:8080, reloading on change
    python scripts/docs.py -o site    # write static HTML to site/

Takes the same options as the `pdoc` command.
"""

from __future__ import annotations

import sys

import pdoc.__main__

PACKAGE = "transitmatters"


def main() -> None:
    pdoc.__main__.cli([*sys.argv[1:], PACKAGE])


if __name__ == "__main__":
    main()
