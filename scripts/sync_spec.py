#!/usr/bin/env python3
"""Sync the TransitMatters Data Dashboard OpenAPI spec from upstream.

Downloads server/openapi.json from transitmatters/t-performance-dash at a
pinned commit and records that commit in spec/UPSTREAM_SHA.

Usage:
    python scripts/sync_spec.py              # sync to latest commit on main
    python scripts/sync_spec.py --ref <sha>  # sync to a specific commit, tag, or branch
    python scripts/sync_spec.py --check      # exit 1 if upstream differs; write nothing

Set GITHUB_TOKEN to avoid GitHub's unauthenticated API rate limit.
Standard library only, so it runs before any dependencies are installed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

UPSTREAM_REPO = "transitmatters/t-performance-dash"
UPSTREAM_PATH = "server/openapi.json"

ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = ROOT / "spec" / "openapi.json"
SHA_FILE = ROOT / "spec" / "UPSTREAM_SHA"


def _request(url: str, accept: str) -> bytes:
    headers = {"Accept": accept, "User-Agent": "transitmatters-py-sync"}
    token = os.environ.get("GITHUB_TOKEN")
    # Only the API needs auth (for rate limits). A token scoped to another
    # repo makes raw.githubusercontent.com return 404 for public files.
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"error: GET {url} failed with HTTP {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        sys.exit(f"error: GET {url} failed: {e.reason}")


def resolve_sha(ref: str) -> str:
    """Resolve a branch, tag, or short SHA to a full commit SHA."""
    url = f"https://api.github.com/repos/{UPSTREAM_REPO}/commits/{ref}"
    return _request(url, "application/vnd.github.sha").decode().strip()


def fetch_spec(sha: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{sha}/{UPSTREAM_PATH}"
    data = _request(url, "application/json")
    try:
        doc = json.loads(data)
    except json.JSONDecodeError as e:
        sys.exit(f"error: upstream spec at {sha} is not valid JSON: {e}")
    if "openapi" not in doc or "paths" not in doc:
        sys.exit(f"error: upstream file at {sha} doesn't look like an OpenAPI spec")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--ref", default="main", help="upstream branch, tag, or SHA (default: main)"
    )
    parser.add_argument(
        "--check", action="store_true", help="report drift without writing files"
    )
    args = parser.parse_args()

    sha = resolve_sha(args.ref)
    spec = fetch_spec(sha)

    current_spec = SPEC_FILE.read_bytes() if SPEC_FILE.exists() else b""
    current_sha = SHA_FILE.read_text().strip() if SHA_FILE.exists() else ""
    spec_changed = spec != current_spec

    if args.check:
        if spec_changed:
            print(
                f"spec differs from upstream {sha[:12]} (vendored: {current_sha[:12] or 'none'})"
            )
            sys.exit(1)
        print(f"spec matches upstream {sha[:12]}")
        return

    SPEC_FILE.parent.mkdir(parents=True, exist_ok=True)
    SPEC_FILE.write_bytes(spec)
    SHA_FILE.write_text(sha + "\n")

    if spec_changed:
        print(f"updated spec to upstream {sha[:12]}")
    elif sha != current_sha:
        print(f"spec unchanged; bumped pin to {sha[:12]}")
    else:
        print(f"already at {sha[:12]}")

    # Expose results to GitHub Actions steps.
    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as f:
            f.write(
                f"sha={sha}\nshort_sha={sha[:12]}\nchanged={str(spec_changed).lower()}\n"
            )


if __name__ == "__main__":
    main()
