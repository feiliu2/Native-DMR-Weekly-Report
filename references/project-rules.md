# DMR Weekly Report Generator - Project Rules

This document contains all constraints and rules for the IFWI Release Status Report generation system.

## Project Overview

Automated tool to generate HTML reports from **Artifactory build packages**.

**Platform Naming Convention:**
- **AP1** → `DMR-AP-UCC` (Universal Compute Complex)
- **AP2** → `DMR-AP-MCC` (Memory Compute Complex)

**Example Outputs:**
- `DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5`
- `DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.24.6.01 will be released on WW24.5`

**Key Scripts:**
- **Main Workflow:**
  - `Generate-IFWI-Report-From-Artifactory.ps1` - Main entry point (simplified)
  - `search_artifactory_by_orange_id.py` - Finds builds by Orange ID
  - `construct_artifactory_url.py` - Constructs download URL
  - `extract_artifactory_osxml.py` - Extracts data from build packages
- **Report Generation:**
  - `generate_ifwi_report.py` - Generates single Orange HTML report
  - `generate_multi_ifwi_report.py` - Generates combined multi-Orange HTML report

---

## Rule 0: Simplified Workflow - Minimal User Input

**User only needs to provide 4-5 pieces of information. System automatically finds and downloads the correct build from Artifactory.**

### Required Inputs (All Platforms)

1. **Platform/Stepping** - User selects from menu:
   - `AP1 A0` (Post-Silicon)
   - `AP1 B0` (Pre-Silicon)
   - `AP2 A0` (Pre-Silicon)

2. **Orange ID** - IFWI ID only (e.g., `2026.24.5.01`)
   - System automatically searches Artifactory for matching builds
   - If multiple BIOS IDs found, user selects from list

3. **Simics Version** - Required for Pre-Si only (AP1 B0, AP2 A0)
   - Format: `dmr-7 2026ww24.3.00_45 Pre712`
   - Or short: `2026ww24.3.00_45`

4. **Release Info** - Release status and week:
   - `will be released on WWxx.x` (future)
   - `released on WWxx.x` (past)

5. **API Token** - Artifactory authentication (prompted last with instructions)

### PowerShell Workflow

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1

# Prompts:
Step 1: Select Platform and Stepping
Options:
  1. AP1 A0 (Post-Silicon)
  2. AP1 B0 (Pre-Silicon)
  3. AP2 A0 (Pre-Silicon)
Enter number (1-3): 2

Step 2: Enter Orange ID (IFWI ID)
Format: YYYY.WW.X.NN
Example: 2026.24.5.01
Orange ID: 2026.24.5.01

Step 3: Enter Simics Version (REQUIRED for Pre-Si)
Format: dmr-7 2026ww27.0.00_45 Pre712
   or:  2026ww27.0.00_45
Simics Version: dmr-7 2026ww24.3.00_45 Pre712

Step 4: Enter release information
Examples:
  - 'will be released on WW27.3' (future release)
  - 'released on WW27.3' (past release)
Release info: released on WW27.3

Step 5: Enter Artifactory API Token
How to get API Token:
  1. Go to: https://af01p-or.devtools.intel.com/
  2. Click your username (top right) -> 'Edit Profile'
  3. Scroll to 'API Key' section
  4. Click 'Generate API Key' or 'Regenerate'
  5. Copy the token (starts with AKCp...)

API Token: ****************

# System automatically:
Searching for Orange ID: 2026.24.5.01...
Found build: BIOS ID: 0036.D54
Constructing Artifactory URL...
Downloading BuildPkg.7z...
Extracting OSXML data...
Generating HTML report...

