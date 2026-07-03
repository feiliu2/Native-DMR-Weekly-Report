# DMR IFWI Platform-Specific Rules

**Last Updated:** 2026-06-30

---

## Overview: Three IFWI Types

| Platform | Silicon Type | Binary Suffix | Report Type | uBIOS |
|----------|--------------|---------------|-------------|-------|
| **AP1 A0** | Post-Si | `VIS.bin` | Simplified | ❌ No |
| **AP1 B0** | Pre-Si | `Simics.bin` | Full | ✅ Yes |
| **AP2 A0** | Pre-Si | `Simics.bin` | Full | ✅ Yes |

---

## Platform 1: AP1 A0 Post-Si

### Report Components

**✅ Shows:**
- Release Statement
- BIOS Binary
- AP Unified Patch

**❌ Hides:**
- OSXML table
- PnP/PM Recipe table
- uBIOS statement

### Binary File Format

**Suffix:** `NonIPClean_Trace_DebugSigned_VIS.bin`

**Example:**
```
OKSDCRB1_86B_2026.26.4.01_0036.D54_800009AA_0.892.0_1P0_NonIPClean_Trace_DebugSigned_VIS.bin
                          ^^^^^^^^^ ^^^^^^^^^
                          BIOS ID   Unified Patch (1st hex)
```

### Report Example

```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

Release version information as below:
┌──────────────────┬───────────┐
│ BIOS Binary      │ 0036.D54  │
│ AP Unified Patch │ 800009AA  │
└──────────────────┴───────────┘
```

---

## Platform 2: AP1 B0 Pre-Si

### Report Components

**✅ Shows:**
- Release Statement
- BIOS Binary
- AP Unified Patch
- OSXML table (IMH, CBB, SCF with Simics columns)
- PnP/PM Recipe table
- **uBIOS statement** (Orange week + 1 day)

**❌ Hides:**
- Nothing (full report)

### Binary File Format

**Suffix:** `NonIPClean_Trace_DebugSigned_Simics.bin`

**Example:**
```
OKSDCRB1_86B_2026.26.6.01_0036.D54_52000210_51000312_0.892.0_NonIPClean_Trace_DebugSigned_Simics.bin
                          ^^^^^^^^^ ^^^^^^^^^ ^^^^^^^^^
                          BIOS ID   AP2 A0 UP AP1 B0 UP
                                    (1st hex) (2nd hex)
```

**Extract:** 2nd 8-digit hex after BIOS ID → `51000312`

### Report Example

```
DMR-AP-UCC AP1 B0 Pre-Si Orange IFWI 2026.26.6.01 has been released on WW26.5

Release version information as below:
┌──────────────┬──────────┬────────────┬────────────┬──────────┐
│              │ Version  │ IMH OSXML  │ CBB OSXML  │ SCF IPSD │
├──────────────┼──────────┼────────────┼────────────┼──────────┤
│ BIOS Binary  │ 0036.D54 │ ...        │ ...        │ ...      │
│ Simics       │ dmr-7... │ ...        │ ...        │ ...      │
│ Unified Patch│ 51000312 │ ...        │ ...        │ ...      │
└──────────────┴──────────┴────────────┴────────────┴──────────┘

PNP and PM recipe config in BIOS as below:
┌─────────┬──────────┬────────────┬──────────────┐
│         │ BIOS MC  │ BIOS IIO   │ BIOS Uncore  │
├─────────┼──────────┼────────────┼──────────────┤
│ PNP     │ 26ww06   │ 26ww06     │ 26ww06       │
│ PM      │ 26ww06   │ 26ww06     │ 26ww06       │
└─────────┴──────────┴────────────┴──────────────┘

AP1 B0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6
```

---

## Platform 3: AP2 A0 Pre-Si

### Report Components

**✅ Shows:**
- Release Statement
- BIOS Binary
- AP Unified Patch
- OSXML table (IMH, CBB, SCF with Simics columns)
- PnP/PM Recipe table
- **uBIOS statement** (Orange week + 1 day)

**❌ Hides:**
- Nothing (full report)

### Binary File Format

**Suffix:** `NonIPClean_Trace_DebugSigned_Simics.bin` (same as AP1 B0)

