# Simplified Workflow - Generate Report from Platform + Version

**New Feature:** No need to provide full Artifactory URL anymore!

---

## Quick Start

### Before (Old Way)
```powershell
# You had to manually find and copy the full URL
.\Generate-IFWI-Report-From-Artifactory.ps1

Download Link: https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z
```

### Now (New Way) ⭐
```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1

Choose input method:
  1. Simple mode - Platform + Version (Recommended)  ← Choose this!
  2. Direct URL - Full Artifactory URL

Enter choice: 1

Select Platform:
  1. AP1 A0 (Post-Silicon)
  2. AP1 B0 (Pre-Silicon)
  3. AP2 A0 (Pre-Silicon)

Enter number: 1

Enter IFWI ID and BIOS ID:
Format: IFWI_ID.BIOS_ID
Example: 2026.26.4.01.0036.D.54
Version: 2026.26.4.01.0036.D.54

Enter API Token: ***************

✅ System automatically finds the correct URL and generates the report!
```

---

## How It Works

### Step 1: You Provide Simple Information
```
Platform: AP1 A0
Version: 2026.26.4.01.0036.D.54
```

### Step 2: System Constructs URL Automatically

**For AP1 A0 (Post-Silicon):**
```
Base: https://af01p-or.devtools.intel.com/artifactory/.../Daily/OakStreamAPIfwi/
Path: ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/
Folder: OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/
File: (queried via API) → OakStreamAPIfwi_ap_post_silicon_rel_..._123_BuildPkg.7z
```

**For AP1 B0 / AP2 A0 (Pre-Silicon):**
```
Path: ap_pre_silicon_rel/OAKSTREAMAP.0.RPB.{VERSION}/
Folder: OakStreamRp_DMR_FSP_Glue_Debug_Linux/
File: (queried via API) → OakStreamAPIfwi_ap_pre_silicon_rel_..._90_BuildPkg.7z
```

### Step 3: System Generates Report

Same as before - extracts OSXML data and generates HTML report.

---

## Version Format

**Format:** `IFWI_ID.BIOS_ID`

### Examples

| Input | IFWI ID | BIOS ID |
|-------|---------|---------|
| `2026.26.4.01.0036.D.54` | `2026.26.4.01` | `0036.D.54` |
| `2026.25.3.01.0036.D.29` | `2026.25.3.01` | `0036.D.29` |
| `2026.26.4.02.0036.D.54` | `2026.26.4.02` | `0036.D.54` |

**Alternative format** (space-separated):
```
2026.26.4.01 0036.D.54
```

---

## Complete Example

### Input
```
Platform: AP1 B0
Version: 2026.25.3.01.0036.D.29
Release: released on WW25.5
Simics: dmr-7 2026ww24.3.00_45 Pre712
API Token: ***************
```

### What Happens

1. **URL Construction** (automatic)
   ```
   Constructing Artifactory URL...
   Platform: AP1 B0
   IFWI ID: 2026.25.3.01
   BIOS ID: 0036.D.29
   Release Type: Pre-Silicon
   
   Querying Artifactory API...
   Found: OakStreamAPIfwi_ap_pre_silicon_rel_..._90_BuildPkg.7z
   
   [OK] URL: https://af01p-or.devtools.intel.com/.../BuildPkg.7z
   ```

2. **Data Extraction** (automatic)
   ```
   Downloading from Artifactory...
   [OK] Downloaded BuildPkg.7z
   
   Extracting OSXML data...
   Found Unified Patch: 51000312
   Extracted IMH OSXML from UP: IMH1-B0-1P0N-OSXML-1d
   
   Downloaded Simics release notes...
   [OK] Generated CSV
   ```

3. **Report Generation** (automatic)
   ```
   Generating HTML report...
   [OK] Generated: IFWI_Release_Status_2026.25.3.01.html
   [OK] Opened in browser
   ```

### Output

**HTML Report:**
```
DMR-AP-UCC AP1 B0 Pre-Si Orange IFWI 2026.25.3.01 has been released on WW25.5

[Complete table with BIOS, Simics, Unified Patch versions]
[PnP/PM Recipe table]

AP1 B0 uBIOS based on BIOSID 0036.D29 will be released on WW25.6
```

---

## Comparison: Old vs New

### Old Workflow (5 steps)
1. Find Artifactory build in web browser
2. Copy full URL (very long!)
3. Run PowerShell script
4. Paste URL
5. Provide platform, Simics, release info

### New Workflow (3 steps) ⭐
1. Run PowerShell script
2. Choose platform (from menu)
3. Enter version: `2026.26.4.01.0036.D.54`

