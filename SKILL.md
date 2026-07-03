---
name: dmr-ifwi-report-generator
description: Generate DMR IFWI weekly status reports from Artifactory build packages. Use this skill when the user needs to create HTML reports for DMR-AP (UCC/MCC) platform IFWI releases, extract OSXML data from Artifactory, or automate weekly report generation for AP1 A0/B0 or AP2 A0 platforms. Triggers on keywords like "DMR report", "IFWI report", "Artifactory build", "Orange ID", "OSXML extraction", "weekly status", or "BIOS release report".
compatibility:
  tools:
    - Bash
    - Read
    - Write
    - Edit
  platforms:
    - Windows
  dependencies:
    - Python 3.8+
    - PowerShell 5.1+
    - requests
    - py7zr
---

# DMR IFWI Report Generator Skill

## What This Skill Does

Automates the generation of HTML weekly status reports for DMR IFWI (Integrated Firmware Image) releases. The skill:

1. **Searches Artifactory** for build packages by Orange ID
2. **Extracts version information** (BIOS, Simics, Unified Patch, OSXML data)
3. **Generates formatted HTML reports** with platform-specific tables
4. **Handles three platform types**: AP1 A0 (Post-Si), AP1 B0 (Pre-Si), AP2 A0 (Pre-Si)

## When to Use This Skill

Use this skill when the user wants to:

- Generate DMR IFWI weekly status reports
- Extract OSXML data from Artifactory build packages
- Create release announcements for Orange IFWI builds
- Automate report generation for AP1/AP2 platforms
- Query Artifactory for BIOS versions and component data

## Quick Start Workflow

### Step 1: Understand User Requirements

Ask the user for these key inputs:

1. **Platform/Stepping** - Which platform?
   - AP1 A0 (Post-Silicon) - Simplified report
   - AP1 B0 (Pre-Silicon) - Full report with OSXML
   - AP2 A0 (Pre-Silicon) - Full report with OSXML

2. **Orange ID** - IFWI version (format: `YYYY.WW.X.NN`)
   - Example: `2026.26.4.01`

3. **Simics Version** (Pre-Si only) - Required for AP1 B0 / AP2 A0
   - Format: `dmr-7 2026ww24.3.00_45 Pre712`
   - Or short: `2026ww24.3.00_45`

4. **Release Info** - Release status
   - Example: `released on WW26.5` or `will be released on WW26.5`

5. **API Token** - Artifactory authentication
   - Guide user to: `https://af01p-or.devtools.intel.com` → Edit Profile → API Key

### Step 2: Execute the Workflow

The main entry point is the PowerShell script:

```powershell
.\scripts\Generate-IFWI-Report-From-Artifactory.ps1
```

This script orchestrates the following Python modules:

1. **`search_artifactory_by_orange_id.py`** - Find builds by Orange ID
2. **`construct_artifactory_url.py`** - Build download URLs
3. **`extract_artifactory_osxml.py`** - Extract data from BuildPkg.7z
4. **`generate_ifwi_report.py`** - Generate HTML report

### Step 3: Understand the Output

Generated HTML report includes:

- **Release statement** with platform and version
- **BIOS Binary version**
- **Unified Patch version**
- **OSXML table** (Pre-Si only: IMH, CBB, SCF IPSD)
- **PnP/PM Recipe table** (Pre-Si only: IIO, MC, UNCORE)
- **uBIOS statement** (if applicable)

## Critical Rules and Constraints

Read `references/project-rules.md` for the complete rule set. Key rules:

### Rule 0: Simplified Workflow
User provides minimal input (4-5 items). System auto-discovers builds from Artifactory.

### Rule 0.5: Platform-Specific Reports
- **AP1 A0 Post-Si**: Simplified report (BIOS + UP only, no OSXML)
- **AP1 B0 Pre-Si**: Full report (BIOS + Simics + UP + OSXML + uBIOS)
- **AP2 A0 Pre-Si**: Full report (BIOS + Simics + UP + OSXML + uBIOS)

### Rule 0.6: Platform-Specific OSXML Extraction
IMH and CBB OSXML values contain multiple platform values separated by semicolons. Extract the correct index:

| Platform | IMH Index | CBB Index |
|----------|-----------|-----------|
| AP2 A0   | 0 (1st)   | 0 (1st)   |
| AP1 A0   | 1 (2nd)   | 2 (3rd)   |
| AP1 B0   | 2 (3rd)   | 1 (2nd)   |

### Rule 0.7: Unified Patch IMH OSXML
For Pre-Si platforms, extract IMH OSXML from Unified Patch release notes to populate the UP column in the OSXML table.

