# CRITICAL RULES - Easy to Get Wrong!

**Last Updated:** 2026-06-30

---

## ⚠️ PURPOSE

This document lists the **MOST CRITICAL** rules that are **EASY TO GET WRONG** and would cause **INCORRECT DATA** in reports.

**READ THIS FIRST** before making any changes to extraction or display logic!

---

## 🔴 CRITICAL #1: IMH and CBB Have DIFFERENT Index Orders

**PROBLEM:** IMH and CBB OSXML values are semicolon-separated, but they use **DIFFERENT ordering** for platforms!

### IMH Ordering

```
IMH2-1p0P_26ww17hRTL-OSXML;IMH-Post-1P0AD-FV;IMH1-B0-1P0N
^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^
Index 0: AP2 A0            Index 1: AP1 A0     Index 2: AP1 B0
```

### CBB Ordering

```
CBB_C0_26ww12b_RTL;CBB-B0_MCP_25ww48a_RTL;CBB-A0_PowerOn
^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^
Index 0: AP2 A0     Index 1: AP1 B0         Index 2: AP1 A0
```

### Correct Mapping Table

| Platform | IMH Index | CBB Index | **THEY ARE DIFFERENT!** |
|----------|-----------|-----------|-------------------------|
| AP2 A0 | 0 | 0 | Same |
| **AP1 A0** | **1** | **2** | ⚠️ **DIFFERENT!** |
| **AP1 B0** | **2** | **1** | ⚠️ **DIFFERENT!** |

### ❌ WRONG Implementation

```python
# THIS IS WRONG - assumes same order for both
platform_index = {
    'AP1 A0': 1,
    'AP1 B0': 2,
    'AP2 A0': 0,
}
# Applies to both IMH and CBB
```

### ✅ CORRECT Implementation

```python
def extract_osxml_by_platform(osxml_value, platform, component):
    # Detect if IMH or CBB
    is_imh = 'IMH' in osxml_value or (component and 'IMH' in component)
    
    if is_imh:
        # IMH ordering
        platform_index = {
            'AP1 A0': 1,  # 2nd
            'AP1 B0': 2,  # 3rd
            'AP2 A0': 0,  # 1st
        }
    else:
        # CBB ordering
        platform_index = {
            'AP1 A0': 2,  # 3rd
            'AP1 B0': 1,  # 2nd
            'AP2 A0': 0,  # 1st
        }
```

**FILE:** `generate_ifwi_report.py:91-130`

---

## 🔴 CRITICAL #2: Unified Patch Order in Binary Filename

**PROBLEM:** In Simics.bin files, Unified Patch values follow version number pattern: **51xxxx = AP1 B0, 52xxxx = AP2 A0**

**KEY RULE:** Binary format is `[AP1_UP]_[AP2_UP]`, determined by version prefix (51xxxx vs 52xxxx), NOT by position!

### Binary Format

```
..._[BIOS_ID]_[AP1_UP(51xxxx)]_[AP2_UP(52xxxx)]_...
               ^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^
               1st hex           2nd hex
               Index 0           Index 1
```

### Real Example

```
OKSDCRB1_86B_2026.26.4.02_0036.D54_51000312_52000210_0.892.0_..._Simics.bin
                                    ^^^^^^^^ ^^^^^^^^
                                    AP1 B0   AP2 A0
                                    (51xxxx) (52xxxx)
                                    Index 0  Index 1
```

### Version Number Pattern (CRITICAL!)

**Rule:** Check **2nd digit** of UP version to determine platform!

| UP Version Pattern | 2nd Digit | Platform |
|-------------------|-----------|----------|
| **5_1_xxxxxx** | **1** | **AP1 B0** |
| **5_2_xxxxxx** | **2** | **AP2 A0** |
| **800009xx** | N/A | **AP1 A0** (Post-Si) |

Examples:
- `51000312` → 2nd digit is **1** → **AP1 B0** ✅
- `52000210` → 2nd digit is **2** → **AP2 A0** ✅

