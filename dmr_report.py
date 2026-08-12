#!/usr/bin/env python3
"""
DMR Weekly Report generator - paste the release line, get the HTML.

This replaces the Claude Code workflow: it parses the same release sentences you
would have pasted into chat, then runs the full Artifactory pipeline for each one.

Usage
-----
  Interactive (easiest - just run it and paste):
      python dmr_report.py

  Inline, one or more releases:
      python dmr_report.py "AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5"

  From a file (one release per line):
      python dmr_report.py -f releases.txt

Accepted release-line shapes (all of these parse):
  AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5
  DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.10.1.05 is trend to be released on WW10.5  dmr-rio-7 2026ww09.1.00_01 Pre500
  AP1 B0 Pre-Si Orange IFWI 2026.10.1.02 released on WW10.5  dmr-7 2026ww09.1.00_02 Pre500

The API token is asked for once and remembered in .dmr_token (gitignored).
Override with --token <tok> or the DMR_API_TOKEN environment variable.
"""

import os
import re
import sys
import getpass

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from generate_dmr_report import (  # noqa: E402
    parse_release_info,
    run_pipeline,
    PipelineError,
    PRE_SI_PLATFORMS,
)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(PROJECT_DIR, ".dmr_token")
TOKEN_URL = "https://af01p-or.devtools.intel.com/  ->  Edit Profile  ->  API Key"

# "AP1 A0", "AP2A0", "ap1 b0" - but not the "AP" in "DMR-AP-UCC"
PLATFORM_RE = re.compile(r"\bAP\s*([12])\s*[-_ ]?\s*([AB]0)\b", re.IGNORECASE)
ORANGE_ID_RE = re.compile(r"\b(\d{4}\.\d+\.\d+\.\d+)\b")
# Optional "Simics-rio-7"/"dmr-7" prefix + version + optional "Pre550" suffix
SIMICS_RE = re.compile(
    r"((?:[\w-]*(?:simics|dmr)[\w-]*\s+)?\d{4}ww\d{1,2}\.\d+\.\d+_\d+(?:\s+Pre\d+)?)",
    re.IGNORECASE,
)
SILICON_RE = re.compile(r"\b(Pre|Post)[\s-]*Si\b", re.IGNORECASE)


class ParseError(Exception):
    """Raised when a release line cannot be understood."""


def parse_release_line(line):
    """Turn one free-text release sentence into pipeline arguments.

    Returns a dict with platform, orange_id, release_tense, release_week,
    simics_version (None for Post-Si) and any non-fatal warnings.
    """
    text = line.strip()
    # Strip common bullet/list decoration pasted out of Word or Outlook
    text = re.sub(r"^[\s·•o\-\*\d]+[\.\)\t ]\s*", "", text) or text
    if not text:
        raise ParseError("empty line")

    platform_match = PLATFORM_RE.search(text)
    if not platform_match:
        raise ParseError("could not find a platform (expected AP1 A0, AP1 B0 or AP2 A0)")
    platform = f"AP{platform_match.group(1)} {platform_match.group(2).upper()}"

    orange_match = ORANGE_ID_RE.search(text)
    if not orange_match:
        raise ParseError("could not find an Orange IFWI ID (expected YYYY.WW.X.NN)")
    orange_id = orange_match.group(1)

    release_tense, release_week = parse_release_info(text)
    if not release_week:
        raise ParseError("could not find a release week (expected WWxx.x)")

    simics_match = SIMICS_RE.search(text)
    simics_version = simics_match.group(1).strip() if simics_match else None

    warnings = []

    # The line usually states Pre-Si/Post-Si too; flag it if it disagrees with
    # the platform, since one of the two is then a typo.
    silicon_match = SILICON_RE.search(text)
    if silicon_match:
        stated = silicon_match.group(1).capitalize()
        implied = "Pre" if platform in PRE_SI_PLATFORMS else "Post"
        if stated != implied:
            warnings.append(
                f"line says {stated}-Si but {platform} is a {implied}-Si platform "
                f"- generating as {implied}-Si")

    if platform in PRE_SI_PLATFORMS and not simics_version:
        raise ParseError(
            f"{platform} is Pre-Si and needs a Simics version "
            f"(e.g. 'dmr-rio-7 2026ww09.1.00_01 Pre500')")

    if platform not in PRE_SI_PLATFORMS and simics_version:
        warnings.append(
            f"ignoring Simics version '{simics_version}' - {platform} is Post-Si")
        simics_version = None

    return {
        "platform": platform,
        "orange_id": orange_id,
        "release_tense": release_tense,
        "release_week": release_week,
        "simics_version": simics_version,
        "warnings": warnings,
    }