# Output:
DMR-AP-UCC AP1 B0 Pre-Si Orange IFWI 2026.24.5.01 has been released on WW27.3
```

### Why This is Better

- ✅ **No manual URL construction** - System finds the build automatically
- ✅ **BIOS ID auto-detected** - Searches Artifactory by Orange ID
- ✅ **API Token help shown** - User gets instructions when prompted
- ✅ **Single workflow** - No "choose option 1 or 2" confusion
- ✅ **Minimal input** - Only 4-5 pieces of information needed

### Implementation

**New file:** `search_artifactory_by_orange_id.py`
- Searches Artifactory for builds matching Orange ID pattern
- Returns BIOS ID(s) for matching builds
- Handles single or multiple matches

**Modified:** `Generate-IFWI-Report-From-Artifactory.ps1`
- Step 1: Platform selection (1-3, removed AP2 B0)
- Step 2: Orange ID input
- Step 3: Simics version (if Pre-Si)
- Step 4: Release info
- Step 5: API Token (with help text)
- Step 6: Auto-search Artifactory by Orange ID
- Step 7: Auto-construct URL with found BIOS ID
- Step 8: Extract and generate report

---

## Rule 0.5: Report Types by Platform (NEW)

**Three platform types have different report formats and data extraction rules.**

---

### Type 1: AP1 A0 Post-Si (Simplified Report)

**Detection:**
- Platform/Stepping = `AP1 A0` (user-provided)
- No Simics data for IMH/CBB (OSXML_Simics = N/A)

**Report Content:**
- ✅ Release Statement: `DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5`
- ✅ BIOS Binary: `0036.D54`
- ✅ AP Unified Patch: `800009AA`
- ❌ NO OSXML table
- ❌ NO PnP/PM table
- ❌ NO uBIOS statement

**Binary:** `*_NonIPClean_Trace_DebugSigned_VIS.bin`
```
OKSDCRB1_86B_2026.26.4.01_0036.D54_800009AA_0.892.0_1P0_NonIPClean_Trace_DebugSigned_VIS.bin
                                    ^^^^^^^^ (1st 8-digit hex after BIOS ID)
```

**Why Simplified?** Post-Si uses real hardware, no Simics/OSXML data available.

---

### Type 2: AP1 B0 Pre-Si (Full Report)

**Detection:**
- Platform/Stepping = `AP1 B0` (user-provided)
- Has Simics data for IMH/CBB

**Report Content:**
- ✅ Release Statement: `DMR-AP-UCC AP1 B0 Pre-Si Orange IFWI 2026.26.6.01 has been released on WW26.5`
- ✅ BIOS Binary: `0036.D54`
- ✅ AP Unified Patch: `51000312`
- ✅ OSXML table (IMH, CBB, SCF IPSD with Simics columns)
- ✅ PnP/PM Recipe table (IIO, MC, UNCORE)
- ✅ uBIOS statement: `AP1 B0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6`

**Binary:** `*_NonIPClean_Trace_DebugSigned_Simics.bin`
```
OKSDCRB1_86B_2026.26.6.01_0036.D54_51000312_52000210_0.892.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                    ^^^^^^^^ (1st hex: 51xxxx = AP1 B0)
                                             ^^^^^^^^ (2nd hex: 52xxxx = AP2 A0)
```

**uBIOS Week Calculation:** Orange release week + 1 day (e.g., WW26.5 → WW26.6)

---

### Type 3: AP2 A0 Pre-Si (Full Report)

**Detection:**
- Platform/Stepping = `AP2 A0` (user-provided)
- Has Simics data for IMH/CBB

**Report Content:**
- ✅ Release Statement: `DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.26.6.01 has been released on WW26.5`
- ✅ BIOS Binary: `0036.D54`
- ✅ AP Unified Patch: `52000210`
- ✅ OSXML table (IMH, CBB, SCF IPSD with Simics columns)
- ✅ PnP/PM Recipe table (IIO, MC, UNCORE)
- ✅ uBIOS statement: `AP2 A0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6`

**Binary:** `*_NonIPClean_Trace_DebugSigned_Simics.bin`
```
OKSDCRB1_86B_2026.26.6.01_0036.D54_51000312_52000210_0.892.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                               ^^^^^^^^ (2nd 8-digit hex after BIOS ID)
                                    ^^^^^^^^ (1st hex is for AP1 B0)
```

**uBIOS Week Calculation:** Orange release week + 1 day (e.g., WW26.5 → WW26.6)

---

### Unified Patch Extraction Summary

| Platform | Binary Suffix | Match Method | Version Pattern | Example UP |
|----------|---------------|--------------|-----------------|------------|
| AP1 A0 Post-Si | `VIS.bin` | 1st hex value | `800009xx` | `800009AA` |
| AP1 B0 Pre-Si | `Simics.bin` | **2nd digit = 1** | **`5_1_xxxxxx`** | `51000312` |
| AP2 A0 Pre-Si | `Simics.bin` | **2nd digit = 2** | **`5_2_xxxxxx`** | `52000210` |

**CRITICAL RULE:** Check **2nd digit** of UP version, NOT position in binary!

**Extraction Logic:**
```python
# Find all 8-digit hex values after BIOS ID
match = re.search(r'_00\d{2}\.D\d+_((?:[A-F0-9]{8}_?)+)', filename)
hex_values = re.findall(r'([A-F0-9]{8})', hex_section)