### Rule 7: Simics Rio Detection
Detect Simics path from user input string, not platform:
- If user input contains 'rio' → use `dmr-rio-7`
- Otherwise → use `dmr-7`

## Project Structure

The skill follows this directory layout:

```
dmr-ifwi-report-generator/
├── SKILL.md                 # This file (skill definition)
├── scripts/                 # Executable scripts
│   ├── Generate-IFWI-Report-From-Artifactory.ps1  # Main entry
│   ├── search_artifactory_by_orange_id.py
│   ├── construct_artifactory_url.py
│   ├── extract_artifactory_osxml.py
│   ├── generate_ifwi_report.py
│   └── [other scripts...]
├── references/              # Documentation
│   ├── project-rules.md     # Complete rule set (from CLAUDE.md)
│   ├── platform-rules.md    # Platform-specific rules
│   ├── simics-requirements.md
│   ├── artifactory-usage.md
│   └── [other guides...]
├── output/                  # Generated reports
│   └── IFWI_Release_Status_*.html
└── test/                    # Test files
    └── test_*.py
```

## Implementation Guidance

### For Simple Report Generation

If the user provides all required information:

1. Call `scripts/search_artifactory_by_orange_id.py` with Orange ID and API token
2. Use returned BIOS ID to construct Artifactory URL
3. Download BuildPkg.7z and extract OSXML data
4. Generate HTML with `scripts/generate_ifwi_report.py`

### For Complex Multi-Report Generation

If the user needs a combined report with multiple Orange IFWIs:

1. Collect data for each Orange ID
2. Use `scripts/generate_multi_ifwi_report.py` to create combined HTML

### Error Handling

Common issues and solutions:

- **Authentication Failed**: API token expired → regenerate at Artifactory
- **Build Not Found**: Orange ID doesn't exist → verify with user
- **Multiple BIOS IDs**: Multiple builds found → ask user to select
- **Network Issues**: Artifactory unreachable → check VPN/network

## Platform Naming Convention

Always use the correct platform names in reports:

- **AP1** → `DMR-AP-UCC` (Universal Compute Complex)
- **AP2** → `DMR-AP-MCC` (Memory Compute Complex)

Example outputs:
- `DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5`
- `DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.24.6.01 will be released on WW24.5`

## Unified Patch Extraction Logic

The Unified Patch (UP) version is extracted from binary filename based on platform:

| Platform | Binary Suffix | Pattern | Example |
|----------|---------------|---------|---------|
| AP1 A0 Post-Si | `VIS.bin` | 1st 8-digit hex after BIOS ID | `800009AA` |
| AP1 B0 Pre-Si | `Simics.bin` | 2nd digit = 1 (`5_1_xxxxxx`) | `51000312` |
| AP2 A0 Pre-Si | `Simics.bin` | 2nd digit = 2 (`5_2_xxxxxx`) | `52000210` |

**Critical**: Check the 2nd digit of the UP version, NOT the position in the filename.

## uBIOS Release Calculation

For Pre-Si platforms with emulation:

1. Auto-detect emulation from build data
2. Calculate uBIOS release week: **Orange week + 1 day**
   - Example: `WW26.5` → `WW26.6`
   - Cross-week: `WW26.7` → `WW27.1`
3. Generate statement: `{Platform} uBIOS based on BIOSID {BIOSID} is trend to be released on WW{week}.{day+1}`

## Release Tense Detection

Automatically detect correct tense from user input:

| User Input | Output |
|------------|--------|
| `will be released on WW26.5` | "will be released on WW26.5" |
| `released on WW26.5` | "has been released on WW26.5" |
| `has been released on WW26.5` | "has been released on WW26.5" |
| `WW26.5` | "has been released on WW26.5" (default) |

**Note**: uBIOS always uses future tense ("will be released") regardless of Orange tense.

## Common User Scenarios

### Scenario 1: Generate AP1 A0 Post-Si Report

```
User: "Generate a report for AP1 A0 Orange ID 2026.26.4.01"

Claude:
1. Collect: Platform (AP1 A0), Orange ID, Release info, API token
2. Execute: search → construct URL → extract → generate
3. Output: Simplified report (BIOS + UP only, no OSXML table)
```

### Scenario 2: Generate AP1 B0 Pre-Si Report

```
User: "I need a weekly report for AP1 B0 build 2026.25.3.01"

Claude:
1. Collect: Platform (AP1 B0), Orange ID, Simics version, Release info, API token
2. Execute: search → download → extract OSXML + Simics data → generate
3. Output: Full report with OSXML table, PnP/PM table, uBIOS statement
```