def get_api_token(cli_token=None):
    """Resolve the Artifactory token: CLI arg, env var, saved file, then prompt."""
    if cli_token:
        return cli_token

    env_token = os.environ.get("DMR_API_TOKEN", "").strip()
    if env_token:
        return env_token

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as handle:
            saved = handle.read().strip()
        if saved:
            return saved

    print("Artifactory API token needed (asked once, then remembered).")
    print(f"  Get it from: {TOKEN_URL}")
    token = getpass.getpass("  API Token (not echoed): ").strip()
    if not token:
        return None

    answer = input(f"  Save it to {os.path.basename(TOKEN_FILE)} for next time? [Y/n] ").strip().lower()
    if answer in ("", "y", "yes"):
        with open(TOKEN_FILE, "w", encoding="utf-8") as handle:
            handle.write(token)
        print(f"  Saved. Delete {os.path.basename(TOKEN_FILE)} if the token expires.")
    print()
    return token


def read_lines_interactively():
    """Prompt the user to paste one or more release lines."""
    print("=" * 68)
    print("DMR Weekly Report Generator")
    print("=" * 68)
    print("Paste your release line(s) below - one release per line.")
    print("Press Enter on an empty line when you are done.")
    print()
    print("  e.g. AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5")
    print()

    lines = []
    while True:
        try:
            line = input("> " if not lines else "  ")
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return lines


def main():
    argv = sys.argv[1:]

    cli_token = None
    if "--token" in argv:
        index = argv.index("--token")
        if index + 1 >= len(argv):
            print("[ERROR] --token needs a value")
            return 1
        cli_token = argv[index + 1]
        del argv[index:index + 2]

    no_browser = False
    if "--no-browser" in argv:
        argv.remove("--no-browser")
        no_browser = True

    # Gather the release lines
    if argv and argv[0] in ("-f", "--file"):
        if len(argv) < 2:
            print("[ERROR] -f needs a file path")
            return 1
        try:
            with open(argv[1], "r", encoding="utf-8") as handle:
                raw_lines = [ln for ln in handle if ln.strip()]
        except OSError as exc:
            print(f"[ERROR] Cannot read {argv[1]}: {exc}")
            return 1
    elif argv and argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    elif argv:
        raw_lines = argv
    else:
        raw_lines = read_lines_interactively()

    if not raw_lines:
        print("Nothing to do - no release lines given.")
        return 1

    # Parse everything up front so typos surface before any slow downloads
    parsed = []
    parse_failures = []
    for raw in raw_lines:
        try:
            parsed.append((raw.strip(), parse_release_line(raw)))
        except ParseError as exc:
            parse_failures.append((raw.strip(), str(exc)))

    if parse_failures:
        print("Could not understand these line(s):")
        for raw, reason in parse_failures:
            print(f"  x {raw}")
            print(f"    -> {reason}")
        print()
        if not parsed:
            print("Expected shape:")
            print("  AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5")
            print("  AP2 A0 Pre-Si Orange IFWI 2026.10.1.05 released on WW10.5  "
                  "dmr-rio-7 2026ww09.1.00_01 Pre500")
            return 1

    print(f"Understood {len(parsed)} release(s):")
    for _, info in parsed:
        simics = f"  Simics: {info['simics_version']}" if info["simics_version"] else ""
        print(f"  - {info['platform']}  {info['orange_id']}  "
              f"{info['release_tense']} on {info['release_week']}{simics}")
        for warning in info["warnings"]:
            print(f"    ! {warning}")
    print()

    token = get_api_token(cli_token)
    if not token:
        print("[ERROR] No API token supplied - cannot reach Artifactory.")
        return 1

    results = []
    for index, (raw, info) in enumerate(parsed, start=1):
        print(f"[{index}/{len(parsed)}] {info['platform']} {info['orange_id']}")
        try:
            output_file = run_pipeline(
                platform=info["platform"],
                orange_id=info["orange_id"],
                release_tense=info["release_tense"],
                release_week=info["release_week"],
                simics_version=info["simics_version"],
                api_token=token,
                open_browser=not no_browser,
                log=print,
            )
            print(f"        -> {output_file}")
            results.append((info, output_file, None))
        except PipelineError as exc:
            print(f"        [FAILED] {exc}")
            results.append((info, None, str(exc)))
        print()

    # Summary
    succeeded = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]

    print("=" * 68)
    print(f"Done: {len(succeeded)} generated, {len(failed)} failed"
          + (f", {len(parse_failures)} unparsed" if parse_failures else ""))
    print("=" * 68)
    for info, output_file, _ in succeeded:
        print(f"  OK      {info['platform']} {info['orange_id']} -> {output_file}")
    for info, _, error in failed:
        print(f"  FAILED  {info['platform']} {info['orange_id']}: {error.splitlines()[0]}")
    for raw, reason in parse_failures:
        print(f"  UNREAD  {raw}  ({reason})")

    if failed and any("token" in (e or "").lower() or "403" in (e or "")
                      for _, _, e in failed):
        print()
        print(f"Tip: if the token expired, delete {os.path.basename(TOKEN_FILE)} "
              f"and re-run to enter a new one.")

    return 0 if succeeded and not failed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
