# SCF IPSD Extraction Rules

**Last Updated:** 2026-06-30

---

## Overview

SCF IPSD version is extracted from `OSXML_Version.html` by converting the hexadecimal value of `IpScfMgr` or `IpScfMgrGen5` to decimal.

---

## Platform-Specific Rules

### ✅ Extraction Enabled

| Platform | SCF IPSD Extraction | Reason |
|----------|---------------------|--------|
| **AP1 B0** | ✅ Yes | Pre-Si platform with OSXML data |
| **AP2 A0** | ✅ Yes | Pre-Si platform with OSXML data |

### ❌ Extraction Disabled

| Platform | SCF IPSD Extraction | Reason |
|----------|---------------------|--------|
| **AP1 A0** | ❌ No | Post-Si platform - simplified report (no OSXML table) |
| **AP2 B0** | ❌ No | Not currently used |

---

## Column-Specific Rules

### BIOS Column

**Extraction:** From `OSXML_Version.html`

**Method:**
1. Find `IpScfMgrGen5` or `IpScfMgr` in HTML table
2. Extract hexadecimal value from next cell (e.g., `0x0000000c`)
3. Convert to decimal (e.g., `12`)
4. **Add major version prefix:** `4.0.0.` + decimal value

**Applies to:** AP1 B0, AP2 A0

**Example:**
```
HTML: IpScfMgrGen5 → 0x0000000c
Decimal: 12
BIOS Column: 4.0.0.12
```

---

### Simics Column

**Value:** Always empty (`N/A`)

**Reason:** SCF IPSD for Simics is **NOT** extracted from Simics release notes. Unlike IMH and CBB OSXML, SCF IPSD Simics value is not available in the `daily_release_notification.md` file.

**Applies to:** All platforms

**Example:**
```
Simics Column: (empty/N/A)
```

---

### Unified Patch Column

**Value:** Same as BIOS column (decimal value)

**Applies to:** AP1 B0, AP2 A0

**Example:**
```
Unified Patch Column: 12
```

---

## HTML Table Structure

### Example Source (OSXML_Version.html)

```html
<tr>
    <td>IpScfMgr</td>
    <td>0x000004eb</td>
    <td>ARCH_OSXML_scfcache_gen4_24ww33...</td>
</tr>
<tr>
    <td>IpScfMgrGen5</td>
    <td>0x0000000c</td>
    <td>ARCH_OSXML_scfcache_gen4_24ww33...</td>
</tr>
```

### Extraction Logic

**Priority:** `IpScfMgrGen5` first, then `IpScfMgr` as fallback

```python
def extract_scf_ipsd_version(soup):
    """Extract SCF IPSD version from hex value and format with major version."""
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
            
            for i, cell_text in enumerate(cells):
                # Look for IpScfMgrGen5 or IpScfMgr
                if cell_text in ['IpScfMgrGen5', 'IpScfMgr']:
                    if i + 1 < len(cells):
                        hex_value = cells[i + 1].strip()
                        
                        if hex_value.startswith('0x'):
                            decimal_value = int(hex_value, 16)
                            # Add major version prefix: 4.0.0.
                            version_string = f"4.0.0.{decimal_value}"
                            return version_string
    
    return None
```

---

## Report Display

### AP1 B0 / AP2 A0 (Full Report)

**OSXML Table:**

| Component | Version | IMH OSXML | CBB OSXML | SCF IPSD |
|-----------|---------|-----------|-----------|----------|
| BIOS Binary | 0036.D29 | IMH2-1p0P... | CBB_C0... | **4.0.0.12** |
| Simics | dmr-7... | dmr-imh2... | dmr-cbb... | **(empty)** |
| Unified Patch | 51000312 | N/A | N/A | **4.0.0.12** |

**Key Points:**
- ✅ BIOS row: Shows version format `4.0.0.[decimal]` (e.g., `4.0.0.12`)
- ❌ Simics row: Empty (no SCF IPSD in Simics release notes)
- ✅ Unified Patch row: Shows same version as BIOS

---

