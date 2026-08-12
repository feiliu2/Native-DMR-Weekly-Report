#!/usr/bin/env python3
"""
DMR IFWI Report Generator - pipeline core

Can be used two ways:
  1. As a module:  from generate_dmr_report import run_pipeline
  2. As a CLI:     python generate_dmr_report.py "AP1 A0" "2026.10.1.01" "released on WW10.5" [simics] [token]

For the natural-language front-end (paste the release line as-is), use
dmr_report.py in the project root instead.
"""

import sys
import os
import re
import subprocess
import shutil
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")

PRE_SI_PLATFORMS = ("AP1 B0", "AP2 A0")


def parse_release_info(release_info):
    """Parse a release info string into (tense, week).

    Examples:
        "is trend to be released on WW10.5" -> ("is trend to be released", "WW10.5")
        "will be released on WW10.5"        -> ("will be released", "WW10.5")
        "released on WW10.5"                -> ("has been released", "WW10.5")
    """
    # Ordered longest-first so "is trend to be released" wins over bare "released"
    patterns = [
        (r"(is trend to be released)\s+on\s+(WW\d+\.\d+)", None),
        (r"(is trending to be released)\s+on\s+(WW\d+\.\d+)", None),
        (r"(will be released)\s+on\s+(WW\d+\.\d+)", None),
        (r"(has been released)\s+on\s+(WW\d+\.\d+)", None),
        (r"(released)\s+on\s+(WW\d+\.\d+)", "has been released"),
    ]

    for pattern, tense_override in patterns:
        match = re.search(pattern, release_info, re.IGNORECASE)
        if match:
            tense = tense_override if tense_override else match.group(1)
            return tense, match.group(2)

    # Fallback: a bare week number means it already shipped
    week_match = re.search(r"(WW\d+\.\d+)", release_info, re.IGNORECASE)
    if week_match:
        return "has been released", week_match.group(1)

    return None, None


def _run(args):
    """Run a helper script with the current interpreter, return CompletedProcess."""
    return subprocess.run(
        [sys.executable] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _grab(stdout, prefix):
    """Return the value following the first line starting with prefix."""
    for line in stdout.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):].strip()
    return None


class PipelineError(Exception):
    """Raised when a stage of the report pipeline fails."""