# Match by 2nd digit of version number
for up_value in hex_values:
    if platform == 'AP1 B0' and up_value[1] == '1':  # 51xxxxxx
        return up_value
    elif platform == 'AP2 A0' and up_value[1] == '2':  # 52xxxxxx
        return up_value
```

---

## Rule 0.6: Platform-Specific OSXML Extraction (NEW)

**CRITICAL: IMH and CBB have DIFFERENT ordering!**

**IMH/CBB OSXML values may contain multiple platform-specific values separated by semicolons.**

### IMH Format

```
IMH2-1p0P_26ww17hRTL-OSXML;IMH-Post-1P0AD-FV;IMH1-B0-1P0N
^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^
Index 0: AP2 A0            Index 1: AP1 A0     Index 2: AP1 B0
```

### CBB Format

```
CBB_C0_26ww12b_RTL;CBB-B0_MCP_25ww48a_RTL;CBB-A0_PowerOn
^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^
Index 0: AP2 A0     Index 1: AP1 B0         Index 2: AP1 A0
```

### Extraction Rules

| Platform | IMH Index | CBB Index | Notes |
|----------|-----------|-----------|-------|
| **AP2 A0** | 0 (1st) | 0 (1st) | Same for both |
| **AP1 A0** | 1 (2nd) | **2 (3rd)** | ⚠️ Different! |
| **AP1 B0** | **2 (3rd)** | 1 (2nd) | ⚠️ Different! |

### When to Apply

- **Components:** IMH_OSXML, CBB_OSXML (both BIOS and Simics columns)
- **Not Applied to:** SCF_IPSD (single value, no semicolons)
- **Report Types:** Full reports only (AP1 B0, AP2 A0)
- **Skip:** Simplified reports (AP1 A0 Post-Si - doesn't show OSXML table)

### Implementation

```python
def extract_osxml_by_platform(osxml_value, platform):
    """Extract platform-specific value from semicolon-separated string."""
    if ';' in osxml_value:
        parts = osxml_value.split(';')
        platform_index = {
            'AP1 A0': 1,
            'AP1 B0': 2,
            'AP2 A0': 0,
        }
        idx = platform_index.get(platform, 0)
        return parts[idx].strip()
    return osxml_value
