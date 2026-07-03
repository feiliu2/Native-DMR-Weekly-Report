# Simics Version Requirements for Pre-Si IFWI

**Last Updated:** 2026-06-30

---

## Overview

For **AP1 B0** and **AP2 A0** Pre-Silicon IFWI reports, the user **MUST** provide a Simics version.

This Simics version is used to download the corresponding release notes and extract IMH/CBB OSXML versions for the Simics columns in the report.

---

## Required Input

### Simics Version Format

**Pattern:** `YYYYwwNN.X.XX_NN`

**Examples:**
- `2026ww27.0.00_45`
- `2026ww24.3.00_45`

**Regex:** `^\d{4}ww\d{2}\.\d+\.\d+_\d+$`

---

## When Simics Version is Required

| Platform | Simics Version Required? | Reason |
|----------|-------------------------|--------|
| **AP1 A0 Post-Si** | ❌ No | Post-Si uses real hardware, no Simics |
| **AP1 B0 Pre-Si** | ✅ Yes | Pre-Si uses Simics simulation |
| **AP2 A0 Pre-Si** | ✅ Yes | Pre-Si uses Simics simulation |

---

## Simics Release Notes URL

### Platform-Specific Paths

**CRITICAL:** Different platforms use different Simics paths:

| Platform | Simics Path | URL Template |
|----------|-------------|--------------|
| **AP1 B0** | `dmr-7` | `https://af02p-or.devtools.intel.com/.../platforms/dmr-7/{VERSION}/...` |
| **AP2 A0** | `dmr-rio-7` | `https://af02p-or.devtools.intel.com/.../platforms/dmr-rio-7/{VERSION}/...` |

### Full URL Templates

**AP1 B0:**
```
https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-7/{SIMICS_VERSION}/release_notes/daily_release_notification.md
```

**AP2 A0:**
```
https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-rio-7/{SIMICS_VERSION}/release_notes/daily_release_notification.md
```

### Examples

**AP1 B0 - Simics Version:** `2026ww27.0.00_45`
```
https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-7/2026ww27.0.00_45/release_notes/daily_release_notification.md
```

**AP2 A0 - Simics Version:** `2026ww23.6.00_03`
```
https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-rio-7/2026ww23.6.00_03/release_notes/daily_release_notification.md
```

---

## Download and Extraction Process

### Step 1: Download Release Notes

```python
headers = {
    "X-JFrog-Art-Api": api_token
}

response = requests.get(url, headers=headers)
markdown_content = response.text
```

### Step 2: Parse Markdown Content

Look for lines containing:
- `IMH2 regs:` → Extract IMH OSXML version
- `CBB regs:` → Extract CBB OSXML version

**Example content:**
```markdown
IMH2 regs: **dmr-imh2-1p0p-26ww17h**
CBB regs: **dmr-cbb-g0-26ww20a**
```

**Note:** The `**` markdown bold markers are automatically stripped during extraction.

### Step 3: Extract Versions

```python
for line in markdown_content.split('\n'):
    # Look for "IMH2 regs:" pattern
    if 'IMH2 regs:' in line or 'imh2 regs:' in line.lower():
        # Extract: dmr-imh2-1p0p-26ww17h (without ** markers)
        match = re.search(r'regs:\s*\*{0,2}([a-z0-9\-]+)\*{0,2}', line, re.IGNORECASE)
        imh_osxml = match.group(1).strip()
    
    # Look for "CBB regs:" pattern
    if 'CBB regs:' in line or 'cbb regs:' in line.lower():
        # Extract: dmr-cbb-g0-26ww20a (without ** markers)
        match = re.search(r'regs:\s*\*{0,2}([a-z0-9\-]+)\*{0,2}', line, re.IGNORECASE)
        cbb_osxml = match.group(1).strip()
```

### Step 4: Populate Simics Columns

Extracted OSXML versions are placed in the **Simics column** of the OSXML table:

| Component | Version | IMH OSXML (BIOS) | CBB OSXML (BIOS) | IMH OSXML (Simics) | CBB OSXML (Simics) |
|-----------|---------|------------------|------------------|--------------------|--------------------|
| BIOS Binary | 0036.D54 | IMH1-B0-1P0N | CBB-B0_MCP... | dmr-imh2-1p0p-26ww17h | dmr-cbb-g0-26ww20a |

---

## User Workflow

### PowerShell Prompt Sequence

**For AP1 B0 or AP2 A0:**

```
Step 1: Enter Artifactory build package URL
Download Link: https://...

Step 2: Select Platform and Stepping
Enter number (1-4): 2 (AP1 B0)
Platform/Stepping: AP1 B0

Step 2.5: Enter Simics Version (REQUIRED for Pre-Si)  ← NEW STEP
Format: 2026ww27.0.00_45
This will be used to fetch OSXML information from Simics release notes
Simics Version: 2026ww27.0.00_45

Step 3: Enter release information
Release info: will be released on WW27.2

Step 4: Enter Artifactory API Token
API Token: ****************
```

**For AP1 A0:**

```
Step 1: Enter Artifactory build package URL
Step 2: Select Platform and Stepping → AP1 A0
[No Simics prompt - skipped automatically]
Step 3: Enter release information
Step 4: Enter API Token
```

---

## Implementation Details

### PowerShell Script Changes

**File:** `Generate-IFWI-Report-From-Artifactory.ps1`