### Correct Extraction

| Platform | Match Method | Version Pattern | Example |
|----------|--------------|-----------------|---------|
| **AP1 A0** | 1st hex value | `800009xx` | `800009AA` |
| **AP1 B0** | **2nd digit = 1** | **`5_1_xxxxxx`** | `51000312` |
| **AP2 A0** | **2nd digit = 2** | **`5_2_xxxxxx`** | `52000210` |

**Note:** Do NOT rely on position in binary! Always check the version pattern.

### ❌ WRONG Implementation

```python
# WRONG - old logic based on position only
if platform_stepping == 'AP1 B0':
    extract_position = 2  # Wrong! Should be 1
elif platform_stepping == 'AP2 A0':
    extract_position = 1  # Wrong! Should be 2
```

### ✅ CORRECT Implementation

```python
# Match by version pattern (2nd digit)
# Do NOT rely on position!

if platform_stepping == 'AP1 B0':
    # Look for 5X1XXXXX pattern (2nd digit is 1)
    for up_value in hex_values:
        if len(up_value) >= 2 and up_value[1] == '1':
            unified_patch = up_value
            break

elif platform_stepping == 'AP2 A0':
    # Look for 5X2XXXXX pattern (2nd digit is 2)
    for up_value in hex_values:
        if len(up_value) >= 2 and up_value[1] == '2':
            unified_patch = up_value
            break
```

**FILE:** `extract_artifactory_osxml.py:195-198`

---

## 🔴 CRITICAL #3: Simics Platform Paths Are Different

**PROBLEM:** AP1 B0 and AP2 A0 use **DIFFERENT Simics Artifactory paths**!

### Correct Mapping

| Platform | Simics Path | URL |
|----------|-------------|-----|
| **AP1 B0** | `dmr-7` | `https://.../platforms/dmr-7/{VERSION}/...` |
| **AP2 A0** | `dmr-rio-7` | `https://.../platforms/dmr-rio-7/{VERSION}/...` |

### ❌ WRONG Implementation

```python
# WRONG - hardcoded path
url = f"https://.../platforms/dmr-7/{version}/..."
```

### ✅ CORRECT Implementation

```python
def download_simics_release_notes(version, token, platform_stepping):
    if platform_stepping == 'AP1 B0':
        platform_path = 'dmr-7'
    elif platform_stepping == 'AP2 A0':
        platform_path = 'dmr-rio-7'
    
    url = f"https://.../platforms/{platform_path}/{version}/..."
```

**FILE:** `extract_artifactory_osxml.py:40-49`

---

## 🔴 CRITICAL #4: SCF IPSD Version Format

**PROBLEM:** SCF IPSD must include major version prefix `4.0.0.`, NOT just the decimal value!

### Format

**Hex Value:** `0x000004eb`  
**Decimal Value:** `1259`  
**❌ WRONG Display:** `1259`  
**✅ CORRECT Display:** `4.0.0.1259`

### Implementation

```python
# Extract and convert
hex_value = "0x000004eb"
decimal_value = int(hex_value, 16)  # 1259

# ❌ WRONG
return str(decimal_value)  # Returns "1259"

# ✅ CORRECT
return f"4.0.0.{decimal_value}"  # Returns "4.0.0.1259"
```

**FILE:** `extract_artifactory_osxml.py:462`

---

## 🔴 CRITICAL #5: Simics Version Must Be Complete

**PROBLEM:** Don't hardcode or truncate Simics version - preserve the full string from user input!

### User Input Formats

```
dmr-7 2026ww24.3.00_45 Pre712
dmr-rio-7 2026ww23.6.00_03 Pre539
```

### ❌ WRONG Implementation

```python
# WRONG - hardcoded, loses "Pre712" suffix
data['simics_version'] = f"dmr-7 {simics_version}"
# Result: "dmr-7 2026ww24.3.00_45" (missing Pre712)
```

### ✅ CORRECT Implementation