```

### Example

**Input CSV:**
```
IMH_OSXML,IMH2-1p0P_26ww17hRTL-OSXML;IMH-Post-1P0AD-FV;IMH1-B0-1P0N,N/A,N/A
```

**Output for AP2 A0:**
```html
<td>IMH2-1p0P_26ww17hRTL-OSXML</td>  ← Only 1st value
```

**Output for AP1 B0:**
```html
<td>IMH1-B0-1P0N</td>  ← Only 3rd value
```

---

## Rule 0.7: Unified Patch IMH OSXML Extraction (NEW)

**For AP1 B0 and AP2 A0, extract IMH OSXML from Unified Patch release notes to populate the Unified Patch row in OSXML table.**

### Requirements

When extracting Unified Patch version from binary filename, also extract IMH OSXML from the Unified Patch package.

### Platform-Specific URLs

| Platform | Artifactory Path |
|----------|------------------|
| **AP1 B0** | `https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/IMH1_B0_DMRAP_Unified_Patch/{UP_VERSION}/UP_DMR_AP1_B0_{UP_VERSION}_TPRODSIGNED.7z` |
| **AP2 A0** | `https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/IMH2_B0_DMRAP_Unified_Patch/{UP_VERSION}/UP_DMR_AP2_B0_{UP_VERSION}_TPRODSIGNED.7z` |

### Extraction Steps

1. **Download UP Package** - Download .7z archive from Artifactory
2. **Extract CSV** - Find and extract `_release_notes.csv` from archive
3. **Parse IMH OSXML** - Search CSV for platform-specific keyword and extract OSXML version

### Platform-Specific Search Keywords

| Platform | Search Keyword | CSV Pattern | Example Value |
|----------|----------------|-------------|---------------|
| **AP1 B0** | `imh_osxml` | `OSXML,LTM,iMH: dmr_imh_osxml-{VERSION}` | `IMH1-B0-1P0N-OSXML-1d` |
| **AP2 A0** | `dmrhub2` | `OSXML,Primecode,dmrhub2-a0-{WW}-{VERSION}` | `IMH2-1p0D_26ww03g_RTL-OSXML-1d` |

### Regex Patterns

**AP1 B0:**
```python
match = re.search(r'dmr_imh_osxml-([^,\s]+)', line, re.IGNORECASE)
# Extracts: IMH1-B0-1P0N-OSXML-1d
```

**AP2 A0:**
```python
match = re.search(r'dmrhub2-[^-]+-[^-]+-([^,\s]+)', line, re.IGNORECASE)
# Extracts: IMH2-1p0D_26ww03g_RTL-OSXML-1d
```

### CSV File Examples

**AP1 B0 - `UP_DMR_AP1_B0_51000312_TPRODSIGNED_release_notes.csv`:**
```csv
OSXML,LTM,iMH: dmr_imh_osxml-IMH1-B0-1P0N-OSXML-1d,26ww22a
```

**AP2 A0 - `UP_DMR_AP2_B0_5200020F_TPRODSIGNED_release_notes.csv`:**
```csv
OSXML,Primecode,dmrhub2-a0-26ww03g-IMH2-1p0D_26ww03g_RTL-OSXML-1d,null
OSXML,LTM,iMH: dmrhub2-a0-26ww06h-IMH2-1p0G_26ww06h_RTL-OSXML-1d,26ww16a
```

### Report Display

**Unified Patch row in OSXML table will show:**

| Component | BIOS OSXML | Simics OSXML | **Unified Patch OSXML** |
|-----------|------------|--------------|-------------------------|
| IMH OSXML | IMH1-B0-1P0N | dmr-imh-1p0n-26ww26a | **IMH1-B0-1P0N-OSXML-1d** ⭐ |

### Implementation

**Files:**
- `extract_up_imh_osxml.py` - Standalone extraction module
- `extract_artifactory_osxml.py:657-668` - Integration in main workflow (Step 4.6)

**Integration Point:**
```python
# Step 4.6: Extract IMH OSXML from Unified Patch (only for AP1 B0 / AP2 A0)
if final_platform in ['AP1 B0', 'AP2 A0'] and unified_patch_from_binary:
    from extract_up_imh_osxml import extract_imh_osxml_from_up
    
    up_imh_osxml = extract_imh_osxml_from_up(unified_patch_from_binary, final_platform, api_token, output_path)
    
    if up_imh_osxml:
        data['osxml_data']['IMH_OSXML']['up'] = up_imh_osxml
```

### When to Apply

- ✅ **AP1 B0** - Pre-Si, full OSXML table
- ✅ **AP2 A0** - Pre-Si, full OSXML table  
- ❌ **AP1 A0** - Post-Si, simplified report (no OSXML table)

### Why

Unified Patch packages contain their own IMH OSXML version in release notes. This provides complete version tracking for all three data sources (BIOS, Simics, Unified Patch) in the OSXML table.

---

## Rule 1: Orange ID Auto-Detection

**When user provides Orange Report URL, automatically extract Orange ID from the URL.**

### Detection Pattern
```
URL: https://fiv-ifwi.intel.com/test_report/report_wrap/*/Orange/2026.26.4.01/
Extract: 2026.26.4.01
```

Regex pattern: `Orange/(2026\.[^/]+)/`

### Behavior
- ✅ Automatically extract Orange ID from URL
- ✅ Display: "Auto-detected Orange ID: 2026.26.4.01"
- ⚠️ Only prompt for manual input if auto-detection fails

### User Workflow
```powershell
# User only needs to provide:
1. FIV URL
2. Release Week (e.g., WW26.5)

