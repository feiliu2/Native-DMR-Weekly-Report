# Unified Patch Version Pattern Rules

**Critical Update:** 2026-06-30

---

## Executive Summary

**DO NOT** rely on position in binary filename to determine which Unified Patch belongs to which platform!

**Instead:** Check the **2nd digit** of the UP version number:
- `5_1_xxxxxx` (2nd digit = **1**) → **AP1 B0**
- `5_2_xxxxxx` (2nd digit = **2**) → **AP2 A0**

---

## The Problem

Previously, the system assumed a fixed binary format:
```
..._[AP2_UP]_[AP1_UP]_...
```

This led to errors because the actual binary format can vary, and position alone is unreliable.

---

## The Solution

**Version Number Pattern Matching**

The UP version number itself contains the platform identifier in the **2nd digit**:

### Pattern Rules

| Version Pattern | 2nd Digit | Platform | Example |
|-----------------|-----------|----------|---------|
| **5_1_xxxxxx** | **1** | **AP1 B0** | `51000312` |
| **5_2_xxxxxx** | **2** | **AP2 A0** | `52000210` |
| **800009xx** | N/A | **AP1 A0** (Post-Si) | `800009AA` |

### Real Example

**Binary filename:**
```
OKSDCRB1_86B_2026.26.4.02_0036.D54_51000312_52000210_0.892.0_NonIPClean_Trace_DebugSigned_Simics.bin
                                    ^^^^^^^^ ^^^^^^^^
                                    51000312 52000210
```

**Analysis:**
- `51000312` → 2nd digit is **1** → **AP1 B0** ✅
- `52000210` → 2nd digit is **2** → **AP2 A0** ✅

**For AP2 A0 platform:**
- ✅ **Correct**: Extract `52000210` (by checking 2nd digit = 2)
- ❌ **Wrong**: Extract by position (might get 51000312)

---

## Implementation

### Old Logic (WRONG)

```python
# WRONG - relies on position
if platform_stepping == 'AP1 B0':
    extract_position = 1  # Assumes 1st hex
elif platform_stepping == 'AP2 A0':
    extract_position = 2  # Assumes 2nd hex

unified_patch = hex_values[extract_position - 1]
```

**Problem:** If binary format changes or values are in different order, extraction fails!

---

### New Logic (CORRECT)

```python
# CORRECT - matches by version pattern
hex_values = ['51000312', '52000210']  # All hex values from binary

if platform_stepping == 'AP1 B0':
    # Look for 5X1XXXXX pattern (2nd digit is 1)
    for up_value in hex_values:
        if len(up_value) >= 2 and up_value[1] == '1':
            unified_patch = up_value  # Returns '51000312'
            break

elif platform_stepping == 'AP2 A0':
    # Look for 5X2XXXXX pattern (2nd digit is 2)
    for up_value in hex_values:
        if len(up_value) >= 2 and up_value[1] == '2':
            unified_patch = up_value  # Returns '52000210'
            break
```

**Advantage:** Works regardless of order in binary filename!

---

## Why This Matters

### Case Study: AP2 A0 Extraction

**Old system (position-based):**
1. Assumes AP2 is always 1st hex
2. Extracts `51000312` for AP2 A0
3. Tries to download: `.../IMH2_B0_DMRAP_Unified_Patch/51000312/...`
4. **HTTP 404 Error** ❌ (package doesn't exist for AP2)

**New system (pattern-based):**
1. Searches for 2nd digit = '2'
2. Finds `52000210` 
3. Downloads: `.../IMH2_B0_DMRAP_Unified_Patch/52000210/...`
4. **Success!** ✅ (correct package)

---

## Validation

### Test Cases

**Test 1: AP1 B0**
```
Binary: ..._51000312_52000210_...
Platform: AP1 B0
Expected: 51000312 (2nd digit is 1)
Result: ✅ PASS
```

**Test 2: AP2 A0**
```
Binary: ..._51000312_52000210_...
Platform: AP2 A0
Expected: 52000210 (2nd digit is 2)
Result: ✅ PASS
```

**Test 3: AP1 A0 (Post-Si)**
```
Binary: ..._800009AA_...
Platform: AP1 A0
Expected: 800009AA (1st hex, no digit check needed)
Result: ✅ PASS
```

---

## Edge Cases

### What if there are multiple 51xxxxxx values?

```python
hex_values = ['51000312', '51000400', '52000210']

# System returns the FIRST match
for up_value in hex_values:
    if up_value[1] == '1':
        return up_value  # Returns '51000312'
```

**Solution:** This is rare, but if it happens, the first match is used.

### What if no match is found?

```python
hex_values = ['60000000', '70000000']  # No 51xxx or 52xxx

# No match found
unified_patch = None
print("[WARN] No Unified Patch found with expected pattern")
```

**Solution:** System logs warning and continues without UP data.

---

## Documentation Updates

**Files updated to reflect new rules:**
- ✅ `extract_artifactory_osxml.py` - Implementation
- ✅ `CRITICAL_RULES.md` - Critical rule #2
- ✅ `CLAUDE.md` - Project rules and summary table
- ✅ `UP_VERSION_PATTERN_RULES.md` - This document

---

## Key Takeaways

1. **Never assume position** - Binary format can vary
2. **Always check 2nd digit** - This is the platform identifier
3. **5_1_xxxxxx = AP1 B0** - Digit 1 means AP1
4. **5_2_xxxxxx = AP2 A0** - Digit 2 means AP2
5. **Test with real data** - Validate against actual binary filenames

---

## Related Documentation

- [CRITICAL_RULES.md](CRITICAL_RULES.md) - Full critical rules list
- [CLAUDE.md](CLAUDE.md) - Complete project rules
- [extract_artifactory_osxml.py:170-240](extract_artifactory_osxml.py#L170-L240) - Implementation

---

**Last Updated:** 2026-06-30  
**Rule Status:** ✅ Implemented and Tested  
**Priority:** 🔴 **CRITICAL**