```python
# Extract pure version for API call
pure_version = re.search(r'(\d{4}ww\d{2}\.\d+\.\d+_\d+)', simics_version).group(1)

# But preserve full version for display
if simics_version.startswith('dmr') or 'Pre' in simics_version:
    data['simics_version'] = simics_version  # Keep full string
else:
    # Only version number provided, add platform path
    platform_path = 'dmr-rio-7' if platform == 'AP2 A0' else 'dmr-7'
    data['simics_version'] = f"{platform_path} {simics_version}"
```

**FILE:** `extract_artifactory_osxml.py:679-689`

---

## 🔴 CRITICAL #6: SCF IPSD Only for AP1 B0 and AP2 A0

**PROBLEM:** Don't extract SCF IPSD for AP1 A0 Post-Si!

### Platform Rules

| Platform | Extract SCF IPSD? | Reason |
|----------|-------------------|--------|
| AP1 A0 | ❌ **NO** | Post-Si, no OSXML table |
| AP1 B0 | ✅ **YES** | Pre-Si, full OSXML table |
| AP2 A0 | ✅ **YES** | Pre-Si, full OSXML table |

### Implementation

```python
# MUST check platform before extraction
if final_platform in ['AP1 B0', 'AP2 A0']:
    scf_ipsd_version = extract_scf_ipsd_version(soup)
    # ...
else:
    print(f"[INFO] SCF IPSD extraction skipped for {final_platform}")
```

**FILE:** `extract_artifactory_osxml.py:657-668`

---

## 🔴 CRITICAL #7: Simics Release Notes Search Patterns

**PROBLEM:** AP1 B0 and AP2 A0 use **DIFFERENT patterns** in Simics release notes!

### Search Patterns

| Platform | IMH Pattern | CBB Pattern |
|----------|-------------|-------------|
| **AP1 B0** | `IMH regs:` | `CBB regs:` |
| **AP2 A0** | `IMH2 regs:` | `CBB regs:` |

### Implementation

```python
# MUST support both patterns
if ('IMH2 regs:' in line or 'imh2 regs:' in line.lower() or
    'IMH regs:' in line or 'imh regs:' in line.lower()):
    # Extract IMH OSXML
```

**FILE:** `extract_artifactory_osxml.py:106-114`

---

## ✅ Validation Checklist

Before committing any changes, verify:

- [ ] **IMH and CBB use different index mappings** (component parameter passed)
- [ ] **Unified Patch extraction uses correct position** (AP2 is 1st, AP1 is 2nd in binary)
- [ ] **Simics path selected by platform** (dmr-7 vs dmr-rio-7)
- [ ] **SCF IPSD has 4.0.0. prefix** (not just decimal)
- [ ] **Simics version preserved complete** (including Pre### suffix)
- [ ] **SCF IPSD only for AP1 B0 / AP2 A0** (not AP1 A0)
- [ ] **Simics search supports both IMH and IMH2** patterns

---

## 📚 Related Documentation

- [CLAUDE.md](CLAUDE.md) - Complete project rules
- [PLATFORM_RULES.md](PLATFORM_RULES.md) - Platform-specific details
- [UNIFIED_PATCH_ORDER.md](UNIFIED_PATCH_ORDER.md) - Binary format details
- [SCF_IPSD_RULES.md](SCF_IPSD_RULES.md) - SCF IPSD extraction rules
- [SIMICS_PLATFORM_PATHS.md](SIMICS_PLATFORM_PATHS.md) - Simics path mapping

---

## 🚨 When Adding New Features

**ALWAYS check:**
1. Does it involve IMH or CBB? → Remember they have different orders!
2. Does it parse binary filenames? → Remember AP2 comes before AP1!
3. Does it use Simics? → Remember platforms have different paths!
4. Does it display SCF IPSD? → Remember to add 4.0.0. prefix!
5. Does it store Simics version? → Remember to preserve complete string!

---

**IF IN DOUBT, RE-READ THIS DOCUMENT!**

---

**End of Critical Rules Document**
