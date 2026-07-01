# DMR IFWI Report Generator - Complete Constraints and Rules

**Last Updated:** 2026-06-30  
**Version:** 2.0

---

## 📋 Table of Contents

1. [Artifactory Workflow Input Requirements](#constraint-1-artifactory-workflow-input-requirements)
2. [AP1 A0 Post-Si Simplified Report](#constraint-2-ap1-a0-post-si-simplified-report)
3. [Data Extraction Rules](#constraint-3-data-extraction-rules)
4. [Report Generation Rules](#constraint-4-report-generation-rules)
5. [Platform Naming Conventions](#constraint-5-platform-naming-conventions)

---

## Constraint 1: Artifactory Workflow Input Requirements

### User MUST Provide Three Inputs

When using Artifactory as data source, the user **must explicitly provide** the following information:

#### 1.1 Download Link
- **Format:** Full Artifactory build package URL ending with `.7z`
- **Example:**
  ```
  https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z
  ```

#### 1.2 Platform/Stepping
- **Method:** User selects from menu (1-4)
- **Options:**
  1. AP1 A0
  2. AP1 B0
  3. AP2 A0
  4. AP2 B0
- **Why Required:** Cannot be reliably auto-detected from Artifactory build packages
- **Implementation:** Passed to `extract_artifactory_osxml.py` and stored in CSV

#### 1.3 Release Information
- **Format:** Must include tense and work week
- **Accepted Formats:**
  - `will be released on WW26.5` (future release)
  - `released on WW26.5` (past release, converts to "has been released")
  - `has been released on WW26.5` (past release, explicit)
- **Why Required:** Release week is not stored in build package metadata
- **Implementation:** Parsed by PowerShell script, passed to report generator

### Rationale

❌ **Auto-detection is unreliable for Artifactory:**
- Platform (AP1/AP2) cannot be determined from file structure alone
- Release week is planning data, not build data

✅ **User knows best:**
- User has direct knowledge of platform target
- User knows the planned release schedule
- Eliminates guessing and errors

---

## Constraint 2: AP1 A0 Post-Si Simplified Report

### 2.1 Detection Criteria

AP1 A0 Post-Si is automatically detected when:
- **Platform/Stepping** = `AP1 A0` (user-provided)
- **No Simics data** for IMH/CBB (OSXML_Simics = N/A or empty)

### 2.2 Simplified Report Content

#### ✅ MUST Show:

**Release Statement:**
```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5
```

**Release Version Information Table:**
```
┌─────────────────────┬───────────┐
│ BIOS Binary         │ 0036.D54  │
│ AP Unified Patch    │ 800009AA  │
└─────────────────────┴───────────┘
```

#### ❌ MUST NOT Show:

- OSXML table (IMH OSXML, CBB OSXML, SCF IPSD columns)
- PnP/PM Recipe table (IIO, MC, UNCORE)

### 2.3 Why Simplified Report?

- AP1 A0 Post-Si uses **real hardware** (not simulation)
- **No OSXML data** available (hardware-based testing, not Simics)
- Only **BIOS Binary** and **Unified Patch** are relevant for Post-Si releases
- Cleaner, focused report without empty/N/A tables

---

## Constraint 3: Data Extraction Rules

### 3.1 Orange ID Extraction

**Source:** Artifactory URL path

**Pattern:** `2026.\d+.\d+.\d+`

**Example:**
```
URL: .../OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/...
Extract: 2026.26.4.01
```

**Regex:** `(2026\.\d+\.\d+\.\d+)`

### 3.2 BIOS ID Extraction

**Source:** Artifactory URL path (PRIMARY METHOD)

**Pattern:** `00\d{2}\.D\.\d+`

**Example:**
```
URL: .../OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/...
Extract: 0036.D.54
Convert: 0036.D54 (remove middle dot)
```

**Regex:** `(00\d{2}\.D\.\d+)`

**Transformation:** Remove middle dot → `0036.D.54` → `0036.D54`

**Implementation:**
```python
url_bios_match = re.search(r'(00\d{2}\.D\.\d+)', artifactory_url)
if url_bios_match:
    bios_id = url_bios_match.group(1).replace('.D.', '.D')
```

### 3.3 Unified Patch Extraction

**Source:** Binary filename inside .7z archive

**Target Binary:** Must end with `NonIPClean_Trace_DebugSigned_VIS.bin`

**Exclusions:** Must NOT contain:
- `_2S` suffix
- `_IFWI_OEMID` suffix

**Example:**
```
Binary: OKSDCRB1_86B_2026.26.4.01_0036.D54_800009AA_0.892.0_1P0_NonIPClean_Trace_DebugSigned_VIS.bin
                                            ^^^^^^^^
                                            Extract this
```

**Pattern:** 8-digit hex immediately after BIOS ID

**Regex:** `_00\d{2}\.D\d+_([A-F0-9]{8})_`

**Implementation:**
```python
# Search for specific binary suffix
if filename.endswith('NonIPClean_Trace_DebugSigned_VIS.bin'):
    # Extract 8-digit hex after BIOS ID
    match = re.search(r'_00\d{2}\.D\d+_([A-F0-9]{8})_', filename, re.IGNORECASE)
    if match:
        unified_patch = match.group(1).upper()
```

### 3.4 Platform/Stepping

**Source:** User input (mandatory)

**Why not auto-detected:**
- Artifactory build packages do not reliably indicate AP1 vs AP2
- URL path may contain misleading indicators
- User knows the exact target platform

**Storage:** Written to CSV as `Platform_Stepping,AP1 A0`

---

## Constraint 4: Report Generation Rules

### 4.1 Post-Si vs Pre-Si Detection

**Logic:**
```python
# Post-Si: No Simics data for IMH/CBB
has_simics = (
    (data['simics_version'] and data['simics_version'] not in ['N/A', 'NA', '']) or
    data['osxml'].get('IMH_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA', ''] or
    data['osxml'].get('CBB_OSXML', {}).get('simics', 'N/A') not in ['N/A', 'NA', '']
)

silicon_type = 'Pre-Si' if has_simics else 'Post-Si'
```

**Note:** SCF_IPSD Simics data is **ignored** for silicon type detection

### 4.2 Release Statement Format

**Template:**
```
DMR-AP-{UCC|MCC} {Platform} {Stepping} {Silicon-Type} Orange IFWI {Orange-ID} {Tense} on WW{Week}.{Day}
```

**Example:**
```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5
```

**Components:**
- **DMR-AP-UCC** or **DMR-AP-MCC** (based on Platform)
- **AP1/AP2** (Platform)
- **A0/B0** (Stepping)
- **Post-Si** or **Pre-Si** (Silicon Type)
- **Orange IFWI** (IFWI Type)
- **2026.26.4.01** (Orange ID)
- **has been released** or **will be released** (Tense)
- **WW26.5** (Work Week)

### 4.3 Simplified Report Generation

**Conditions for Simplified Report:**
```python
simplified_report = (
    data.get('platform_stepping') == 'AP1 A0' and
    data['osxml_data'].get('IMH_OSXML', {}).get('simics') in [None, 'N/A', ''] and
    data['osxml_data'].get('CBB_OSXML', {}).get('simics') in [None, 'N/A', '']
)
```

**CSV Flag:** `Simplified_Report,Yes`

**HTML Output:**
- **Show:** Release Statement + 2-row table (BIOS Binary, Unified Patch)
- **Hide:** OSXML table, PnP/PM table

---

## Constraint 5: Platform Naming Conventions

### 5.1 Platform Mapping

| Platform Code | Full Name | Description |
|---------------|-----------|-------------|
| AP1 | DMR-AP-UCC | Universal Compute Complex |
| AP2 | DMR-AP-MCC | Memory Compute Complex |

### 5.2 Stepping Codes

| Code | Description |
|------|-------------|
| A0 | First silicon revision |
| B0 | Second silicon revision |

### 5.3 Silicon Type

| Type | Description | Simics Data |
|------|-------------|-------------|
| Post-Si | Post-Silicon (real hardware) | No (IMH/CBB Simics = N/A) |
| Pre-Si | Pre-Silicon (simulation) | Yes (IMH/CBB Simics present) |

---

## Constraint 6: File and Data Format

### 6.1 CSV Format

**Header Section:**
```csv
IFWI_Type,Orange
Orange_ID,2026.26.4.01
BIOSID,0036.D54
Platform_Stepping,AP1 A0
Has_Emulation,No
Simics_Version,N/A
Simplified_Report,Yes
```

**OSXML Section:**
```csv
Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
IMH_OSXML,<value>,N/A,N/A
CBB_OSXML,<value>,N/A,N/A
SCF_IPSD,N/A,N/A,N/A
```

**Unified Patch:**
```csv
AP_Unified_Patch,800009AA
```

**PnP/PM Section:**
```csv
Domain,PnP_Version,PM_Version
IIO,26ww06,26ww06
MC,26ww06,26ww06
UNCORE,26ww06,26ww06
```

### 6.2 HTML Output Format

**Title:** `{Platform} {Stepping} IFWI Release Status`

**Header:**
```html
<div class="report-header">
    <h1>DMR Weekly Status Report</h1>
    <p><strong>Generated:</strong> 2026-06-30</p>
</div>
```

**Release Statement:**
```html
<p style="color: #2c3e50; font-size: 18px; font-weight: bold;">
    <strong>DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5</strong>
</p>
```

---

## Constraint 7: Validation and Error Handling

### 7.1 Required Fields Validation

**Before CSV generation:**
- ✅ Orange ID must be extracted (from URL)
- ✅ BIOS ID should be extracted (from URL, fallback to N/A)
- ✅ Platform/Stepping must be provided by user
- ✅ Unified Patch should be extracted (from binary, fallback to N/A)

### 7.2 Error Messages

**Orange ID Not Found:**
```
[ERROR] Orange ID not found, cannot generate CSV
```

**Binary Not Found:**
```
[WARN] No Unified Patch found in binary with suffix: NonIPClean_Trace_DebugSigned_VIS.bin
```

**OSXML_Version.html Not Found:**
```
[ERROR] OSXML_Version.html not found in archive.
Archive contains X files:
  - file1.bin
  - file2.xml
  ...
```

---

## Constraint 8: PowerShell Workflow

### 8.1 Interactive Prompts (4 Steps)

**Step 1: Download Link**
```powershell
Enter Artifactory build package URL
Download Link: https://...
```

**Step 2: Platform/Stepping**
```powershell
Select Platform and Stepping
Options:
  1. AP1 A0
  2. AP1 B0
  3. AP2 A0
  4. AP2 B0
Enter number (1-4): 1
Platform/Stepping: AP1 A0
```

**Step 3: Release Info**
```powershell
Enter release information
Examples:
  - 'will be released on WW26.5' (future release)
  - 'released on WW26.5' (past release)
Release info: released on WW26.5
Release: has been released on WW26.5
```

**Step 4: API Token**
```powershell
Enter Artifactory API Token
(Token will not be displayed)
API Token: ****************
```

### 8.2 Input Validation

**URL Validation:**
- Must contain `.7z` extension
- Should be Artifactory domain

**Platform Selection:**
- Must be 1, 2, 3, or 4
- Maps to AP1 A0, AP1 B0, AP2 A0, AP2 B0

**Release Info Validation:**
- Must match pattern: `(will be released|released|has been released) on WW\d+\.\d+`
- Auto-converts "released on" to "has been released on"

---

## Summary Checklist

### For AP1 A0 Post-Si Report Generation:

- [ ] User provides Download Link (Artifactory URL)
- [ ] User selects Platform: AP1 A0
- [ ] User provides Release Info (e.g., "released on WW26.5")
- [ ] User provides API Token
- [ ] Script downloads .7z package
- [ ] Script extracts BIOS ID from URL (0036.D54)
- [ ] Script extracts Unified Patch from binary filename (800009AA)
- [ ] Script detects Post-Si mode (no IMH/CBB Simics data)
- [ ] Script sets Simplified_Report = Yes
- [ ] Report shows ONLY: Release Statement + BIOS Binary + Unified Patch
- [ ] Report does NOT show: OSXML table, PnP/PM table

### Key Files:

- **extract_artifactory_osxml.py** - Data extraction from Artifactory
- **generate_ifwi_report.py** - HTML report generation
- **Generate-IFWI-Report-From-Artifactory.ps1** - User interface
- **OSXML_Summary_{Orange_ID}.csv** - Intermediate data format
- **IFWI_Release_Status_{Orange_ID}.html** - Final output

---

**End of Constraints Document**

For implementation details, see:
- [CLAUDE.md](CLAUDE.md) - Complete project rules
- [RULES_SUMMARY.md](RULES_SUMMARY.md) - Quick reference
- [QUICK_START_ARTIFACTORY.md](QUICK_START_ARTIFACTORY.md) - Usage guide