```powershell
# After Platform selection
if ($PlatformStepping -in @("AP1 B0", "AP2 A0")) {
    $SimicsVersion = Read-Host "Simics Version"
    
    # Validate format
    if ($SimicsVersion -notmatch '^\d{4}ww\d{2}\.\d+\.\d+_\d+$') {
        Write-Host "[ERROR] Invalid Simics version format"
        exit 1
    }
}

# Pass to Python
python extract_artifactory_osxml.py $Url $Token "." $Platform $SimicsVersion
```

### Python Script Changes

**File:** `extract_artifactory_osxml.py`

**New Functions:**
```python
def download_simics_release_notes(simics_version, api_token):
    """Download and parse Simics release notes markdown file."""
    url = f"https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-7/{simics_version}/release_notes/daily_release_notification.md"
    # Download and return parsed OSXML data

def extract_osxml_from_simics_md(markdown_content):
    """Parse markdown to extract IMH/CBB OSXML versions.
    
    Search patterns:
    - "IMH2 regs:" → extract IMH OSXML (e.g., dmr-imh2-1p0p-26ww17h)
    - "CBB regs:" → extract CBB OSXML (e.g., dmr-cbb-g0-26ww20a)
    
    Note: Automatically strips ** markdown bold markers
    """
    # Search for IMH2 regs: and CBB regs: patterns
    # Return extracted versions without ** markers
```

**Main Flow:**
```python
# If Simics version provided for Pre-Si
if simics_version and platform in ['AP1 B0', 'AP2 A0']:
    simics_osxml = download_simics_release_notes(simics_version, api_token)
    
    # Merge into data structure
    data['osxml_data']['IMH_OSXML']['simics'] = simics_osxml['IMH_OSXML']
    data['osxml_data']['CBB_OSXML']['simics'] = simics_osxml['CBB_OSXML']
```

---

## CSV Output

**With Simics Version:**

```csv
IFWI_Type,Orange
Orange_ID,2026.26.6.01
BIOSID,0036.D54
Platform_Stepping,AP1 B0
Has_Emulation,No
Simics_Version,dmr-7 2026ww27.0.00_45
Simplified_Report,No

Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
IMH_OSXML,IMH1-B0-1P0N,dmr-imh2-1p0p-26ww17h,N/A
CBB_OSXML,CBB-B0_MCP_25ww48a_RTL,dmr-cbb-g0-26ww20a,N/A
...
```

**Key Differences:**
- `Simics_Version` populated with `dmr-7 {version}`
- `OSXML_Simics` column populated with values from Simics release notes

---

## Error Handling

### Missing Simics Version

**Condition:** User selects AP1 B0 or AP2 A0 but doesn't provide Simics version

**Action:** PowerShell script requires input, won't proceed without it

**Result:** Report generation blocked until Simics version provided

### Invalid Simics Version Format

**Condition:** Simics version doesn't match pattern `YYYYwwNN.X.XX_NN`

**Error Message:**
```
[ERROR] Invalid Simics version format
Expected format: YYYYwwNN.X.XX_NN (e.g., 2026ww27.0.00_45)
```

### Simics Release Notes Not Found

**Condition:** HTTP 404 when downloading release notes

**Warning Message:**
```
[ERROR] Simics release notes not found (HTTP 404)
Version '2026ww27.0.00_45' may not exist or URL is incorrect
```

**Fallback:** Simics OSXML columns show N/A, report still generates

### No OSXML Found in Release Notes

**Condition:** Downloaded successfully but no IMH/CBB OSXML lines found

**Warning Message:**
```
[WARN] No IMH/CBB OSXML versions found in Simics release notes
```

**Fallback:** Simics OSXML columns show N/A

---

## Testing

### Test Case 1: AP1 B0 with Valid Simics Version

**Input:**
- Platform: AP1 B0
- Simics: `2026ww27.0.00_45`

**Expected:**
- ✅ Downloads release notes from Artifactory
- ✅ Extracts IMH/CBB OSXML versions
- ✅ Populates Simics columns in report
- ✅ Shows `Simics_Version: dmr-7 2026ww27.0.00_45`

### Test Case 2: AP2 A0 with Valid Simics Version

**Input:**
- Platform: AP2 A0
- Simics: `2026ww24.3.00_45`

**Expected:**
- ✅ Downloads release notes
- ✅ Extracts IMH/CBB OSXML (uses index 0 for platform-specific extraction)
- ✅ Full report with Simics data

### Test Case 3: AP1 A0 (No Simics)

**Input:**
- Platform: AP1 A0
- Simics: (not prompted)

**Expected:**
- ✅ Skips Simics prompt
- ✅ Generates simplified report
- ✅ No Simics columns shown

---

## Summary

| Step | Platform | Simics Required | Action |
|------|----------|-----------------|--------|
| 1 | All | N/A | Provide Download Link |
| 2 | All | N/A | Select Platform (AP1 A0/B0, AP2 A0) |
| **2.5** | **AP1 B0, AP2 A0** | **✅ Yes** | **Provide Simics Version** |
| 3 | All | N/A | Provide Release Info |
| 4 | All | N/A | Provide API Token |

**Simics version enables:**
- Complete OSXML table with Simics columns
- Accurate Pre-Si simulation information
- Professional, data-complete reports

---

**End of Simics Requirements Document**
