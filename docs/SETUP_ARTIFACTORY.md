# Setup Guide: Artifactory Data Source

## What Was Created

### New Scripts

1. **`extract_artifactory_osxml.py`** - Core extraction script
   - Downloads .7z from Artifactory with API Token authentication
   - Extracts OSXML_Version.html from archive
   - Parses HTML tables for OSXML and PnP/PM data
   - Generates CSV in same format as FIV workflow

2. **`Generate-IFWI-Report-From-Artifactory.ps1`** - User-friendly PowerShell wrapper
   - Prompts for Artifactory URL and API Token
   - Calls Python extractor
   - Generates HTML report
   - Opens report in browser

3. **`Install-Dependencies.ps1`** - Dependency installer
   - Checks Python installation
   - Installs required packages from requirements.txt

4. **`requirements.txt`** - Python dependencies
   - `requests` - HTTP downloads
   - `py7zr` - 7-Zip extraction
   - `beautifulsoup4` - HTML parsing
   - `lxml` - HTML parser backend

5. **`test_artifactory.py`** - Dependency checker
   - Tests if all packages are installed correctly

---

## Installation Steps

### Step 1: Install Python Dependencies

```powershell
# Option A: Use install script (recommended)
.\Install-Dependencies.ps1

# Option B: Manual installation
pip install -r requirements.txt
```

### Step 2: Verify Installation

```powershell
python test_artifactory.py
```

**Expected output:**
```
[OK] requests imported successfully
[OK] py7zr imported successfully
[OK] beautifulsoup4 imported successfully
[OK] lxml imported successfully
```

### Step 3: Get Artifactory API Token

1. Open Artifactory Web UI: https://af01p-or.devtools.intel.com/
2. Click your profile (top-right) → "Edit Profile"
3. Click "Generate API Key" or copy existing key
4. Save token securely

---

## Quick Start

### Generate Single IFWI Report

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

**You MUST provide (4 prompts):**
1. **Download Link** - Artifactory build package URL (.7z file)
2. **Platform/Stepping** - Select from menu (AP1 A0, AP1 B0, AP2 A0, AP2 B0)
3. **Release Info** - Format: `will be released on WWxx.x` or `released on WWxx.x`
4. **API Token** - Your Artifactory authentication token

**Why these inputs are required:**
- Platform/Stepping cannot be reliably auto-detected from Artifactory packages
- Release week is not stored in build metadata
- User knows the exact platform and release plan better than auto-detection

**Example URL:**
```
https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z
```

**Output:**
```
IFWI_Release_Status_2026.26.4.01.html
```

---

## Advanced Usage

### Use Python Script Directly

```bash
# Extract data
python extract_artifactory_osxml.py \
    "https://af01p-or.devtools.intel.com/.../BuildPkg.7z" \
    "YOUR_API_TOKEN" \
    "."

# Generate report
python generate_ifwi_report.py \
    "OSXML_Summary_2026.26.4.01.csv" \
    "release_info.txt"
```

### Combine with FIV Workflow

Both workflows generate identical CSV format, so you can mix sources:

```powershell
# From FIV (Pre-Silicon with Simics data)
.\Generate-IFWI-Report.ps1

# From Artifactory (Post-Silicon without Simics)
.\Generate-IFWI-Report-From-Artifactory.ps1

# Combine into multi-IFWI report
python generate_multi_ifwi_report.py \
    "OSXML_Summary_2026.25.3.01.csv,OSXML_Summary_2026.26.4.01.csv" \
    "release_info_multi.txt"
```

---

## Data Extraction Details

### What's Inside OSXML_Version.html?

The HTML file inside the BuildPkg.7z archive contains:

**1. OSXML Table**
```html
<table>
  <tr><th>Component</th><th>OSXML in BIOS</th><th>OSXML in Simics</th><th>Unified Patch</th></tr>
  <tr><td>IMH OSXML</td><td>Version</td><td>Version</td><td>Version</td></tr>
  <tr><td>CBB OSXML</td><td>Version</td><td>Version</td><td>Version</td></tr>
  <tr><td>SCF IPSD</td><td>Version</td><td>Version</td><td>Version</td></tr>
</table>
```

**2. PnP/PM Recipe Table**
```html
<table>
  <tr><th>Domain</th><th>PnP Version</th><th>PM Version</th></tr>
  <tr><td>IIO</td><td>26ww06</td><td>26ww06</td></tr>
  <tr><td>MC</td><td>26ww06</td><td>26ww06</td></tr>
  <tr><td>UNCORE</td><td>26ww06</td><td>26ww06</td></tr>
</table>
```

