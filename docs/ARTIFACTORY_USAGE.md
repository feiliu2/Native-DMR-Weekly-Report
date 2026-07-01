# DMR IFWI Report Generator - Artifactory Data Source

## Overview

This toolset allows you to generate DMR Weekly Status Reports from **Artifactory build packages** instead of FIV Portal Orange Report URLs.

### Data Flow

```
Artifactory Build Package (.7z)
    ↓ Download with API Token
OSXML_Version.html (extracted)
    ↓ Parse HTML tables
OSXML_Summary_{Orange_ID}.csv
    ↓ Generate report
IFWI_Release_Status_{Orange_ID}.html
```

---

## Prerequisites

### 1. Python Dependencies

Install required Python packages:

```powershell
.\Install-Dependencies.ps1
```

**Required packages:**
- `requests` - HTTP downloads from Artifactory
- `py7zr` - Extract .7z archives
- `beautifulsoup4` - Parse HTML tables
- `lxml` - HTML parser backend

### 2. Artifactory API Token

You need an Artifactory API Token for authentication.

**Get your API Token:**
1. Log in to Artifactory Web UI: https://af01p-or.devtools.intel.com/
2. Click your profile (top-right) → "Edit Profile"
3. Click "Generate API Key" or copy existing key
4. Save the token securely

---

## Usage

### Quick Start

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

**Interactive Prompts (4 steps):**

1. **Download Link** - Full path to .7z build package
   ```
   https://af01p-or.devtools.intel.com/artifactory/.../BuildPkg.7z
   ```

2. **Platform/Stepping** - Select from menu:
   - 1. AP1 A0
   - 2. AP1 B0
   - 3. AP2 A0
   - 4. AP2 B0

3. **Release Info** - Must include tense and week:
   - `will be released on WW26.5` (future)
   - `released on WW26.5` (past)

4. **API Token** - Your Artifactory authentication token

**Why Manual Input?**
- Platform/Stepping: Build packages don't reliably indicate AP1 vs AP2
- Release Info: Week/tense not in package metadata
- Accuracy: You know the exact platform and release plan

### Example Session

```
=== DMR IFWI Report Generator (Artifactory Source) ===

Enter Artifactory build package URL:
Example: https://af01p-or.devtools.intel.com/artifactory/.../BuildPkg.7z
URL: https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z

Enter your Artifactory API Token:
(Token will not be displayed)
API Token: ****************

Step 1: Extracting OSXML data from Artifactory...
Downloading from Artifactory...
[OK] Downloaded: OakStreamAPIfwi_..._BuildPkg.7z

Extracting OSXML_Version.html from archive...
[OK] Extracted: OSXML_Version.html

Parsing OSXML_Version.html...
Auto-detected Orange ID: 2026.26.4.01
Auto-detected BIOS ID: 0036.D54
Detected Platform/Stepping: AP1 A0
>>> Identified OSXML Table (Table 1)
>>> Identified PnP/PM Table (Table 2)

[OK] Generated CSV: OSXML_Summary_2026.26.4.01.csv

Step 2: Enter release information
Examples:
  - 'will be released on WW26.5' (future release)
  - 'released on WW26.5' (past release)
Release info: will be released on WW26.5

Detected: will be released on WW26.5

Step 3: Generating HTML report...
[OK] Generated report: IFWI_Release_Status_2026.26.4.01.html

=== SUCCESS ===
Generated report: IFWI_Release_Status_2026.26.4.01.html

Open report in browser? (Y/N): Y
```

---

## Artifactory URL Examples

### AP1 A0 Post-Silicon Build
```
https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z
```

### AP2 A0 Post-Silicon Build
```
https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap2_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.24.6.01.0036.D.48/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap2_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z
```

### BIOS ID Only (Alternative Source)
```
https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/BIOSID/0036.D54/0036.D54.7z
```

---

## Advanced Usage

### Command-Line Parameters

You can provide URL and token via parameters to skip prompts:

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1 `
    -ArtifactoryUrl "https://af01p-or.devtools.intel.com/.../BuildPkg.7z" `
    -ApiToken "YOUR_API_TOKEN"
```

### Using Python Script Directly

```powershell
# Step 1: Extract data from Artifactory
python extract_artifactory_osxml.py `
    "https://af01p-or.devtools.intel.com/.../BuildPkg.7z" `
    "YOUR_API_TOKEN" `
    "."

# Step 2: Generate report (same as FIV workflow)
python generate_ifwi_report.py `
    "OSXML_Summary_2026.26.4.01.csv" `
    "release_info.txt"
```

---

## What Gets Extracted from OSXML_Version.html?

