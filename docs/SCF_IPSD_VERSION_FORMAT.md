# SCF IPSD Version Format

**Last Updated:** 2026-06-30

---

## Format Specification

**Version String:** `4.0.0.[decimal_value]`

- **Major Version:** `4.0.0` (fixed, not parsed from HTML)
- **Minor Version:** `[decimal_value]` (converted from hex in OSXML_Version.html)

---

## Conversion Process

### Step 1: Extract Hex Value from HTML

```html
<td>IpScfMgr</td>
<td>0x000004eb</td>
```

### Step 2: Convert Hex to Decimal

```python
hex_value = "0x000004eb"
decimal_value = int(hex_value, 16)
# Result: 1259
```

### Step 3: Add Major Version Prefix

```python
version_string = f"4.0.0.{decimal_value}"
# Result: "4.0.0.1259"
```

---

## Examples

| HTML Hex Value | Decimal | Final Version String |
|----------------|---------|----------------------|
| `0x0000000c` | 12 | `4.0.0.12` |
| `0x000004eb` | 1259 | `4.0.0.1259` |
| `0x00000010` | 16 | `4.0.0.16` |
| `0x000000ff` | 255 | `4.0.0.255` |
| `0x00000001` | 1 | `4.0.0.1` |

---

## Report Display

### CSV Format

```csv
Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
SCF_IPSD,4.0.0.1259,N/A,4.0.0.1259
```

### HTML Table

```
┌───────────────┬──────────┬────────────┬────────────┬──────────────┐
│               │ Version  │ IMH OSXML  │ CBB OSXML  │ SCF IPSD     │
├───────────────┼──────────┼────────────┼────────────┼──────────────┤
│ BIOS Binary   │ 0036.D29 │ IMH2...    │ CBB_C0...  │ 4.0.0.1259   │
│ Simics        │ dmr-7... │ dmr-imh2...│ dmr-cbb... │ (empty)      │
│ Unified Patch │ 5200020F │ N/A        │ N/A        │ 4.0.0.1259   │
└───────────────┴──────────┴────────────┴────────────┴──────────────┘
```

---

## Why Major Version 4.0.0?

**Historical Context:**
- SCF IPSD versioning follows a semantic versioning scheme
- Major version `4.0.0` represents the current architecture generation
- Only the minor version (last component) is stored in OSXML as hex

**Not Parsed:**
- The `4.0.0` prefix is **NOT** extracted from OSXML_Version.html
- It is a **constant** that must be prepended to the parsed decimal value

---

## Implementation

### Python Code

```python
def extract_scf_ipsd_version(soup):
    """Extract SCF IPSD version and format as 4.0.0.[decimal]."""
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = [c.get_text(strip=True) for c in row.find_all(['td', 'th'])]
            
            for i, cell_text in enumerate(cells):
                if cell_text in ['IpScfMgrGen5', 'IpScfMgr']:
                    if i + 1 < len(cells):
                        hex_value = cells[i + 1].strip()
                        
                        if hex_value.startswith('0x'):
                            decimal_value = int(hex_value, 16)
                            # CRITICAL: Add major version prefix
                            version_string = f"4.0.0.{decimal_value}"
                            return version_string
    
    return None
```

### Usage in Main Flow

```python
# After platform is determined
if final_platform in ['AP1 B0', 'AP2 A0']:
    scf_ipsd_version = extract_scf_ipsd_version(soup)
    
    if scf_ipsd_version:
        # scf_ipsd_version is already formatted as "4.0.0.[decimal]"
        data['osxml_data']['SCF_IPSD']['bios'] = scf_ipsd_version
        data['osxml_data']['SCF_IPSD']['up'] = scf_ipsd_version
        data['osxml_data']['SCF_IPSD']['simics'] = None
```

---

## Validation

### Expected vs Wrong

| Scenario | ❌ Wrong | ✅ Correct |
|----------|---------|-----------|
| Basic | `1259` | `4.0.0.1259` |
| Small value | `12` | `4.0.0.12` |
| Single digit | `1` | `4.0.0.1` |
| Large value | `65535` | `4.0.0.65535` |

### Common Mistakes

1. **Missing prefix:**
   ```python
   # ❌ WRONG
   return str(decimal_value)  # Returns "1259"
   
   # ✅ CORRECT
   return f"4.0.0.{decimal_value}"  # Returns "4.0.0.1259"
   ```

2. **Wrong separator:**
   ```python
   # ❌ WRONG
   return f"4-0-0-{decimal_value}"  # Wrong separator
   
   # ✅ CORRECT
   return f"4.0.0.{decimal_value}"  # Uses dots
   ```

3. **Hardcoded decimal:**
   ```python
   # ❌ WRONG
   return "4.0.0.1259"  # Hardcoded for one case only
   
   # ✅ CORRECT
   return f"4.0.0.{decimal_value}"  # Dynamic based on hex
   ```

---

## Testing

### Test Script

```python
import pytest

def test_scf_ipsd_version_format():
    test_cases = [
        ("0x0000000c", "4.0.0.12"),
        ("0x000004eb", "4.0.0.1259"),
        ("0x00000001", "4.0.0.1"),
        ("0x000000ff", "4.0.0.255"),
    ]
    
    for hex_val, expected in test_cases:
        decimal = int(hex_val, 16)
        result = f"4.0.0.{decimal}"
        assert result == expected, f"Expected {expected}, got {result}"
```

### Manual Verification

1. Check extraction log:
   ```
   Found IpScfMgr: 0x000004eb -> Decimal: 1259 -> Version: 4.0.0.1259
   ```

2. Check CSV output:
   ```csv
   SCF_IPSD,4.0.0.1259,N/A,4.0.0.1259
   ```

3. Check HTML report:
   - Look for `<td>4.0.0.1259</td>` in OSXML table
   - Verify format includes `4.0.0.` prefix

---

## Summary

| Component | Value |
|-----------|-------|
| **Major Version** | `4.0.0` (constant) |
| **Minor Version** | Parsed from hex, converted to decimal |
| **Format** | `4.0.0.[decimal]` |
| **Example** | `4.0.0.1259` |

**Key Point:** Always include the `4.0.0.` prefix when displaying SCF IPSD version.

---

**End of SCF IPSD Version Format Document**
