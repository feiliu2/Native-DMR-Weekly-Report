# DMR IFWI Report Generator - Rules Summary

## 📜 Updated Rules (2026-06-30)

This document summarizes the latest project rules and constraints.

---

## 🆕 New Rule: Artifactory Workflow User Input Requirements

### Rule 0 (Artifactory Workflow)

**User MUST explicitly provide three pieces of information:**

#### 1. Download Link
- Full Artifactory build package URL
- Format: `https://af01p-or.devtools.intel.com/artifactory/.../BuildPkg.7z`
- Example:
  ```
  https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z
  ```

#### 2. Platform/Stepping
- User selects from menu (1-4):
  - `AP1 A0`
  - `AP1 B0`
  - `AP2 A0`
  - `AP2 B0`
- **Why required:** Build packages don't reliably indicate AP1 vs AP2
- **Implementation:** Passed to `extract_artifactory_osxml.py` and stored in CSV

#### 3. Release Info
- Must include tense and work week
- Accepted formats:
  - `will be released on WW26.5` (future release)
  - `released on WW26.5` (past release, converts to "has been released")
  - `has been released on WW26.5` (past release, explicit)
- **Why required:** Release week not stored in build package metadata
- **Implementation:** Parsed by PowerShell script, passed to report generator

### Why Manual Input?

❌ **Auto-detection is unreliable:**
- Platform (AP1/AP2) cannot be determined from file structure alone
- Stepping (A0/B0) may be ambiguous in Post-Si builds
- Release week is planning data, not build data

✅ **User knows best:**
- User has direct knowledge of platform target
- User knows the planned release schedule
- Eliminates guessing and errors

---

## 🆕 Rule 0.5: AP1 A0 Post-Si Simplified Report

### When AP1 A0 Post-Si is Detected

**Criteria:**
- User input: Platform/Stepping = `AP1 A0`
- No Simics data for IMH/CBB (indicates Post-Silicon, not Pre-Silicon simulation)

### Simplified Report Output

**✅ Shows:**
```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

Release version information as below:
┌─────────────────────┬───────────┐
│ BIOS Binary         │ 0036.D54  │
│ AP Unified Patch    │ 800009AA  │
└─────────────────────┴───────────┘
```

**❌ Hides:**
- OSXML table (IMH OSXML, CBB OSXML, SCF IPSD)
- PnP/PM Recipe table (IIO, MC, UNCORE)

### Unified Patch Extraction

**From binary filename in build package:**

```
OKSDCRB1_86B_2026.26.4.01_0036.D54_800009AA_0.892.0_1P0_NonIPClean_Trace_DebugSigned_VIS.bin
                                    ^^^^^^^^
                                    Extract this 8-digit hex
```

**Requirements:**
- Binary must end with: `NonIPClean_Trace_DebugSigned_VIS.bin`
- Extract 8-digit hex after BIOS ID pattern

**Why?**
- AP1 A0 Post-Si uses real hardware (no simulation/Simics)
- OSXML and PnP/PM data not applicable for Post-Si testing
- Only Unified Patch version is relevant

---

## 🎯 Output Format

### Release Statement with Post-Si/Pre-Si Label

**Format:**
```
DMR-AP-{UCC|MCC} {Platform} {Stepping} {Silicon-Type} Orange IFWI {Orange-ID} {Tense} on WW{Week}.{Day}
```

**Example Output:**
```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5
```

**Silicon Type Detection:**
- **Post-Si**: No Simics data for IMH/CBB (OSXML_Simics = N/A)
- **Pre-Si**: Has Simics data for IMH/CBB

**Platform Mapping:**
- AP1 → DMR-AP-UCC (Universal Compute Complex)
- AP2 → DMR-AP-MCC (Memory Compute Complex)

---

## 📊 Workflow Comparison