# Script automatically extracts:
- Orange ID (from URL)
```

**Implementation:** `extract_fiv_table.py` lines 130-133

---

## Rule 2: Conditional Table Display

**BIOS Binary and Unified Patch always shown. OSXML columns and PnP/PM table conditionally displayed.**

### Display Rules

| Data Type | Has Data | No Data |
|-----------|----------|---------|
| **BIOS Binary** | ✅ Always show | ✅ Always show |
| **Unified Patch** | ✅ Always show | ✅ Always show |
| OSXML columns | Show OSXML columns | **Remove OSXML columns** (show simplified 2-column table) |
| PnP/PM table | Show entire table | **Remove entire table** |
| Simics row | Show row | **Hide row** |

### Detection Logic
- **OSXML columns**: Check if ANY value in IMH_OSXML, CBB_OSXML, or SCF_IPSD is not N/A
  - If data exists → Show 5-column table (Version + 3 OSXML columns + SCF IPSD)
  - If no data → Show 2-column table (Version only) but keep BIOS Binary and Unified Patch rows
- **PnP/PM table**: Check if ANY value in IIO/MC/UNCORE PnP or PM is not N/A
  - If data exists → Show entire PnP/PM table
  - If no data → Completely remove PnP/PM table

### Why
- **BIOS Binary and Unified Patch are core release info** → always displayed regardless of OSXML/PnP data
- Post-Silicon releases (actual hardware) have **no OSXML/PnP data** → show clean simplified table
- Pre-Silicon releases (Simics) have complete data → show full 5-column table with OSXML columns
- Removing empty OSXML columns is cleaner than showing columns full of empty cells

### HTML Generation Logic
```python
# BIOS Binary and Unified Patch: always show, even if empty
if has_osxml:
    # Full 5-column table
    html += '''<th>Version</th><th>IMH OSXML</th><th>CBB OSXML</th><th>SCF IPSD</th>'''
else:
    # Simplified 2-column table (no OSXML columns)
    html += '''<th>Version</th>'''

# PnP/PM table: only show if has data
if has_pnp_pm:
    html += '''<p><strong>PNP and PM recipe config...</strong></p>'''
```

**Implementation:** 
- `generate_ifwi_report.py` lines 234-283
- `generate_multi_ifwi_report.py` lines 177-233

---

## Rule 3: Platform Stepping Detection

**Detect AP1/AP2 and A0/B0 stepping from Orange Report page text (NOT from BIOS ID).**

### Detection Rules

| Page Text Pattern | Result |
|-------------------|--------|
| "AP1 pre" or "AP1 Pre-Silicon" | **AP1 B0** |
| "AP1 A0 post" or "AP1 A0 post silicon" | **AP1 A0** |
| "AP2 A0 post" or "AP2 A0 post silicon" | **AP2 A0** |
| "AP2 pre" or "AP2 Pre-Silicon" | **AP2 A0** |

**CRITICAL:** BIOS ID is **NEVER** used to determine AP1 vs AP2. Only page text is authoritative.

### Examples

```
Page text: "This Orange IFWI 2026.25.3.01 is for AP1 Pre-Silicon"
Result: AP1 B0
Output: DMR-AP-UCC AP1 B0 Orange IFWI...

Page text: "This is the DMR AP1 A0 post silicon IFWI release"
Result: AP1 A0
Output: DMR-AP-UCC AP1 A0 Orange IFWI...

Page text: "This is the DMR AP2 A0 post silicon IFWI release"
Result: AP2 A0
Output: DMR-AP-MCC AP2 A0 Orange IFWI...

Page text: "This Orange IFWI 2026.24.6.01 is for AP2 Pre-Silicon"
Result: AP2 A0
Output: DMR-AP-MCC AP2 A0 Orange IFWI...
```

### Why
BIOS ID is NOT reliable for determining AP1 vs AP2:
- BIOS ID only tells us the stepping (A0/B0), not the platform (AP1/AP2)
- Page text explicitly states which platform (AP1 or AP2)
- Must search for **both** platform identifier (AP1/AP2) **and** stepping indicator (pre/post) in same text

### Fallback
If page text detection fails, try OSXML data:
- Check `IMH_OSXML` or `CBB_OSXML` BIOS field for "B0" or "A0" keywords

**Implementation:** `extract_fiv_table.py` lines 138-164, stores in CSV as `Platform_Stepping`

---

## Rule 4: uBIOS Emulation Statement

**When Orange Report contains "Emulation info", add uBIOS release statement.**

### Detection
Search page text for keywords:
- "emulation info" (case-insensitive)
- "emulation"

### Auto-Calculation
When emulation detected, **automatically calculate uBIOS release week**:
- Formula: **Orange release week + 1 day**
- Example: `WW26.5` → `WW26.6`
- Cross-week: `WW26.7` → `WW27.1`

**No user prompt needed** - fully automatic.

### Output Format
Add uBIOS statement **after PNP and PM Recipe table**:
```html
DMR-AP-UCC AP1 A0 Orange IFWI 2026.26.4.01 has been released on WW26.5