**Example:**
```
OKSDCRB1_86B_2026.25.3.01_0036.D29_5200020F_51000312_0.883.0_NonIPClean_Trace_DebugSigned_Simics.bin
                          ^^^^^^^^^ ^^^^^^^^^ ^^^^^^^^^
                          BIOS ID   AP2 A0 UP AP1 B0 UP
                                    (1st hex  (2nd hex)
                                    extract)
```

**Extract:** 1st 8-digit hex after BIOS ID → `5200020F`

### Report Example

```
DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.26.6.01 has been released on WW26.5

Release version information as below:
┌──────────────┬──────────┬────────────┬────────────┬──────────┐
│              │ Version  │ IMH OSXML  │ CBB OSXML  │ SCF IPSD │
├──────────────┼──────────┼────────────┼────────────┼──────────┤
│ BIOS Binary  │ 0036.D54 │ ...        │ ...        │ ...      │
│ Simics       │ dmr-7... │ ...        │ ...        │ ...      │
│ Unified Patch│ 52000210 │ ...        │ ...        │ ...      │
└──────────────┴──────────┴────────────┴────────────┴──────────┘

PNP and PM recipe config in BIOS as below:
┌─────────┬──────────┬────────────┬──────────────┐
│         │ BIOS MC  │ BIOS IIO   │ BIOS Uncore  │
├─────────┼──────────┼────────────┼──────────────┤
│ PNP     │ 26ww06   │ 26ww06     │ 26ww06       │
│ PM      │ 26ww06   │ 26ww06     │ 26ww06       │
└─────────┴──────────┴────────────┴──────────────┘

AP2 A0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6
```

---

## Unified Patch Extraction Logic

### Python Implementation

```python
def extract_unified_patch_from_binary(archive_path, platform_stepping):
    """
    Binary format for Simics.bin: ..._[BIOS_ID]_[AP2_UP]_[AP1_UP]_...
    
    AP1 A0: Look for VIS.bin, extract 1st hex
    AP1 B0: Look for Simics.bin, extract 2nd hex (index 1)
    AP2 A0: Look for Simics.bin, extract 1st hex (index 0)
    """
    
    # Determine binary suffix and extraction position
    if platform_stepping == 'AP1 A0':
        target_suffix = 'NonIPClean_Trace_DebugSigned_VIS.bin'
        extract_position = 1
    elif platform_stepping == 'AP1 B0':
        target_suffix = 'NonIPClean_Trace_DebugSigned_Simics.bin'
        extract_position = 2  # 2nd hex (AP1 B0 is after AP2 A0)
    elif platform_stepping == 'AP2 A0':
        target_suffix = 'NonIPClean_Trace_DebugSigned_Simics.bin'
        extract_position = 1  # 1st hex (AP2 A0 comes first)
    
    # Find binary file
    for filename in archive_files:
        if filename.endswith(target_suffix):
            # Extract all 8-digit hex values after BIOS ID
            match = re.search(r'_00\d{2}\.D\d+_((?:[A-F0-9]{8}_?)+)', filename)
            hex_values = re.findall(r'([A-F0-9]{8})', match.group(1))
            
            # Return hex at specified position
            return hex_values[extract_position - 1].upper()
```

### Test Cases

**Binary 1 (AP1 A0):**
```
Input: OKSDCRB1_86B_2026.26.4.01_0036.D54_800009AA_0.892.0_1P0_NonIPClean_Trace_DebugSigned_VIS.bin
Platform: AP1 A0
Expected: 800009AA (1st hex)
```

**Binary 2 (AP1 B0):**
```
Input: OKSDCRB1_86B_2026.25.3.01_0036.D29_5200020F_51000312_0.883.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                           ^^^^^^^^^ ^^^^^^^^^
                                           AP2 A0    AP1 B0
Platform: AP1 B0
Expected: 51000312 (2nd hex, index 1)
```

**Binary 3 (AP2 A0):**
```
Input: OKSDCRB1_86B_2026.25.3.01_0036.D29_5200020F_51000312_0.883.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                           ^^^^^^^^^ ^^^^^^^^^
                                           AP2 A0    AP1 B0
Platform: AP2 A0
Expected: 5200020F (1st hex, index 0)
```