| Aspect | FIV Portal | Artifactory |
|--------|-----------|-------------|
| **Data Source** | Orange Report web page | Build package .7z |
| **Platform Input** | Auto-detected from page | **User selects from menu** |
| **Release Week** | User provides | **User provides** |
| **Orange ID** | Auto-detected from URL | Auto-detected from URL |
| **BIOS ID** | Auto-detected from page | Auto-detected from URL |
| **Simics Data** | Usually available (Pre-Si) | Usually N/A (Post-Si) |
| **Speed** | Slower (Selenium) | Faster (HTTP download) |

---

## 🔄 Updated Files

### Scripts
1. **extract_artifactory_osxml.py**
   - Added `platform_stepping` parameter (optional, overrides auto-detection)
   - Extract Orange ID from URL (more reliable than page text)
   - Extract BIOS ID from URL pattern

2. **Generate-IFWI-Report-From-Artifactory.ps1**
   - 4-step interactive input:
     1. Download Link
     2. Platform/Stepping (menu selection)
     3. Release Info (with format validation)
     4. API Token
   - Validates all inputs before proceeding
   - Passes platform to Python extractor

3. **generate_ifwi_report.py**
   - Added silicon type detection (Post-Si vs Pre-Si)
   - Based on IMH/CBB Simics data presence
   - SCF IPSD Simics data ignored for silicon type

### Documentation
1. **CLAUDE.md** - Added Rule 0 (Artifactory User Input)
2. **QUICK_START_ARTIFACTORY.md** - Updated with 4-step workflow
3. **SETUP_ARTIFACTORY.md** - Added input requirements section
4. **ARTIFACTORY_USAGE.md** - Updated prompts documentation
5. **README.md** - Added input requirements summary
6. **RULES_SUMMARY.md** - This document (new)

---

## ✅ Validation Checklist

Before generating a report, ensure:

- [ ] Download Link is valid Artifactory URL (.7z file)
- [ ] Platform/Stepping matches build target (AP1 A0, AP1 B0, AP2 A0, or AP2 B0)
- [ ] Release Info includes:
  - [ ] Tense: "will be released" or "released" (converts to "has been released")
  - [ ] Week: Format WWxx.x (e.g., WW26.5)
- [ ] API Token is valid and not expired
- [ ] Output includes:
  - [ ] Platform label (DMR-AP-UCC or DMR-AP-MCC)
  - [ ] Silicon type (Post-Si or Pre-Si)
  - [ ] Correct tense in release statement

---

## 📝 Example Usage

### Command Line

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

### Interactive Session

```
=== DMR IFWI Report Generator (Artifactory Source) ===

Step 1: Enter Artifactory build package URL
Download Link: https://af01p-or.devtools.intel.com/.../BuildPkg.7z

Step 2: Select Platform and Stepping
Options:
  1. AP1 A0
  2. AP1 B0
  3. AP2 A0
  4. AP2 B0
Enter number (1-4): 1
Platform/Stepping: AP1 A0

Step 3: Enter release information
Release info: released on WW26.5
Release: has been released on WW26.5

Step 4: Enter Artifactory API Token
API Token: ****************

=== Processing ===

Downloading and extracting OSXML data...
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

### Generated Report Output

```html
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

Release version information as below:
[OSXML table with BIOS Binary, Unified Patch data]

PNP and PM recipe config in BIOS as below:
[PnP/PM table with IIO, MC, UNCORE versions]
```

---

## 🔗 Related Documents

- **[CLAUDE.md](CLAUDE.md)** - Complete project rules (Rule 0-6)
- **[QUICK_START_ARTIFACTORY.md](QUICK_START_ARTIFACTORY.md)** - Quick start guide
- **[SETUP_ARTIFACTORY.md](SETUP_ARTIFACTORY.md)** - Setup and installation
- **[ARTIFACTORY_USAGE.md](ARTIFACTORY_USAGE.md)** - Detailed usage guide
- **[INSTALL_TROUBLESHOOTING.md](INSTALL_TROUBLESHOOTING.md)** - Troubleshooting

---

**Last Updated:** 2026-06-30  
**Version:** 2.0 (Added Artifactory workflow with user input requirements)
