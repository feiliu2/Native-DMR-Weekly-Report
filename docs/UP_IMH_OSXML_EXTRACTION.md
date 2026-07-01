# Unified Patch IMH OSXML Extraction

**Feature:** Extract IMH OSXML version from Unified Patch release notes and populate the Unified Patch column in OSXML table.

**Applies to:** AP1 B0 and AP2 A0 Pre-Silicon releases only

---

## Overview

When generating reports for AP1 B0 or AP2 A0 from Artifactory, the system now:

1. Extracts Unified Patch version from binary filename
2. Downloads the Unified Patch package from Artifactory
3. Extracts `_release_notes.csv` from the package
4. Parses IMH OSXML version from CSV
5. Populates the Unified Patch column in OSXML table

This provides complete version tracking across all three data sources: BIOS, Simics, and Unified Patch.

---

## Architecture

### Components

```
Generate-IFWI-Report-From-Artifactory.ps1
    |
    v
extract_artifactory_osxml.py
    |
    +-> [Step 4] Extract Unified Patch from binary filename
    |
    +-> [Step 4.6] Extract IMH OSXML from UP package
             |
             v
        extract_up_imh_osxml.py
             |
             +-> download_unified_patch_package()
             |
             +-> extract_release_notes_csv()
             |
             +-> parse_imh_osxml_from_csv()
```

### Standalone Module

`extract_up_imh_osxml.py` - Self-contained module that can be:
- Imported: `from extract_up_imh_osxml import extract_imh_osxml_from_up`
- Run standalone: `python extract_up_imh_osxml.py <up_version> <platform> <token>`

---

## Platform-Specific Details

### AP1 B0

**Artifactory URL Pattern:**
```
https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/IMH1_B0_DMRAP_Unified_Patch/{UP_VERSION}/UP_DMR_AP1_B0_{UP_VERSION}_TPRODSIGNED.7z
```

**CSV Filename:**
```
UP_DMR_AP1_B0_51000312_TPRODSIGNED_release_notes.csv
```

**Search Keyword:**
```
imh_osxml
```

**CSV Line Pattern:**
```csv
OSXML,LTM,iMH: dmr_imh_osxml-IMH1-B0-1P0N-OSXML-1d,26ww22a
                              ^^^^^^^^^^^^^^^^^^^^^^^
                              This is what we extract
```

**Extraction Regex:**
```python
match = re.search(r'dmr_imh_osxml-([^,\s]+)', line, re.IGNORECASE)
# Returns: IMH1-B0-1P0N-OSXML-1d
```

**Example:**
- Unified Patch: `51000312`
- IMH OSXML: `IMH1-B0-1P0N-OSXML-1d`

---

### AP2 A0

**Artifactory URL Pattern:**
```
https://af01p-sc.devtools.intel.com/artifactory/DEG-IFWI-LOCAL/SiEn-OakStream-DiamondRapids-AP/Ingredients/IMH2_B0_DMRAP_Unified_Patch/{UP_VERSION}/UP_DMR_AP2_B0_{UP_VERSION}_TPRODSIGNED.7z
```

**CSV Filename:**
```
UP_DMR_AP2_B0_5200020F_TPRODSIGNED_release_notes.csv
```

**Search Keyword:**
```
dmrhub2
```

**CSV Line Pattern:**
```csv
OSXML,Primecode,dmrhub2-a0-26ww03g-IMH2-1p0D_26ww03g_RTL-OSXML-1d,null
OSXML,LTM,iMH: dmrhub2-a0-26ww06h-IMH2-1p0G_26ww06h_RTL-OSXML-1d,26ww16a
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    This is what we extract
```

**Extraction Regex:**
```python
match = re.search(r'dmrhub2-[^-]+-[^-]+-([^,\s]+)', line, re.IGNORECASE)
# Returns: IMH2-1p0D_26ww03g_RTL-OSXML-1d (first match)
```

**Example:**
- Unified Patch: `5200020F`
- IMH OSXML: `IMH2-1p0D_26ww03g_RTL-OSXML-1d`

---

## Data Flow

### Input
```
Unified Patch Version: 51000312
Platform: AP1 B0
API Token: ***************
```

### Processing

**Step 1: Build URL**
```
https://af01p-sc.devtools.intel.com/artifactory/.../IMH1_B0_DMRAP_Unified_Patch/51000312/UP_DMR_AP1_B0_51000312_TPRODSIGNED.7z
```

**Step 2: Download .7z (5.3 MB)**
```
[OK] Downloaded: UP_DMR_AP1_B0_51000312_TPRODSIGNED.7z (5314482 bytes)
```

**Step 3: Extract CSV**
```
[OK] Extracted: UP_DMR_AP1_B0_51000312_TPRODSIGNED_release_notes.csv
```

**Step 4: Parse CSV**
```
Search keyword: imh_osxml
Found line: OSXML,LTM,iMH: dmr_imh_osxml-IMH1-B0-1P0N-OSXML-1d,26ww22a...
[OK] Found IMH OSXML: IMH1-B0-1P0N-OSXML-1d
```

**Step 5: Cleanup**
```
Cleaned up: *.7z
Cleaned up: *_release_notes.csv
```

### Output
```
IMH_OSXML (Unified Patch): IMH1-B0-1P0N-OSXML-1d
```

---

## Report Display

### Before (Missing UP IMH OSXML)

```
Release version information
---------------------------
Component       | BIOS OSXML           | Simics OSXML           | Unified Patch OSXML
----------------|----------------------|------------------------|--------------------
IMH OSXML       | IMH1-B0-1P0N        | dmr-imh-1p0n-26ww26a  | N/A ❌
CBB OSXML       | CBB-B0_MCP_25ww48a  | dmr-cbb-b0-26ww20a    | N/A
SCF IPSD        | 4.0.0.1259          |                        | 4.0.0.1259
```