---

## uBIOS Statement Rules

### When to Generate uBIOS Statement

- ✅ **AP1 B0 Pre-Si** - Always
- ✅ **AP2 A0 Pre-Si** - Always
- ❌ **AP1 A0 Post-Si** - Never

### uBIOS Week Calculation

**Formula:** Orange release week + 1 day

**Examples:**
- Orange: `WW26.5` → uBIOS: `WW26.6`
- Orange: `WW26.7` → uBIOS: `WW27.1` (crosses week boundary)

### uBIOS Statement Format

**Template:**
```
{Platform} {Stepping} uBIOS based on BIOSID {BIOS_ID} is trend to be released on WW{Week}.{Day}
```

**Examples:**
```
AP1 B0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6
AP2 A0 uBIOS based on BIOSID 0036.D54 is trend to be released on WW26.6
```

---

## Decision Tree

```
User selects platform
    │
    ├─ AP1 A0
    │   ├─ Binary: VIS.bin
    │   ├─ UP: 1st hex (e.g., 800009AA)
    │   ├─ Report: Simplified (BIOS + UP only)
    │   └─ uBIOS: No
    │
    ├─ AP1 B0
    │   ├─ Binary: Simics.bin
    │   ├─ UP: 1st hex (e.g., 51000312)
    │   ├─ Report: Full (BIOS + UP + OSXML + PnP/PM)
    │   └─ uBIOS: Yes (Orange week + 1 day)
    │
    └─ AP2 A0
        ├─ Binary: Simics.bin
        ├─ UP: 2nd hex (e.g., 52000210)
        ├─ Report: Full (BIOS + UP + OSXML + PnP/PM)
        └─ uBIOS: Yes (Orange week + 1 day)
```

---

## OSXML Multi-Value Extraction

### Problem

IMH and CBB OSXML values may contain **multiple platform-specific values** separated by semicolons:

```
IMH2-1p0P_26ww17hRTL-OSXML;IMH-Post-1P0AD-FV;IMH1-B0-1P0N
```

### Solution

Extract only the value corresponding to the current platform:

| Platform | Index | Extract |
|----------|-------|---------|
| AP2 A0 | 0 | `IMH2-1p0P_26ww17hRTL-OSXML` (1st) |
| AP1 A0 | 1 | `IMH-Post-1P0AD-FV` (2nd) |
| AP1 B0 | 2 | `IMH1-B0-1P0N` (3rd) |

### Applies To

- ✅ IMH_OSXML (BIOS and Simics columns)
- ✅ CBB_OSXML (BIOS and Simics columns)
- ❌ SCF_IPSD (single value, no extraction needed)

### Example

**Before (raw CSV):**
```
IMH OSXML: IMH2-1p0P_26ww17hRTL-OSXML;IMH-Post-1P0AD-FV;IMH1-B0-1P0N
```

**After (AP2 A0 report):**
```
IMH OSXML: IMH2-1p0P_26ww17hRTL-OSXML
```

**After (AP1 B0 report):**
```
IMH OSXML: IMH1-B0-1P0N
```

---

## Summary Table

| Aspect | AP1 A0 Post-Si | AP1 B0 Pre-Si | AP2 A0 Pre-Si |
|--------|----------------|---------------|---------------|
| **Binary Suffix** | `VIS.bin` | `Simics.bin` | `Simics.bin` |
| **UP Position** | 1st hex | 1st hex | 2nd hex |
| **BIOS Binary** | ✅ Show | ✅ Show | ✅ Show |
| **Unified Patch** | ✅ Show | ✅ Show | ✅ Show |
| **OSXML Table** | ❌ Hide | ✅ Show | ✅ Show |
| **PnP/PM Table** | ❌ Hide | ✅ Show | ✅ Show |
| **uBIOS Statement** | ❌ No | ✅ Yes (+1 day) | ✅ Yes (+1 day) |
| **Platform Label** | DMR-AP-UCC | DMR-AP-UCC | DMR-AP-MCC |
| **Silicon Type** | Post-Si | Pre-Si | Pre-Si |

---

**End of Platform Rules**
