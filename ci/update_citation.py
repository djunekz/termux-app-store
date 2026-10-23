#!/usr/bin/env python3
"""
ci/update_citation.py
Keep CITATION.cff in step with a release.

Sets `version` and `date-released` in CITATION.cff from a release tag. The
release date is read from the matching heading in CHANGELOG.md
(`## [v0.9.1] - 2026-10-21`), so the citation always agrees with the
changelog; when the heading has no date, today's date (UTC) is used.

Only those two top-level lines are touched. Nothing else in the file changes
and no YAML library is needed.

Usage:
  python ci/update_citation.py --version v0.9.2            # write the file
  python ci/update_citation.py --version v0.9.2 --check    # exit 1 if stale
  python ci/update_citation.py --version v0.9.2 --only-if-newer

Options:
  --version V        Release tag or version (a leading "v" is removed).
  --date D           Release date, YYYY-MM-DD (default: from the changelog).
  --file PATH        Citation file (default: CITATION.cff).
  --changelog PATH   Changelog file (default: CHANGELOG.md).
  --check            Do not write; exit 1 when the file does not match.
  --only-if-newer    Do not move the file back to an older version.
  --warn             In GitHub Actions, emit a warning annotation when the
                     file had to be changed.

Exit codes: 0 ok, 1 mismatch (--check only), 2 error.

When GITHUB_OUTPUT is set, `changed` (true/false) and `version` are written
to it so a workflow can decide whether to commit.
"""

import argparse
import datetime
import os
import re
import sys
from pathlib import Path

VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z][0-9A-Za-z.+-]*)?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_VERSION_LINE = re.compile(r'^version:[ \t]*"?([^"\r\n]*?)"?[ \t]*$', re.MULTILINE)
_DATE_LINE = re.compile(r'^date-released:[ \t]*"?([^"\r\n]*?)"?[ \t]*$', re.MULTILINE)


def normalize_version(raw):
    version = raw.strip()
    if version[:1] in ("v", "V"):
        version = version[1:]
    if not VERSION_RE.match(version):
        raise ValueError(f"not a valid version: {raw!r} (expected e.g. v1.2.3)")
    return version


def changelog_date(changelog_text, version):
    pattern = re.compile(
        r"^##[ \t]*\[v?" + re.escape(version) + r"\][ \t]*-[ \t]*(\d{4}-\d{2}-\d{2})",
        re.MULTILINE,
    )
    match = pattern.search(changelog_text)
    return match.group(1) if match else None


def today_utc():
    return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def read_fields(text):
    version = _VERSION_LINE.search(text)
    date = _DATE_LINE.search(text)
    return (version.group(1) if version else None, date.group(1) if date else None)


def version_key(version):
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:[-+](.*))?$", version)
    if not match:
        return (-1, -1, -1, 0, "")
    major, minor, patch, extra = match.groups()
    return (int(major), int(minor), int(patch), 0 if extra else 1, extra or "")


def apply_fields(text, version, date):
    if not _VERSION_LINE.search(text):
        raise ValueError("no top-level `version:` line found in the citation file")
    if not _DATE_LINE.search(text):
        raise ValueError("no top-level `date-released:` line found in the citation file")
    text = _VERSION_LINE.sub(lambda _m: f'version: "{version}"', text, count=1)
    text = _DATE_LINE.sub(lambda _m: f'date-released: "{date}"', text, count=1)
    return text


def _write_outputs(changed, version):
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"changed={'true' if changed else 'false'}\n")
        handle.write(f"version={version}\n")


def _parse_args(argv):
    parser = argparse.ArgumentParser(description="Update version and date-released in CITATION.cff from a release tag.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--date")
    parser.add_argument("--file", default="CITATION.cff")
    parser.add_argument("--changelog", default="CHANGELOG.md")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--only-if-newer", action="store_true")
    parser.add_argument("--warn", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)

    try:
        version = normalize_version(args.version)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    citation = Path(args.file)
    if not citation.is_file():
        print(f"error: {citation} not found", file=sys.stderr)
        return 2
    text = citation.read_text(encoding="utf-8")

    date = args.date
    if date is None:
        changelog = Path(args.changelog)
        if changelog.is_file():
            date = changelog_date(changelog.read_text(encoding="utf-8"), version)
        if date is None:
            date = today_utc()
            print(f"note: no dated changelog heading for {version}, using today ({date})")
    if not DATE_RE.match(date):
        print(f"error: not a valid date: {date!r} (expected YYYY-MM-DD)", file=sys.stderr)
        return 2

    current_version, current_date = read_fields(text)

    if args.check:
        if (current_version, current_date) == (version, date):
            print(f"ok: {citation} is at {version} ({date})")
            return 0
        print(
            f"mismatch: {citation} has version {current_version} / date {current_date}, release is {version} / {date}",
            file=sys.stderr,
        )
        return 1

    if args.only_if_newer and current_version and version_key(current_version) > version_key(version):
        print(f"skip: {citation} is already at newer version {current_version}")
        _write_outputs(False, current_version)
        return 0

    try:
        new_text = apply_fields(text, version, date)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    changed = new_text != text
    if changed:
        citation.write_text(new_text, encoding="utf-8")
        message = f"{citation} updated: version {current_version} -> {version}, date {current_date} -> {date}"
        print(message)
        if args.warn and os.environ.get("GITHUB_ACTIONS") == "true":
            print(
                f"::warning file={citation}::The tagged commit had an outdated {citation} "
                f"({current_version}). It was corrected for this release; commit the same "
                f"change before the next tag."
            )
    else:
        print(f"ok: {citation} already at {version} ({date})")

    _write_outputs(changed, version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