### After (Complete UP IMH OSXML)

```
Release version information
---------------------------
Component       | BIOS OSXML           | Simics OSXML           | Unified Patch OSXML
----------------|----------------------|------------------------|--------------------
IMH OSXML       | IMH1-B0-1P0N        | dmr-imh-1p0n-26ww26a  | IMH1-B0-1P0N-OSXML-1d ✅
CBB OSXML       | CBB-B0_MCP_25ww48a  | dmr-cbb-b0-26ww20a    | N/A
SCF IPSD        | 4.0.0.1259          |                        | 4.0.0.1259
```

**Key Benefit:** Now showing complete version tracking for IMH OSXML across all three sources!

---

## Error Handling

### Package Not Found (HTTP 404)
```
[ERROR] Unified Patch package not found (HTTP 404)
URL: https://af01p-sc.devtools.intel.com/.../51000312/...
```

**Cause:** Wrong UP version or URL path changed

**Action:** Verify UP version and Artifactory path structure

---

### Authentication Failed (HTTP 403)
```
[ERROR] Authentication failed (HTTP 403). Check API Token.
```

**Cause:** Invalid or expired API token

**Action:** Generate new token from [Artifactory Profile Settings](https://af01p-sc.devtools.intel.com/ui/admin/artifactory/user-profile)

---

### CSV Not Found in Archive
```
[ERROR] _release_notes.csv not found in archive
```

**Cause:** Package structure changed or corrupted download

**Action:** Verify package integrity, try re-downloading

---

### IMH OSXML Not Found in CSV
```
[WARN] IMH OSXML not found in release notes
```

**Cause:** Keyword not found or CSV format changed

**Action:** Check CSV content manually, verify search keyword is correct

---

## Testing

### Test AP1 B0 Extraction
```bash
python extract_up_imh_osxml.py 51000312 "AP1 B0" <your_api_token>

# Expected output:
SUCCESS: IMH OSXML = IMH1-B0-1P0N-OSXML-1d
```

### Test AP2 A0 Extraction
```bash
python extract_up_imh_osxml.py 5200020F "AP2 A0" <your_api_token>

# Expected output:
SUCCESS: IMH OSXML = IMH2-1p0D_26ww03g_RTL-OSXML-1d
```

---

## API Token Requirements

**Required Permissions:**
- Read access to `DEG-IFWI-LOCAL` repository
- Path: `/SiEn-OakStream-DiamondRapids-AP/Ingredients/`

**How to Get Token:**
1. Go to [https://af01p-sc.devtools.intel.com](https://af01p-sc.devtools.intel.com)
2. Click user icon → "Edit Profile"
3. Enter current password
4. Copy API Key (under "Authentication Settings")

---

## Performance

**Typical Download Sizes:**
- AP1 B0 UP Package: ~5.3 MB
- AP2 A0 UP Package: ~5.5 MB

**Timing:**
- Download: 5-10 seconds (depends on network)
- Extract CSV: <1 second
- Parse: <1 second
- **Total: ~6-12 seconds per platform**

**Network Usage:**
- Only downloads if needed (AP1 B0 / AP2 A0)
- Cleans up archives after extraction
- Minimal disk footprint

---

## Integration Points

### In extract_artifactory_osxml.py

**Step 4.6 (Line ~670):**
```python
# Step 4.6: Extract IMH OSXML from Unified Patch (only for AP1 B0 / AP2 A0)
if final_platform in ['AP1 B0', 'AP2 A0'] and unified_patch_from_binary:
    print(f"\n[INFO] Extracting IMH OSXML from Unified Patch...")
    try:
        from extract_up_imh_osxml import extract_imh_osxml_from_up

        up_imh_osxml = extract_imh_osxml_from_up(
            unified_patch_from_binary, 
            final_platform, 
            api_token, 
            output_path
        )

        if up_imh_osxml:
            print(f"[OK] Extracted IMH OSXML from UP: {up_imh_osxml}")
            if 'IMH_OSXML' not in data['osxml_data']:
                data['osxml_data']['IMH_OSXML'] = {'bios': None, 'simics': None, 'up': None}
            data['osxml_data']['IMH_OSXML']['up'] = up_imh_osxml
        else:
            print(f"[WARN] Failed to extract IMH OSXML from Unified Patch")

    except Exception as e:
        print(f"[ERROR] Failed to extract IMH OSXML from UP: {e}")
```

**CSV Output:**
```csv
Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
IMH_OSXML,IMH1-B0-1P0N,dmr-imh-1p0n-26ww26a,IMH1-B0-1P0N-OSXML-1d
```

---

## Limitations

1. **Platform Support:** Only AP1 B0 and AP2 A0 (Pre-Si with Simics)
2. **Dependency:** Requires valid Artifactory API token with read permissions
3. **Network:** Requires internet connection to download UP packages
4. **Artifactory Dependency:** If Artifactory path structure changes, URLs must be updated

---

## Future Enhancements

Potential improvements:
- Cache downloaded UP packages to avoid re-downloading
- Parallel download if processing multiple oranges
- Support for other platforms (AP2 B0 if needed)
- Fallback to alternative extraction methods if primary fails

---

## Related Documentation

- [CLAUDE.md Rule 0.7](CLAUDE.md#rule-07-unified-patch-imh-osxml-extraction-new) - Project rules
- [CRITICAL_RULES.md](CRITICAL_RULES.md) - Critical extraction rules
- [HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md) - API token setup guide

---

**Last Updated:** 2026-06-30  
**Feature Status:** ✅ Implemented and Tested  
**Version:** 1.0