[Release version information table]
[PNP and PM recipe config table]

AP1 A0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6
```

### Template
```
{Platform} uBIOS based on BIOSID {BIOSID} is trend to be released on WW{week}.{day+1}
```

### Why
Emulation Orange releases indicate a corresponding uBIOS build is planned. uBIOS typically releases 1 day after Orange IFWI.

**Implementation:**
- Detection: `extract_fiv_table.py` lines 212-218, stores `Has_Emulation,Yes/No` in CSV
- Auto-calculation: `calculate_ubios_release_week()` function in Python report generators
- Display: PowerShell scripts show "Detected Emulation info - uBIOS release statement will be auto-generated"
- Report: `generate_ifwi_report.py` and `generate_multi_ifwi_report.py`

---

## Rule 5: Report Header Simplification

**Remove redundant information from report headers and body.**

### Removed Elements

1. **Header: Orange ID and BIOS ID line**
   - ❌ Remove: `Orange ID: 2026.26.4.01 | BIOS ID: 0036.D54`
   - ✅ Keep only: `Generated: 2026-06-29`

2. **Header: Simics version line**
   - ❌ Remove: `Simics: dmr-7 2026ww24.3.00_45 Pre712`
   - Simics info only shown in table if exists

### Why
- Orange ID already in release statement
- BIOS ID shown in uBIOS statement if applicable
- Simics version shown in table data
- Cleaner, less redundant header

### Before vs After

**Before:**
```
DMR Weekly Status Report
Generated: 2026-06-29 | Orange: 2026.26.4.01
Simics: dmr-7 2026ww24.3.00_45 Pre712

DMR-AP-UCC AP1 B0 Orange IFWI 2026.26.4.01 has been released on WW26.5
Orange ID: 2026.26.4.01 | BIOS ID: 0036.D29
```

**After:**
```
DMR Weekly Status Report
Generated: 2026-06-29

DMR-AP-UCC AP1 B0 Orange IFWI 2026.26.4.01 has been released on WW26.5

[Release version information table]
[PNP and PM recipe config table]

AP1 B0 uBIOS based on BIOSID 0036.D29 is trend to be released on WW26.6
```

**Implementation:** `generate_ifwi_report.py` and `generate_multi_ifwi_report.py`

---

## Rule 6: Release Tense Detection

**Automatically detect and use correct tense (past or future) from user input.**

### Supported Input Formats

| User Input | Detected Tense | HTML Output |
|------------|----------------|-------------|
| `will be released on WW26.5` | will be released | "will be released on WW26.5" |
| `released on WW26.5` | has been released | "has been released on WW26.5" |
| `has been released on WW26.5` | has been released | "has been released on WW26.5" |
| `WW26.5` | has been released | "has been released on WW26.5" (default) |

### Examples

**Future Release:**
```
Input: "will be released on WW26.5"
Output: DMR-AP-UCC AP1 A0 Orange IFWI 2026.26.4.01 will be released on WW26.5
```

**Past Release:**
```
Input: "released on WW25.5"
Output: DMR-AP-UCC AP1 B0 Orange IFWI 2026.25.3.01 has been released on WW25.5
```

### uBIOS Tense Rule
**uBIOS always uses "will be released"** (future tense) regardless of Orange tense, because uBIOS is always planned for future release.

### Why
Different Orange IFWIs may have different release statuses - some already released, some planned for future. The report must accurately reflect each status.

**Implementation:** PowerShell scripts parse user input with regex, Python generators use the detected tense

---

## Workflow Summary

### Single Orange IFWI
```powershell
.\Generate-IFWI-Report.ps1

# Prompts:
How many Orange IFWIs to include? 1
Enter FIV URL: https://fiv-ifwi.intel.com/.../Orange/2026.26.4.01/
Enter release info: will be released on WW26.5
Detected: will be released on WW26.5
[if emulation detected] Display: "Detected Emulation info - uBIOS release statement will be auto-generated"

# Output:
IFWI_Release_Status_2026.26.4.01.html
```

### Multiple Orange IFWIs
```powershell
.\Generate-IFWI-Report.ps1

# Prompts:
How many Orange IFWIs to include? 2
Enter FIV URL: [first Orange]
Enter release info: will be released on WW26.5
Detected: will be released on WW26.5
Enter FIV URL: [second Orange]
Enter release info: released on WW25.5
Detected: has been released on WW25.5

