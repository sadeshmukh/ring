#!/usr/bin/env python3
"""Validate channels.yml entries.

Checks:
 - `channels` key exists and is a list
 - each item has `channel_id`, `user_id`, `slug`
 - channel_id looks like a Slack channel id (starts with C)
 - user_id looks like a Slack user id (starts with U)
 - slug is URL-safe (lowercase letters, digits, hyphen, dot, underscore, tilde) and contains no commas

Exit code: 0 on success, 1 on validation errors, 2 on parsing / usage errors.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml


CHANNEL_PATTERN = re.compile(r"^[C][A-Z0-9]{8,}$")
USER_PATTERN = re.compile(r"^[U][A-Z0-9]{8,}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9._~\-]+$")


def validate_entry(entry: dict[str, Any], index: int, filename: str) -> list[str]:
    errors: list[str] = []
    prefix = f"{filename}:channels[{index}]"

    if not isinstance(entry, dict):
        errors.append(f"{prefix}: entry is not a mapping/dict")
        return errors

    for key in ("channel_id", "user_id", "slug"):
        if key not in entry:
            errors.append(f"{prefix}: missing required key '{key}'")

    channel_id = entry.get("channel_id")
    user_id = entry.get("user_id")
    slug = entry.get("slug")

    if channel_id is not None:
        if not isinstance(channel_id, str) or not CHANNEL_PATTERN.match(channel_id):
            errors.append(
                f"{prefix}.channel_id='{channel_id}' is not a valid Slack channel id (expected e.g. C12345678)"
            )

    if user_id is not None:
        if not isinstance(user_id, str) or not USER_PATTERN.match(user_id):
            errors.append(
                f"{prefix}.user_id='{user_id}' is not a valid Slack user id (expected e.g. U12345678)"
            )

    if slug is not None:
        if not isinstance(slug, str) or not slug:
            errors.append(f"{prefix}.slug must be a non-empty string")
        else:
            if "," in slug:
                errors.append(f"{prefix}.slug='{slug}' must not contain commas")
            if not SLUG_PATTERN.match(slug):
                errors.append(
                    f"{prefix}.slug='{slug}' contains invalid characters; allowed: a-z 0-9 . _ ~ -"
                )

    return errors


def load_yaml(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        raise
    except yaml.YAMLError as exc:
        print(f"Error parsing YAML {path}: {exc}", file=sys.stderr)
        raise


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate channels.yml entries")
    p.add_argument("files", nargs="*", help="YAML files to validate (default: channels.yml)")
    args = p.parse_args(argv)

    files = args.files or ["channels.yml"]
    had_error = False

    for f in files:
        path = Path(f)
        try:
            data = load_yaml(path)
        except Exception:
            had_error = True
            continue

        if data is None:
            print(f"{path}: YAML is empty", file=sys.stderr)
            had_error = True
            continue

        if not isinstance(data, dict):
            print(f"{path}: top-level YAML structure must be a mapping/object", file=sys.stderr)
            had_error = True
            continue

        channels = data.get("channels")
        if channels is None:
            print(f"{path}: missing top-level 'channels' key", file=sys.stderr)
            had_error = True
            continue

        if not isinstance(channels, list):
            print(f"{path}: 'channels' must be a list", file=sys.stderr)
            had_error = True
            continue

        all_errors: list[str] = []
        for i, entry in enumerate(channels):
            all_errors.extend(validate_entry(entry, i, str(path)))

        if all_errors:
            had_error = True
            for e in all_errors:
                print(e, file=sys.stderr)
        else:
            print(f"{path}: OK ({len(channels)} channels)")

    return 1 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
