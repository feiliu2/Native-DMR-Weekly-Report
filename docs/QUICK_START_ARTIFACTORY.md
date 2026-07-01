# Quick Start: Artifactory Workflow

## 🚀 User Input Requirements

**You must provide THREE pieces of information:**

1. **Download Link** - Artifactory build package URL (.7z file)
2. **Platform/Stepping** - Select from menu: AP1 A0, AP1 B0, AP2 A0, AP2 B0
3. **Release Info** - Format: `will be released on WWxx.x` or `released on WWxx.x`

**Why?** These cannot be reliably auto-detected from Artifactory packages, so you provide them for accuracy.

### 🎯 Special: AP1 A0 Post-Si Simplified Report

**If you select AP1 A0:**
- Report will automatically detect Post-Si mode (no Simics data)
- Generates simplified report with **BIOS Binary + Unified Patch only**
- No OSXML or PnP/PM tables (not applicable for Post-Si)
- Unified Patch extracted from binary filename automatically

**Example Output:**
```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

Release version information:
┌──────────────────┬───────────┐
│ BIOS Binary      │ 0036.D54  │
│ AP Unified Patch │ 800009AA  │
└──────────────────┴───────────┘
```

---

## 📋 Setup Steps

### Step 1: Install Dependencies (First Time Only)

**If you're at Intel and pip doesn't work:**

```powershell
# Option A: Try with proxy
$env:HTTP_PROXY = "http://proxy-dmz.intel.com:911"
$env:HTTPS_PROXY = "http://proxy-dmz.intel.com:912"
pip install py7zr beautifulsoup4 lxml

# Option B: Ask IT for correct proxy/mirror settings

# Option C: Manual download (if network blocked)
# Download wheel files from another machine and transfer:
# - py7zr-0.20.0-py3-none-any.whl
# - beautifulsoup4-4.12.0-py3-none-any.whl  
# - lxml-4.9.0-cp314-win_amd64.whl
pip install *.whl
```

### Step 2: Get Artifactory API Token

1. Open https://af01p-or.devtools.intel.com/ (or your Artifactory server)
2. Click profile icon (top-right) → "Edit Profile"
3. Click "Generate API Key" or copy existing
4. Save token securely

### Step 3: Run Report Generator

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

**You'll be prompted for:**
1. **Artifactory URL** (the .7z build package)
2. **API Token** (from Step 2)
3. **Release info** (e.g., "will be released on WW26.5")

**Output:** `IFWI_Release_Status_{Orange_ID}.html`

---

## 📋 Example Session

```
=== DMR IFWI Report Generator (Artifactory Source) ===

Step 1: Enter Artifactory build package URL
Example: https://af01p-or.devtools.intel.com/artifactory/.../BuildPkg.7z
Download Link: https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z

Step 2: Select Platform and Stepping
Options:
  1. AP1 A0
  2. AP1 B0
  3. AP2 A0
  4. AP2 B0
Enter number (1-4): 1
Platform/Stepping: AP1 A0

Step 3: Enter release information
Examples:
  - 'will be released on WW26.5' (future release)
  - 'released on WW26.5' (past release)
Release info: released on WW26.5
Release: has been released on WW26.5

Step 4: Enter Artifactory API Token
(Token will not be displayed)
API Token: ****************

=== Processing ===

Downloading and extracting OSXML data...
[OK] Downloaded: BuildPkg.7z

Extracting OSXML_Version.html from archive...
[OK] Extracted: OSXML_Version.html

Parsing OSXML_Version.html...
Auto-detected Orange ID from URL: 2026.26.4.01
Auto-detected BIOS ID from URL: 0036.D54
>>> Identified OSXML Table (Table 1)
>>> Identified PnP/PM Table (Table 2)
Using user-provided platform/stepping: AP1 A0

[OK] Data extraction complete
Orange ID: 2026.26.4.01

Generating HTML report...
[OK] Generated IFWI Release Status HTML: IFWI_Release_Status_2026.26.4.01.html

=== SUCCESS ===
Generated report: IFWI_Release_Status_2026.26.4.01.html

Summary:
  Platform: AP1 A0
  Orange ID: 2026.26.4.01
  Release: has been released on WW26.5

Report opened in browser
```

---

## 🆚 When to Use Which Workflow

| Use Case | Workflow | Reason |
|----------|----------|--------|
| Pre-Silicon release with Simics data | **FIV Portal** | FIV has complete Simics info |
| Post-Silicon release | **Artifactory** ⭐ | Faster, no Simics needed |
| Need both Pre and Post in one report | **Both → Multi-IFWI** | Generate CSVs separately, then combine |
| Quick test/validation | **Artifactory** ⭐ | Faster download + parse |
| Network issues with Artifactory | **FIV Portal** | Selenium works with browser auth |

---

## 🔧 Troubleshooting Quick Fixes

### Can't install Python packages?

```powershell
# Check Python installed
python --version

# Try with --user flag
pip install --user py7zr beautifulsoup4 lxml

# Still failing? See INSTALL_TROUBLESHOOTING.md
```

### HTTP 403 when downloading?

- **Check:** API Token is correct (no spaces)
- **Try:** Regenerate token in Artifactory Web UI
- **Verify:** You have permission to access the build package

### OSXML_Version.html not found?

- **Check:** You're using BuildPkg.7z (not other .7z files)
- **Try:** List archive contents: `7z l BuildPkg.7z | grep -i osxml`
- **Alternative:** Extract manually and point script to HTML file

### Platform detection failed?

- **Check:** HTML file manually for "AP1"/"AP2" keywords
- **Fallback:** Edit CSV file and add Platform_Stepping manually
- **Report issue:** Save HTML and share for pattern update

---

## 📚 Full Documentation

- **[SETUP_ARTIFACTORY.md](SETUP_ARTIFACTORY.md)** - Complete setup guide
- **[ARTIFACTORY_USAGE.md](ARTIFACTORY_USAGE.md)** - Detailed usage examples
- **[INSTALL_TROUBLESHOOTING.md](INSTALL_TROUBLESHOOTING.md)** - Network/proxy issues
- **[CLAUDE.md](CLAUDE.md)** - Project rules and conventions

---

## ⚡ Advanced: Direct Python Usage

If you prefer command-line control:

```bash
# Step 1: Extract data
python extract_artifactory_osxml.py \
    "https://af01p-or.devtools.intel.com/.../BuildPkg.7z" \
    "YOUR_API_TOKEN" \
    "."

# Step 2: Create release info file
echo "will be released on WW26.5" > release_info.txt

# Step 3: Generate report
python generate_ifwi_report.py \
    "OSXML_Summary_2026.26.4.01.csv" \
    "release_info.txt"
```

---

## 🎯 Key Features

✅ **Auto-detection** - Orange ID, BIOS ID, Platform from URL/content  
✅ **Same CSV format** - Compatible with existing FIV workflow  
✅ **Fast** - Direct download (5-10 sec vs 15-30 sec for Selenium)  
✅ **Secure** - API Token auth (no browser cookies)  
✅ **Flexible** - Works with both Pre-Silicon and Post-Silicon builds  

---

**Need Help?** Check [INSTALL_TROUBLESHOOTING.md](INSTALL_TROUBLESHOOTING.md) or contact DMR IFWI Team

**Last Updated:** 2026-06-30