### Auto-Detected Metadata

From URL and filename patterns:
- **Orange ID**: `2026.26.4.01` (from path)
- **BIOS ID**: `0036.D54` (from path, converted from `0036.D.54`)
- **Platform**: `AP1` or `AP2` (from text "ap_post_silicon_rel" or "ap2_post_silicon_rel")
- **Stepping**: `A0` or `B0` (from page text)

---

## Troubleshooting

### Missing Dependencies Error

**Problem:**
```
ModuleNotFoundError: No module named 'py7zr'
```

**Solution:**
```powershell
pip install -r requirements.txt
```

### HTTP 403 Forbidden

**Problem:**
```
[ERROR] Authentication failed (HTTP 403)
```

**Solution:**
1. Regenerate API Token in Artifactory
2. Verify token has no extra spaces
3. Check token hasn't expired

### OSXML_Version.html Not Found

**Problem:**
```
[ERROR] OSXML_Version.html not found in archive
```

**Solution:**
1. Verify you're using BuildPkg.7z (not other .7z files)
2. Check archive contents: `7z l BuildPkg.7z`
3. Update script if HTML file has different name

### Platform Detection Failed

**Problem:**
```
Detected Platform/Stepping: None
```

**Solution:**
1. Check HTML content manually
2. Look for "AP1", "AP2", "A0", "B0" keywords
3. Update detection patterns in `extract_artifactory_osxml.py`

---

## File Structure After Setup

```
c:\Work\DMR\AI\Native DMR Weekly Report\
├── extract_artifactory_osxml.py          # NEW: Artifactory extractor
├── Generate-IFWI-Report-From-Artifactory.ps1  # NEW: PowerShell wrapper
├── Install-Dependencies.ps1              # NEW: Dependency installer
├── requirements.txt                      # NEW: Python packages
├── test_artifactory.py                   # NEW: Dependency checker
├── ARTIFACTORY_USAGE.md                  # NEW: Detailed usage guide
├── SETUP_ARTIFACTORY.md                  # NEW: This file
├── extract_fiv_table.py                  # EXISTING: FIV extractor
├── generate_ifwi_report.py               # EXISTING: Single report generator
├── generate_multi_ifwi_report.py         # EXISTING: Multi report generator
├── Generate-IFWI-Report.ps1              # EXISTING: FIV workflow
└── CLAUDE.md                             # EXISTING: Project rules
```

---

## Comparison: Two Data Sources

| Feature | FIV Portal (Original) | Artifactory (New) |
|---------|----------------------|-------------------|
| **Data Source** | Orange Report web page | Build package .7z archive |
| **Authentication** | Browser automation (Selenium) | API Token (secure) |
| **Speed** | Slower (15-30 seconds) | Faster (5-10 seconds) |
| **Simics Data** | Usually available | May not be available |
| **OSXML Data** | ✓ Available | ✓ Available |
| **PnP/PM Data** | ✓ Available | ✓ Available |
| **Best For** | Pre-Silicon releases | Post-Silicon releases |
| **Setup** | Selenium + ChromeDriver | requests + py7zr |

---

## Key Benefits

### 1. **No Browser Automation**
- No Selenium/WebDriver setup
- Faster and more reliable
- Works in headless environments

### 2. **Secure Authentication**
- API Token instead of browser cookies
- Token can be rotated easily
- No session management needed

### 3. **Identical Output**
- Same CSV format as FIV workflow
- Same HTML report generator
- Same report styling

### 4. **Flexible Integration**
- Can mix FIV and Artifactory sources
- Works with existing multi-IFWI workflow
- No changes to report generators needed

---

## Next Steps

1. **Install dependencies**: `.\Install-Dependencies.ps1`
2. **Get API Token** from Artifactory Web UI
3. **Test extraction**: `.\Generate-IFWI-Report-From-Artifactory.ps1`
4. **Compare output** with FIV workflow
5. **Update CLAUDE.md** with Artifactory workflow rules (optional)

---

## Support

- **Detailed usage**: See [ARTIFACTORY_USAGE.md](ARTIFACTORY_USAGE.md)
- **Project rules**: See [CLAUDE.md](CLAUDE.md)
- **Original workflow**: See [README.md](README.md)

---

**Created by:** Claude Code  
**Date:** 2026-06-30  
**Version:** 1.0