def run_pipeline(platform, orange_id, release_tense, release_week,
                 simics_version=None, api_token=None, open_browser=True,
                 log=print):
    """Search Artifactory, extract versions, and generate the HTML report.

    Returns the path to the generated report in output/.
    Raises PipelineError with a readable message if any stage fails.
    """
    if not re.match(r"^AP[12] [AB]0$", platform):
        raise PipelineError(
            f"Invalid platform '{platform}' (expected AP1 A0, AP1 B0, or AP2 A0)")

    if not re.match(r"^\d{4}\.\d+\.\d+\.\d+$", orange_id):
        raise PipelineError(
            f"Invalid Orange ID '{orange_id}' (expected YYYY.WW.X.NN)")

    if platform in PRE_SI_PLATFORMS and not simics_version:
        raise PipelineError(
            f"Simics version is required for Pre-Si platform {platform}")

    if not api_token:
        raise PipelineError("Artifactory API token is required")

    # Step 1: find the build for this Orange ID
    log("  [1/4] Searching Artifactory...")
    result = _run([os.path.join(SCRIPT_DIR, "search_artifactory_by_orange_id.py"),
                   platform, orange_id, api_token])
    if result.returncode != 0:
        raise PipelineError(f"Artifactory search failed:\n{result.stdout}{result.stderr}")

    bios_id = _grab(result.stdout, "BIOS_ID:")
    version_string = _grab(result.stdout, "VERSION:")
    if not bios_id or not version_string:
        if "MATCH_0_BIOS_ID:" in result.stdout:
            raise PipelineError(
                f"Multiple builds found for {orange_id}. Re-run "
                f"scripts/generate_dmr_report.py manually to pick one:\n{result.stdout}")
        raise PipelineError(f"No build found for Orange ID {orange_id}:\n{result.stdout}")
    log(f"        BIOS ID: {bios_id}")

    # Step 2: resolve the BuildPkg download URL
    log("  [2/4] Locating build package...")
    result = _run([os.path.join(SCRIPT_DIR, "construct_artifactory_url.py"),
                   platform, version_string, api_token])
    if result.returncode != 0:
        raise PipelineError(f"Could not build Artifactory URL:\n{result.stdout}{result.stderr}")

    artifactory_url = _grab(result.stdout, "URL: ")
    if not artifactory_url or not artifactory_url.startswith("https://"):
        raise PipelineError(f"Could not extract BuildPkg URL:\n{result.stdout}")

    # Step 3: download and extract BIOS / UP / OSXML data
    log("  [3/4] Downloading and extracting versions (this takes a minute)...")
    work_dir = os.path.join(PROJECT_DIR, bios_id)
    os.makedirs(work_dir, exist_ok=True)

    result = _run([os.path.join(SCRIPT_DIR, "extract_artifactory_osxml.py"),
                   artifactory_url, api_token, work_dir, platform,
                   simics_version or ""])
    if result.returncode != 0:
        raise PipelineError(f"Data extraction failed:\n{result.stdout}{result.stderr}")

    csv_path = _grab(result.stdout, "CSV_OUTPUT:")
    if not csv_path or not os.path.exists(csv_path):
        raise PipelineError(f"Extraction produced no CSV:\n{result.stdout}")

    # Step 4: render the HTML report
    log("  [4/4] Generating HTML report...")
    result = _run([os.path.join(SCRIPT_DIR, "generate_ifwi_report.py"),
                   csv_path, orange_id, release_week, release_tense])
    if result.returncode != 0:
        raise PipelineError(f"HTML generation failed:\n{result.stdout}{result.stderr}")

    html_file = os.path.join(work_dir, f"IFWI_Release_Status_{orange_id}.html")
    if not os.path.exists(html_file):
        raise PipelineError(f"Expected report not found at {html_file}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, f"IFWI_Release_Status_{orange_id}.html")
    shutil.copy2(html_file, output_file)

    if open_browser:
        webbrowser.open(output_file)

    return output_file


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print('Examples:')
        print('  python generate_dmr_report.py "AP1 A0" "2026.10.1.01" '
              '"is trend to be released on WW10.5" <token>')
        print('  python generate_dmr_report.py "AP2 A0" "2026.10.1.05" '
              '"released on WW10.5" "dmr-rio-7 2026ww09.1.00_01 Pre500" <token>')
        sys.exit(1)

    platform = sys.argv[1]
    orange_id = sys.argv[2]
    release_info = sys.argv[3]

    # argv[4] is either the Simics version or the API token
    simics_version = None
    api_token = None
    if len(sys.argv) >= 5:
        arg4 = sys.argv[4]
        if arg4.startswith("AKCp") or arg4.startswith("eyJ"):
            api_token = arg4
        else:
            simics_version = arg4
            if len(sys.argv) >= 6:
                api_token = sys.argv[5]

    release_tense, release_week = parse_release_info(release_info)
    if not release_week:
        print(f"[ERROR] Could not parse a release week (WWxx.x) from: {release_info}")
        sys.exit(1)

    if not api_token:
        print("\nArtifactory API Token required")
        print("Get it from: https://af01p-or.devtools.intel.com/ -> Edit Profile -> API Key")
        api_token = input("API Token: ").strip()

    print("=" * 60)
    print("DMR IFWI Report Generator")
    print("=" * 60)
    print(f"Platform:  {platform}")
    print(f"Orange ID: {orange_id}")
    print(f"Release:   {release_tense} on {release_week}")
    if simics_version:
        print(f"Simics:    {simics_version}")
    print()

    try:
        output_file = run_pipeline(platform, orange_id, release_tense, release_week,
                                   simics_version, api_token)
    except PipelineError as exc:
        print(f"\n[ERROR] {exc}")
        sys.exit(1)

    print(f"\n[OK] Report: {output_file}")
    print("[OK] Opened in browser")


if __name__ == "__main__":
    main()
