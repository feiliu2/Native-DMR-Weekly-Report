# How to Generate the DMR Weekly Report (without Claude Code)

Everything runs from one Python script. You paste the same release sentence you
used to paste into chat, and it produces the HTML report.

## One-time setup

1. Install Python 3.8 or newer (check with `python --version`).
2. Install the three packages this report needs:

   ```
   pip install requests py7zr beautifulsoup4
   ```

   (`requirements.txt` also lists `selenium` and `lxml`, but those are only for
   the separate FIV Portal script and are not needed here.)

3. Be on the Intel network or VPN (Artifactory must be reachable).

## Normal weekly use

Double-click **`DMR_REPORT.bat`**, or run:

```
python dmr_report.py
```

It asks you to paste your release line(s). Paste one release per line, then press
Enter on an empty line:

```
> AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5
  DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.10.1.05 is trend to be released on WW10.5  dmr-rio-7 2026ww09.1.00_01 Pre500
  <empty line to start>
```

The script then, for each release:

1. Searches Artifactory for the build matching the Orange IFWI ID
2. Reads the real BIOS Binary and Unified Patch versions out of the build package
3. For Pre-Si, also pulls the Simics / IMH / CBB / SCF IPSD OSXML values
4. Writes `output/IFWI_Release_Status_<orange-id>.html` and opens it in your browser

The first run asks for your Artifactory API token and offers to remember it in
`.dmr_token`, so you only type it once.

## The release line

The parser needs three things in the sentence, in any order and any wording:

| Needs | Looks like | Notes |
|-------|-----------|-------|
| Platform | `AP1 A0`, `AP1 B0`, `AP2 A0` | `DMR-AP-UCC` / `DMR-AP-MCC` prefixes and `o`/`•` bullets are ignored |
| Orange IFWI ID | `2026.10.1.01` | |
| Release week | `... on WW10.5` | |
| Simics version | `dmr-rio-7 2026ww09.1.00_01 Pre500` | **Pre-Si only** (AP1 B0 / AP2 A0) |

Wording controls the tense in the report:

| You write | Report says |
|-----------|-------------|
| `is trend to be released on WW10.5` | is trend to be released on WW10.5 |
| `will be released on WW10.5` | will be released on WW10.5 |
| `released on WW10.5` | has been released on WW10.5 |

If a line is missing something, the script says which line and what is missing,
and still processes the other lines.

## Other ways to run it

```
# Pass releases inline instead of pasting
python dmr_report.py "AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5"

# Read releases from a file, one per line
python dmr_report.py -f releases.txt

# Use a different token without touching the saved one
python dmr_report.py --token AKCp...

# Don't pop open the browser
python dmr_report.py --no-browser

# Show help
python dmr_report.py --help
```

## When something goes wrong

| Message | What to do |
|---------|-----------|
| `No build found for Orange ID ...` | The ID is not in Artifactory yet, or it is a typo. Check the ID. |
| HTTP 403 / token errors | Token expired. Delete `.dmr_token` and re-run to enter a new one. |
| `Multiple builds found` | Two builds share the Orange ID. Run `python scripts/generate_dmr_report.py "<platform>" "<orange-id>" "<release info>"` and pick one. |
| `Simics version is required` | Pre-Si releases (AP1 B0, AP2 A0) must include the Simics version in the line. |
| Cannot reach Artifactory | Connect to the Intel network / VPN. |

## Disk cleanup

Each run downloads a build package (~150-220 MB) into a folder named after the
BIOS ID (e.g. `NNNN.D.NN/`). These are safe to delete any time:

```
rm -rf [0-9][0-9][0-9][0-9].D.*/
```

The finished reports live in `output/` and are not affected.

## What is where

| Path | Purpose |
|------|---------|
| `dmr_report.py` | **Start here.** Parses your release line, runs everything |
| `DMR_REPORT.bat` | Double-click launcher for `dmr_report.py` |
| `scripts/generate_dmr_report.py` | The pipeline itself; also usable directly with explicit arguments |
| `scripts/search_artifactory_by_orange_id.py` | Step 1 - find the build |
| `scripts/construct_artifactory_url.py` | Step 2 - locate the build package |
| `scripts/extract_artifactory_osxml.py` | Step 3 - pull out BIOS / UP / OSXML versions |
| `scripts/generate_ifwi_report.py` | Step 4 - render the HTML |
| `templates/` | Known-good reference reports to compare against |
| `output/` | Generated reports |
| `references/project-rules.md` | The extraction rules (OSXML indices, UP patterns, etc.) |