### Metadata
- **Orange ID** - From filename pattern (e.g., 2026.26.4.01)
- **BIOS ID** - From path pattern (e.g., 0036.D54)
- **Platform/Stepping** - From text or path (AP1 A0, AP1 B0, AP2 A0)
- **Unified Patch** - 8-digit hex ID (e.g., 800009AA)

### OSXML Table Data
| Component | OSXML in BIOS | OSXML in Simics | Unified Patch |
|-----------|---------------|-----------------|---------------|
| IMH_OSXML | Version or N/A | Version or N/A | Version or N/A |
| CBB_OSXML | Version or N/A | Version or N/A | Version or N/A |
| SCF_IPSD | Version or N/A | Version or N/A | Version or N/A |

### PnP/PM Recipe Table
| Domain | PnP Version | PM Version |
|--------|-------------|------------|
| IIO | 26ww06 | 26ww06 |
| MC | 26ww06 | 26ww06 |
| UNCORE | 26ww06 | 26ww06 |

---

## Output Files

### Generated Files
```
OakStreamAPIfwi_..._BuildPkg.7z    # Downloaded archive
OSXML_Version.html                 # Extracted HTML
OSXML_Summary_2026.26.4.01.csv     # Parsed data (CSV)
IFWI_Release_Status_2026.26.4.01.html  # Final report
```

### CSV Format (Same as FIV Workflow)
```csv
IFWI_Type,Orange
Orange_ID,2026.26.4.01
BIOSID,0036.D54
Platform_Stepping,AP1 A0
Has_Emulation,No
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

## Troubleshooting

### HTTP 403 Forbidden
**Cause:** Invalid or expired API Token

**Solution:**
1. Regenerate API Token in Artifactory Web UI
2. Verify token is copied correctly (no extra spaces)

### HTTP 404 Not Found
**Cause:** Invalid Artifactory URL

**Solution:**
1. Verify the build package exists
2. Check URL is copied correctly from Artifactory browser
3. Ensure you have permission to access the path

### OSXML_Version.html Not Found
**Cause:** Archive doesn't contain OSXML_Version.html file

**Solution:**
1. Verify you're using the correct BuildPkg.7z file
2. Check if alternative archive names are used
3. List archive contents: `7z l BuildPkg.7z | grep -i osxml`

### Platform/Stepping Detection Fails
**Cause:** Page text doesn't contain expected patterns

**Solution:**
1. Check HTML content manually
2. Update detection patterns in `extract_artifactory_osxml.py`
3. Manually specify platform in CSV if needed

---

## Comparison: FIV Portal vs Artifactory

| Feature | FIV Portal | Artifactory |
|---------|------------|-------------|
| **Data Source** | Orange Report URL | Build Package .7z |
| **Authentication** | Browser automation | API Token |
| **Speed** | Slower (Selenium) | Faster (direct download) |
| **Reliability** | Depends on web page | Depends on archive structure |
| **Simics Data** | Available | May not be available |
| **Use Case** | Pre-Silicon releases | Post-Silicon releases |

---

## Integration with Existing Workflow

The Artifactory workflow generates **identical CSV format** to FIV workflow, so:

✅ **Same report generator** (`generate_ifwi_report.py`)
✅ **Same HTML output** (styling, structure, content)
✅ **Same multi-IFWI support** (can combine FIV + Artifactory sources)

### Multi-Source Example

```powershell
# Generate from FIV (Pre-Silicon with Simics)
.\Generate-IFWI-Report.ps1  # → OSXML_Summary_2026.25.3.01.csv

# Generate from Artifactory (Post-Silicon)
.\Generate-IFWI-Report-From-Artifactory.ps1  # → OSXML_Summary_2026.26.4.01.csv

# Combine both into multi-IFWI report
python generate_multi_ifwi_report.py `
    "OSXML_Summary_2026.25.3.01.csv,OSXML_Summary_2026.26.4.01.csv" `
    "release_info_multi.txt"
```

---

## Security Notes

### API Token Safety
- ⚠️ **Never commit API tokens to Git**
- ⚠️ **Don't share tokens in emails or chat**
- ✅ Use PowerShell secure input (token hidden)
- ✅ Store token in secure credential manager
- ✅ Regenerate tokens periodically

### Recommended Practice
```powershell
# Use Windows Credential Manager
cmdkey /add:artifactory /user:YOUR_USERNAME /pass:YOUR_TOKEN

# Retrieve in script
$cred = Get-StoredCredential -Target "artifactory"
$apiToken = $cred.GetNetworkCredential().Password
```

---

## Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Verify prerequisites are met
4. Contact DMR IFWI Team

---

**Generated by:** Claude Code
**Last Updated:** 2026-06-30