# Output:
DMR_Weekly_Status_Report_YYYYMMDD.html (combined report)
```

---

## CSV Data Format

Generated by `extract_fiv_table.py`:

```csv
Orange_ID,2026.26.4.01
BIOSID,0036.D54
Platform_Stepping,AP1 A0
Has_Emulation,Yes
Simics_Version,N/A

Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
IMH_OSXML,N/A,N/A,N/A
CBB_OSXML,N/A,N/A,N/A
SCF_IPSD,N/A,N/A,N/A

AP_Unified_Patch,800009AA

Domain,PnP_Version,PM_Version
IIO,26ww06,26ww06
MC,26ww06,26ww06
UNCORE,26ww06,26ww06
```

---

## File Dependencies

```
Generate-IFWI-Report.ps1
    ├─> extract_fiv_table.py (Selenium)
    │   └─> Output: OSXML_Summary_{Orange_ID}.csv
    │
    └─> [Single] generate_ifwi_report.py
        └─> Output: IFWI_Release_Status_{Orange_ID}.html
    
    └─> [Multiple] generate_multi_ifwi_report.py
        └─> Output: DMR_Weekly_Status_Report_YYYYMMDD.html
```

---

## Important Notes

1. **Auto-detection Priority:**
   - Orange ID: URL → manual prompt
   - Platform/Stepping: Page text → OSXML → manual fallback
   
2. **CSV Encoding:**
   - PowerShell writes temp files with ASCII encoding (no BOM)
   - Python reads with `utf-8-sig` to handle potential BOM

3. **Browser Automation:**
   - Uses Selenium WebDriver (Edge)
   - Requires Edge browser and matching WebDriver version

4. **HTML Output:**
   - Single Orange: Named by Orange ID
   - Multiple Oranges: Named by date, contains all sections

---

## Version History

- **2026-06-29**: Added uBIOS emulation statement, platform stepping detection
- **2026-06**: Initial implementation with auto Orange ID detection

---

**Generated by:** Claude Code
**Maintained by:** DMR IFWI Team


---

## Rule 7: Simics Path Detection (Rio Rule)

**Detect Simics Artifactory path from user input string, not from platform parameter.**

### Core Rule

**Check if user's Simics input contains 'rio' keyword:**

```python
# Simple string check (case-insensitive)
if 'rio' in simics_version.lower():
    platform_path = 'dmr-rio-7'
else:
    platform_path = 'dmr-7'
```

### Examples

| User Input | Contains 'rio'? | Simics Path |
|------------|-----------------|-------------|
| `dmr-rio-7 2026ww23.6.00_03 Pre539` | ✅ Yes | `dmr-rio-7` |
| `dmr-7 2026ww24.3.00_45 Pre712` | ❌ No | `dmr-7` |
| `2026ww25.3.00_03` | ❌ No | `dmr-7` (default) |

### Why This Rule

**Old rule (deprecated):**
- Based on platform_stepping parameter
- AP1 B0 → dmr-7, AP2 A0 → dmr-rio-7
- Not flexible

**New rule (current):**
- Based on user input string
- User has full control
- Supports special cases (e.g., AP1 B0 can use dmr-rio-7 if needed)

### Implementation

**File:** `extract_artifactory_osxml.py`  
**Function:** `download_simics_release_notes()`

```python
# Pass FULL simics_version (not just pure version number)
simics_osxml = download_simics_release_notes(simics_version, api_token, platform_stepping)

# Inside function:
if 'rio' in simics_version.lower():
    platform_path = 'dmr-rio-7'
else:
    platform_path = 'dmr-7'
    
# Extract pure version for URL
pure_version = re.search(r'(\d{4}ww\d{2}\.\d+\.\d+_\d+)', simics_version).group(1)
url = f"https://.../platforms/{platform_path}/{pure_version}/..."
```

### Tested Scenarios

✅ AP1 B0 with dmr-rio-7 → Works  
✅ AP1 B0 with dmr-7 → Works  
✅ AP2 A0 with dmr-rio-7 → Works  
✅ Case insensitive ('RIO', 'Rio') → Works

**Implementation:** `extract_artifactory_osxml.py` lines 25-55

**Documentation:** `SIMICS_RIO_RULE.md`

---

