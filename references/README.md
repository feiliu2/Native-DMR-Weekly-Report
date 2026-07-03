# Reference Documentation

This directory contains all reference documentation for the DMR IFWI Report Generator skill.

## Core Documentation

### 📋 Project Rules
- **[project-rules.md](project-rules.md)** - Complete rule set for report generation
  - Rule 0: Simplified Workflow
  - Rule 0.5: Platform-Specific Reports (AP1 A0/B0, AP2 A0)
  - Rule 0.6: Platform-Specific OSXML Extraction
  - Rule 0.7: Unified Patch IMH OSXML Extraction
  - Rule 7: Simics Rio Detection

### 🚀 Quick Start Guides
- **[quick-start.md](quick-start.md)** - 5-minute quick start for new users
- **[simplified-workflow.md](simplified-workflow.md)** - Detailed step-by-step workflow

### 🔧 Technical Guides
- **[artifactory-usage.md](artifactory-usage.md)** - Artifactory API usage and authentication
- **[platform-rules.md](platform-rules.md)** - Platform-specific extraction rules
- **[simics-requirements.md](simics-requirements.md)** - Simics version requirements and paths
- **[api-token-guide.md](api-token-guide.md)** - How to obtain Artifactory API token

## Document Organization

### When to Read Each Document

**Starting a new report generation:**
1. Read `quick-start.md` first
2. Get API token from `api-token-guide.md`
3. Follow `simplified-workflow.md` for detailed steps

**Troubleshooting extraction issues:**
1. Check `project-rules.md` for relevant rules
2. Verify platform logic in `platform-rules.md`
3. Check Simics path in `simics-requirements.md`

**Implementing new features:**
1. Review `project-rules.md` for all constraints
2. Understand Artifactory APIs from `artifactory-usage.md`
3. Test with platform-specific rules from `platform-rules.md`

## Key Concepts

### Platform Types

| Platform | Silicon Type | Report Type | OSXML Table | uBIOS |
|----------|--------------|-------------|-------------|-------|
| AP1 A0   | Post-Si      | Simplified  | ❌ No       | ❌ No |
| AP1 B0   | Pre-Si       | Full        | ✅ Yes      | ✅ Yes |
| AP2 A0   | Pre-Si       | Full        | ✅ Yes      | ✅ Yes |

### Orange ID Format

Format: `YYYY.WW.X.NN`
- YYYY = Year (e.g., 2026)
- WW = Work Week (e.g., 26)
- X = Build number (e.g., 4)
- NN = Revision (e.g., 01)

Example: `2026.26.4.01`

### OSXML Data Sources

For Pre-Si platforms (AP1 B0, AP2 A0), OSXML data comes from three sources:

1. **BIOS OSXML** - From BuildPkg OSXML files
2. **Simics OSXML** - From Simics release notes
3. **Unified Patch OSXML** - From UP release notes (IMH only)

### Unified Patch Extraction

**Critical**: Check 2nd digit of UP version number:
- `51xxxxxx` = AP1 B0
- `52xxxxxx` = AP2 A0
- `800009xx` = AP1 A0 (Post-Si)

## Common Issues and Solutions

### Authentication Issues
**Problem**: 401 Unauthorized  
**Solution**: Regenerate API token at Artifactory (see `api-token-guide.md`)

### Platform Detection Issues
**Problem**: Wrong platform detected  
**Solution**: Check Orange Report page text (see Rule 3 in `project-rules.md`)

### OSXML Extraction Issues
**Problem**: Wrong OSXML value for platform  
**Solution**: Check platform-specific indices (see Rule 0.6 in `project-rules.md`)

### Simics Path Issues
**Problem**: Simics release notes not found  
**Solution**: Check for 'rio' keyword in user input (see Rule 7 in `project-rules.md`)

## Rule Quick Reference

| Rule | Topic | Key Point |
|------|-------|-----------|
| 0 | Simplified Workflow | User provides 4-5 inputs, system auto-discovers |
| 0.5 | Platform Reports | AP1 A0 = simplified, AP1 B0 / AP2 A0 = full |
| 0.6 | OSXML Extraction | IMH and CBB have different platform indices |
| 0.7 | UP IMH OSXML | Extract from UP release notes for Pre-Si |
| 1 | Orange ID Auto-detect | Extract from FIV URL if provided |
| 2 | Conditional Tables | Hide OSXML columns if no data |
| 3 | Platform Detection | Use Orange Report page text, not BIOS ID |
| 4 | uBIOS Statement | Auto-calculate week (Orange week + 1 day) |
| 5 | Report Header | Remove redundant Orange/BIOS ID from header |
| 6 | Release Tense | Detect from user input (will be/has been) |
| 7 | Simics Rio Path | Check 'rio' in user input, not platform |

## Version Control

These reference documents are the authoritative source for all report generation logic. When making changes to scripts or workflows:

1. ✅ **Always check rules first** - Read relevant sections in `project-rules.md`
2. ✅ **Update docs when changing logic** - Keep references in sync with code
3. ✅ **Test platform-specific cases** - Verify AP1 A0, AP1 B0, AP2 A0 all work
4. ✅ **Document edge cases** - Add new patterns to relevant reference docs

## For Developers

When implementing new features or fixing bugs:

1. **Read the rule** - Find the relevant rule in `project-rules.md`
2. **Understand the why** - Rules exist to handle real-world edge cases
3. **Test all platforms** - AP1 A0/B0 and AP2 A0 behave differently
4. **Update references** - Keep documentation current

## For Users

When generating reports:

1. **Start with quick-start.md** - Get up and running in 5 minutes
2. **Get your API token** - Follow `api-token-guide.md`
3. **Run the script** - Use `Generate-IFWI-Report-From-Artifactory.ps1`
4. **Check the output** - HTML report opens automatically

---

**Last Updated**: 2026-07-03  
**Maintained By**: DMR IFWI Team  
**Skill Version**: 1.0