**That's it!** System handles the rest.

---

## Error Handling

### Build Not Found
```
[ERROR] Directory not found (HTTP 404)

Possible reasons:
  - IFWI ID or BIOS ID is incorrect
  - Build not yet available in Artifactory
  - Path structure has changed
```

**Solution:** Double-check version numbers.

### Multiple BuildPkg Files
```
[WARN] Multiple BuildPkg.7z files found, using first one
```

**System behavior:** Automatically uses the first match.

### Network Issues
```
[ERROR] Request timeout - Artifactory may be slow or unreachable
```

**Solution:** Check network connection, try again later.

---

## When to Use Direct URL Mode

**Use Simple Mode (Recommended):**
- Standard IFWI builds from OakStreamAPIfwi
- Version format matches: `YYYY.WW.X.NN.BBBB.D.VV`
- Platform is AP1 A0, AP1 B0, or AP2 A0

**Use Direct URL Mode:**
- Non-standard build paths
- Custom builds not in Daily folder
- Special testing builds

---

## Behind the Scenes

### URL Construction Script

**File:** `construct_artifactory_url.py`

**What it does:**
1. Determines release type (pre-silicon vs post-silicon)
2. Determines folder name based on platform
3. Constructs directory path
4. Queries Artifactory Storage API to list files
5. Finds BuildPkg.7z file (handles build number automatically)
6. Returns complete URL

**API Used:**
```
GET https://af01p-or.devtools.intel.com/artifactory/api/storage/{path}
Header: X-JFrog-Art-Api: {token}
Response: JSON with list of files
```

---

## Platform-Specific Details

### AP1 A0 (Post-Silicon)

**Path Pattern:**
```
ap_post_silicon_rel/
OAKSTREAMAP.0.RPB.{IFWI_ID}.{BIOS_ID}/
OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/
```

**File Pattern:**
```
OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_{BUILD}_BuildPkg.7z
```

**Features:**
- Simplified report (BIOS + Unified Patch only)
- No Simics input needed
- No OSXML table

---

### AP1 B0 / AP2 A0 (Pre-Silicon)

**Path Pattern:**
```
ap_pre_silicon_rel/
OAKSTREAMAP.0.RPB.{IFWI_ID}.{BIOS_ID}/
OakStreamRp_DMR_FSP_Glue_Debug_Linux/
```

**File Pattern:**
```
OakStreamAPIfwi_ap_pre_silicon_rel_OakStreamRp_DMR_FSP_Glue_Debug_Linux_{BUILD}_BuildPkg.7z
```

**Features:**
- Full report (BIOS + UP + OSXML + PnP/PM + uBIOS)
- Simics input required
- Complete OSXML table

---

## Troubleshooting

### Q: "Cannot parse version string"

**Problem:**
```
[ERROR] Cannot parse version string: 2026.26.4.01
```

**Solution:** Provide BIOS ID as well:
```
✓ Correct: 2026.26.4.01.0036.D.54
✗ Wrong: 2026.26.4.01
```

---

### Q: "Directory not found"

**Problem:**
```
[ERROR] Directory not found (HTTP 404)
```

**Check:**
1. Is the IFWI ID correct? (YYYY.WW.X.NN)
2. Is the BIOS ID correct? (BBBB.D.VV)
3. Is the build available in Artifactory?

**Manual verification:**
```
https://af01p-or.devtools.intel.com/artifactory/webapp/#/artifacts/browse/tree/General/server-bios-staging-local/Daily/OakStreamAPIfwi/
```

---

### Q: "Authentication failed"

**Problem:**
```
[ERROR] Authentication failed (HTTP 403)
```

**Solution:** Get new API token from Artifactory:
1. Go to https://af01p-or.devtools.intel.com
2. User icon → Edit Profile
3. Enter current password
4. Copy API Key

---

## Summary

**New simplified workflow saves time:**
- ✅ No need to browse Artifactory web UI
- ✅ No need to copy long URLs
- ✅ Automatic build number detection
- ✅ Cleaner, faster, fewer errors

**Just provide:**
```
Platform + Version → Get Report
```

---

## Related Documentation

- [Generate-IFWI-Report-From-Artifactory.ps1](Generate-IFWI-Report-From-Artifactory.ps1) - Main script
- [construct_artifactory_url.py](construct_artifactory_url.py) - URL construction script
- [ARTIFACTORY_USAGE.md](ARTIFACTORY_USAGE.md) - Full Artifactory workflow guide
- [HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md) - API token instructions

---

**Last Updated:** 2026-06-30  
**Feature:** ✅ Simplified URL Construction  
**Status:** Ready for Production