### AP1 A0 (Simplified Report)

**No OSXML table displayed** - SCF IPSD extraction skipped entirely.

---

## CSV Format

### AP2 A0 Example

```csv
Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
IMH_OSXML,IMH2-1p0P_26ww17hRTL-OSXML,dmr-imh2-1p0f-26ww05,N/A
CBB_OSXML,CBB_C0_26ww12b_RTL,dmr-cbb-c0-1p0-26ww12b,N/A
SCF_IPSD,4.0.0.12,N/A,4.0.0.12
         ^^^^^^^^  ^^^  ^^^^^^^^
         |         |    └── Unified Patch: version format
         |         └──────── Simics: empty (N/A)
         └────────────────── BIOS: version format 4.0.0.[decimal]
```

---

## Implementation Details

### Conditional Extraction

```python
# In parse_osxml_html()
if platform_stepping in ['AP1 B0', 'AP2 A0']:
    scf_ipsd_version = extract_scf_ipsd_version(soup)
    if scf_ipsd_version:
        osxml_data['SCF_IPSD']['bios'] = scf_ipsd_version
        osxml_data['SCF_IPSD']['simics'] = None  # Always empty
        osxml_data['SCF_IPSD']['up'] = scf_ipsd_version  # Same as BIOS
else:
    print(f"[INFO] SCF IPSD extraction skipped for {platform_stepping}")
```

### Why Simics Column is Empty

Unlike IMH and CBB OSXML which have entries in Simics release notes:
```markdown
- IMH2 regs: **dmr-imh2-1p0f-26ww05**
- CBB regs: **dmr-cbb-c0-1p0-26ww12b**
```

**SCF IPSD has no equivalent entry** in `daily_release_notification.md`, so Simics column remains empty.

---

## Test Cases

### Test 1: AP2 A0 (Extraction Enabled)

**Input:**
- Platform: AP2 A0
- HTML: `IpScfMgrGen5` → `0x0000000c`

**Expected Output:**
- BIOS Column: `4.0.0.12`
- Simics Column: `N/A`
- Unified Patch Column: `4.0.0.12`

---

### Test 2: AP1 B0 (Extraction Enabled)

**Input:**
- Platform: AP1 B0
- HTML: `IpScfMgr` → `0x000004eb`

**Expected Output:**
- BIOS Column: `4.0.0.1259`
- Simics Column: `N/A`
- Unified Patch Column: `4.0.0.1259`

---

### Test 3: AP1 A0 (Extraction Disabled)

**Input:**
- Platform: AP1 A0
- HTML: Any value

**Expected Output:**
- SCF IPSD extraction skipped
- No OSXML table in report (simplified report mode)

---

## Conversion Examples

| Hex Value | Decimal Value | Final Version String |
|-----------|---------------|----------------------|
| `0x0000000c` | `12` | `4.0.0.12` |
| `0x000004eb` | `1259` | `4.0.0.1259` |
| `0x00000010` | `16` | `4.0.0.16` |
| `0x000000ff` | `255` | `4.0.0.255` |

**Python Conversion:**
```python
hex_value = "0x0000000c"
decimal_value = int(hex_value, 16)  # Result: 12
version_string = f"4.0.0.{decimal_value}"  # Result: "4.0.0.12"
```

---

## Summary

| Platform | BIOS Column | Simics Column | UP Column | Format | Source |
|----------|-------------|---------------|-----------|--------|--------|
| **AP1 B0** | ✅ Version | ❌ Empty | ✅ Version | `4.0.0.[decimal]` | OSXML_Version.html |
| **AP2 A0** | ✅ Version | ❌ Empty | ✅ Version | `4.0.0.[decimal]` | OSXML_Version.html |
| **AP1 A0** | ❌ N/A | ❌ N/A | ❌ N/A | N/A | (No OSXML table) |

**Key Rules:** 
- SCF IPSD format: `4.0.0.[decimal_value]` where 4.0.0 is the major version prefix
- Simics column is always empty because this data is not available in Simics release notes

---

**End of SCF IPSD Rules Document**
