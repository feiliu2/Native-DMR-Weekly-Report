# Unified Patch Extraction Order (CRITICAL)

**Last Updated:** 2026-06-30

---

## ⚠️ CRITICAL: Binary File Format

**Simics.bin filename format:**
```
..._[BIOS_ID]_[AP2_A0_UP]_[AP1_B0_UP]_...
               ^^^^^^^^^^  ^^^^^^^^^^^
               1st hex     2nd hex
               index 0     index 1
```

**Order:** AP2 A0 comes FIRST, then AP1 B0

---

## Extraction Rules

| Platform | Binary Suffix | Extract Position | Array Index | Example |
|----------|---------------|------------------|-------------|---------|
| **AP1 A0** | `VIS.bin` | 1st hex | `[0]` | `800009AA` |
| **AP1 B0** | `Simics.bin` | **2nd hex** | `[1]` | `51000312` |
| **AP2 A0** | `Simics.bin` | **1st hex** | `[0]` | `5200020F` |

---

## Real Examples

### Example 1: AP2 A0

**Binary:**
```
OKSDCRB1_86B_2026.25.3.01_0036.D29_5200020F_51000312_0.883.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                    ^^^^^^^^^ ^^^^^^^^^
                                    AP2 A0    AP1 B0
                                    [0]       [1]
```

**Extraction:**
- Platform: AP2 A0
- Extract: `hex_values[0]` → `5200020F` ✅

---

### Example 2: AP1 B0

**Binary:**
```
OKSDCRB1_86B_2026.25.3.01_0036.D29_5200020F_51000312_0.883.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                    ^^^^^^^^^ ^^^^^^^^^
                                    AP2 A0    AP1 B0
                                    [0]       [1]
```

**Extraction:**
- Platform: AP1 B0
- Extract: `hex_values[1]` → `51000312` ✅

---

### Example 3: AP1 A0

**Binary:**
```
OKSDCRB1_86B_2026.26.4.01_0036.D54_800009AA_0.892.0_1P0_NonIPClean_Trace_DebugSigned_VIS.bin
                                   ^^^^^^^^^
                                   AP1 A0
                                   [0]
```

**Extraction:**
- Platform: AP1 A0
- Extract: `hex_values[0]` → `800009AA` ✅

---

## Why This Order?

**Historical Reason:** AP2 A0 was designed first, so its Unified Patch appears first in the binary filename.

**Binary Layout:**
```
[Common Prefix]_[BIOS_ID]_[AP2_UP]_[AP1_UP]_[Version]_[Suffix]
                           ^^^^^^   ^^^^^^
                           First    Second
```

---

## Common Mistake ❌

**Wrong assumption:**
```
Binary: ..._0036.D29_5200020F_51000312_...

❌ "AP1 B0 is 1st hex" → 5200020F
❌ "AP2 A0 is 2nd hex" → 51000312
```

**This is BACKWARDS!**

---

## Correct Logic ✅

```python
# After extracting hex values from binary filename
hex_values = ['5200020F', '51000312']
                 ^^^^^^^    ^^^^^^^^^
                 index 0    index 1
                 AP2 A0     AP1 B0

if platform_stepping == 'AP1 B0':
    unified_patch = hex_values[1]  # 51000312
elif platform_stepping == 'AP2 A0':
    unified_patch = hex_values[0]  # 5200020F
```

---

## Implementation

### Code Snippet

```python
if platform_stepping == 'AP1 A0':
    target_suffix = 'NonIPClean_Trace_DebugSigned_VIS.bin'
    extract_position = 1  # Only one hex value

elif platform_stepping in ['AP1 B0', 'AP2 A0']:
    target_suffix = 'NonIPClean_Trace_DebugSigned_Simics.bin'
    
    # CRITICAL: AP2 A0 is 1st, AP1 B0 is 2nd
    if platform_stepping == 'AP2 A0':
        extract_position = 1  # hex_values[0]
    else:  # AP1 B0
        extract_position = 2  # hex_values[1]

# Extract
match = re.search(r'_00\d{2}\.D\d+_((?:[A-F0-9]{8}_?)+)', filename)
hex_values = re.findall(r'([A-F0-9]{8})', match.group(1))

unified_patch = hex_values[extract_position - 1]  # Convert 1-based to 0-based
```

---

## Validation

### How to Verify Correct Extraction

1. **Check binary filename** in extraction log
2. **Identify all hex values** (should show both)
3. **Verify position** matches platform

**Example Log:**
```
[OK] Found Unified Patch from binary (position 1): 5200020F
     Binary file: ..._5200020F_51000312_...Simics.bin
     All UP values found: 5200020F, 51000312
     
Platform: AP2 A0
✅ Correct: position 1 → 5200020F (first hex)
```

---

## Summary Table

### Binary Hex Order

| Position | Index | Platform | Example Value |
|----------|-------|----------|---------------|
| 1st hex | `[0]` | **AP2 A0** | `5200020F` |
| 2nd hex | `[1]` | **AP1 B0** | `51000312` |

### Remember

**"AP2 comes FIRST in binary, not in alphabet!"**

---

**End of Unified Patch Order Document**