### Scenario 3: Generate Combined Multi-Orange Report

```
User: "Create a combined report for 3 Orange IFWIs"

Claude:
1. For each Orange ID: collect data (platform, version, release info)
2. Extract all data in sequence
3. Use generate_multi_ifwi_report.py to create single HTML with all sections
4. Output: Combined report with multiple release statements
```

## Testing and Validation

Test cases are available in `test/` directory:

- `test_artifactory.py` - API connectivity tests
- `test_detect_platform.py` - Platform detection logic
- `test/test_*.txt` - Sample data files

When helping users debug issues:

1. Check Python dependencies: `pip list | grep -E 'requests|py7zr'`
2. Verify API token: Test with curl/requests
3. Check platform detection: Read CSV and verify `Platform_Stepping` field
4. Validate Unified Patch extraction: Check binary filename pattern

## Advanced Features

### Multi-Orange Report Generation

Use `generate_multi_ifwi_report.py` when combining multiple Orange IFWIs:

- Aggregates all sections into one HTML
- Each Orange gets its own release statement
- Shared header with generation date
- Output filename: `DMR_Weekly_Status_Report_YYYYMMDD.html`

### Simics OSXML Extraction

For Pre-Si platforms, extract Simics OSXML data:

1. Download Simics release notes from Artifactory
2. Parse CSV for IMH/CBB OSXML versions
3. Populate "Simics OSXML" column in report table

Simics path logic (Rule 7):
- Check if user input contains 'rio' → `dmr-rio-7` or `dmr-7`

### Cleanup and Maintenance

Use `scripts/Cleanup-TempFiles.ps1` to remove temporary files:

- Downloaded .7z archives
- Extracted CSV files
- Temporary directories

## Troubleshooting Guide

### Issue: "Build not found for Orange ID"

**Solution**: 
1. Verify Orange ID format (YYYY.WW.X.NN)
2. Check if build exists in Artifactory manually
3. Ensure API token has read permissions

### Issue: "Multiple BIOS IDs found"

**Solution**:
1. Display all found BIOS IDs to user
2. Ask user to select the correct one
3. Re-run with selected BIOS ID

### Issue: "Simics OSXML not extracted"

**Solution**:
1. Verify Simics version format
2. Check if 'rio' keyword present (affects path)
3. Verify Artifactory access to Simics packages

### Issue: "Unified Patch version incorrect"

**Solution**:
1. Check binary filename pattern
2. Verify platform detection (affects UP extraction logic)
3. Ensure 2nd digit check for Pre-Si platforms

## Reference Files

For complete documentation, refer to:

- **`references/project-rules.md`** - All 7 rules in detail (previously CLAUDE.md)
- **`references/quick-start.md`** - Quick start guide (previously START_HERE.md)
- **`references/simplified-workflow.md`** - Detailed workflow steps
- **`references/artifactory-usage.md`** - Artifactory API usage
- **`references/platform-rules.md`** - Platform-specific extraction rules
- **`references/simics-requirements.md`** - Simics version requirements
- **`references/api-token-guide.md`** - How to get API token

## Key Scripts Reference

| Script | Purpose | Inputs |
|--------|---------|--------|
| `Generate-IFWI-Report-From-Artifactory.ps1` | Main workflow orchestrator | Platform, Orange ID, Simics, Release info, API token |
| `search_artifactory_by_orange_id.py` | Search builds by Orange ID | Orange ID, API token |
| `construct_artifactory_url.py` | Build Artifactory download URL | Platform, Orange ID, BIOS ID |
| `extract_artifactory_osxml.py` | Extract all data from BuildPkg | BuildPkg path, Platform, Simics version |
| `generate_ifwi_report.py` | Generate single HTML report | CSV data, Release info |
| `generate_multi_ifwi_report.py` | Generate combined HTML report | Multiple CSV files, Release info |

## Summary

This skill enables Claude to:

1. ✅ Understand DMR IFWI report requirements
2. ✅ Guide users through minimal input workflow
3. ✅ Search and download Artifactory builds automatically
4. ✅ Extract platform-specific OSXML data correctly
5. ✅ Generate properly formatted HTML reports
6. ✅ Handle edge cases (Rio detection, uBIOS calculation, tense detection)
7. ✅ Troubleshoot common issues

**Always prioritize** reading the project rules in `references/project-rules.md` before making any changes to the workflow or extraction logic. The rules are critical for correct platform detection, OSXML extraction, and report formatting.
