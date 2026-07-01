# Simics Platform-Specific Paths

**Last Updated:** 2026-06-30

---

## Critical Rule: Platform-Specific Simics Paths

Different platforms use **different Simics Artifactory paths** for release notes.

---

## Path Mapping

| Platform | Simics Path | Full URL Pattern |
|----------|-------------|------------------|
| **AP1 B0** | `dmr-7` | `https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-7/{VERSION}/release_notes/daily_release_notification.md` |
| **AP2 A0** | `dmr-rio-7` | `https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-rio-7/{VERSION}/release_notes/daily_release_notification.md` |

---

## Why Different Paths?

- **AP1 B0** uses standard DMR platform → `dmr-7`
- **AP2 A0** uses RichIO variant → `dmr-rio-7`

**User Input Hint:** When user provides Simics info like "Simics dmr-rio-7 2026ww23.6.00_03", the platform name (`dmr-rio-7`) indicates it's for AP2 A0.

---

## Examples

### AP1 B0 Example

**Input:**
- Platform: AP1 B0
- Simics Version: `2026ww27.0.00_45`

**Generated URL:**
```
https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-7/2026ww27.0.00_45/release_notes/daily_release_notification.md
```

**Expected Content:**
```markdown
# Simics Diamond Rapids...

- **Current** DMR **B0** IMH regs: **dmr-imh-b0-1p0n-26ww17h**
- **Current** DMR **B0** CBB regs: **dmr-cbb-b0-26ww20a**
```

---

### AP2 A0 Example

**Input:**
- Platform: AP2 A0
- Simics Version: `2026ww23.6.00_03`

**Generated URL:**
```
https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/dmr-rio-7/2026ww23.6.00_03/release_notes/daily_release_notification.md
```

**Expected Content:**
```markdown
# Simics Diamond Rapids RichIO IMH2 1p0F and CBB C0...

- **Current** DMR **A0** IMH2 regs: **dmr-imh2-1p0f-26ww05**
- **Current** DMR **C0** CBB regs: **dmr-cbb-c0-1p0-26ww12b**
```

---

## Implementation

### Python Code

```python
def download_simics_release_notes(simics_version, api_token, platform_stepping):
    """Download Simics release notes with platform-specific path."""
    
    # Choose platform path based on platform_stepping
    if platform_stepping == 'AP1 B0':
        platform_path = 'dmr-7'
    elif platform_stepping == 'AP2 A0':
        platform_path = 'dmr-rio-7'
    else:
        platform_path = 'dmr-7'  # Default fallback
    
    url = f"https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/{platform_path}/{simics_version}/release_notes/daily_release_notification.md"
    
    # Download and parse...
```

### Call Site

```python
# In main extraction flow
if simics_version and user_platform_stepping in ['AP1 B0', 'AP2 A0']:
    simics_osxml = download_simics_release_notes(
        simics_version, 
        api_token, 
        user_platform_stepping  # ← Pass platform to determine path
    )
```

---

## Common Error: HTTP 404

### Symptom
```
[ERROR] Simics release notes not found (HTTP 404)
Version '2026ww23.6.00_03' may not exist or URL is incorrect
```

### Cause
Using wrong platform path:
- ❌ AP2 A0 with `dmr-7` → 404 error
- ✅ AP2 A0 with `dmr-rio-7` → Success

### Solution
Always pass `platform_stepping` to `download_simics_release_notes()` so it can choose the correct path.

---

## Testing

### Test AP1 B0
```bash
# Should use dmr-7
python extract_artifactory_osxml.py <url> <token> . "AP1 B0" "2026ww27.0.00_45"
# Expected: Downloads from .../dmr-7/2026ww27.0.00_45/...
```

### Test AP2 A0
```bash
# Should use dmr-rio-7
python extract_artifactory_osxml.py <url> <token> . "AP2 A0" "2026ww23.6.00_03"
# Expected: Downloads from .../dmr-rio-7/2026ww23.6.00_03/...
```

---

## Summary

| Platform | Path | Release Notes |
|----------|------|---------------|
| AP1 B0 | `dmr-7` | DMR standard platform |
| AP2 A0 | `dmr-rio-7` | DMR RichIO variant |

**Key Point:** System must dynamically select the correct path based on `platform_stepping` parameter.

---

**End of Platform Paths Document**
