# DMR IFWI Report Generator - Directory Structure

This document explains the reorganized directory structure following Claude Code skill standards.

---

## 📁 Root Directory Layout

```
dmr-ifwi-report-generator/
├── SKILL.md                 # ⭐ Skill definition (Claude Code entry point)
├── README.md                # Human-readable quick start
├── STRUCTURE.md             # This file (directory structure guide)
├── requirements.txt         # Python dependencies
├── START_HERE.bat          # Windows quick launcher
├── GIT_QUICK_START.md      # Git setup guide
│
├── scripts/                 # 🔧 Executable scripts (deterministic tasks)
├── references/              # 📚 Reference documentation (loaded as needed)
├── docs/                    # 📂 Legacy documentation (archived)
├── output/                  # 📄 Generated HTML reports
└── test/                    # 🧪 Test files and test data
```

---

## 📂 Directory Details

### `SKILL.md` (Root)
**Purpose**: Skill definition file - Claude Code's entry point  
**Contains**:
- Skill metadata (name, description, compatibility)
- When to use this skill
- Quick start workflow
- Critical rules summary
- Implementation guidance
- Common user scenarios
- Troubleshooting guide

**Usage**: Claude reads this first when skill is triggered

---

### `scripts/` - Executable Scripts
**Purpose**: Self-contained, deterministic scripts for repetitive tasks  
**Principle**: Scripts save future skill invocations from reinventing the wheel

#### PowerShell Scripts (Workflow Orchestration)
```
scripts/
├── Generate-IFWI-Report-From-Artifactory.ps1  # ⭐ Main entry point
├── Generate-IFWI-Report.ps1                   # Legacy FIV-based workflow
├── Generate-Multi-IFWI-Report.ps1             # Multi-Orange report
├── Install-Dependencies.ps1                   # Setup script
└── Cleanup-TempFiles.ps1                      # Cleanup utility
```

#### Python Scripts (Core Logic)
```
scripts/
├── search_artifactory_by_orange_id.py         # Search builds by Orange ID
├── construct_artifactory_url.py               # Build download URLs
├── extract_artifactory_osxml.py               # Extract all data from BuildPkg
├── extract_up_imh_osxml.py                    # Extract UP IMH OSXML
├── generate_ifwi_report.py                    # Generate single HTML report
└── generate_multi_ifwi_report.py              # Generate combined HTML report
```

#### Legacy Scripts
```
scripts/legacy/
├── run_test_ap1_a0.ps1                        # Old test runners
└── run_test_ap2_a0.ps1                        # (kept for reference)
```

**Design Pattern**:
- Each script is **single-purpose** and **self-contained**
- Can be called independently or chained in workflows
- Input/output via files or command-line arguments
- No hardcoded paths (use parameters)

---

### `references/` - Reference Documentation
**Purpose**: Documentation loaded into context as needed  
**Principle**: Progressive disclosure - only load what's relevant

#### Core References
```
references/
├── README.md                   # Documentation index
├── project-rules.md            # ⭐ Complete rule set (was CLAUDE.md)
├── quick-start.md              # Quick start guide (was START_HERE.md)
├── simplified-workflow.md      # Detailed workflow steps
├── artifactory-usage.md        # Artifactory API guide
├── platform-rules.md           # Platform-specific rules
├── simics-requirements.md      # Simics version requirements
└── api-token-guide.md          # API token instructions
```

**When to Read**:
- `project-rules.md` - Before any generation logic changes
- `quick-start.md` - When user is new to the tool
- `platform-rules.md` - When debugging platform detection
- `simics-requirements.md` - When handling Simics path issues

---

### `docs/` - Legacy Documentation
**Purpose**: Original documentation structure (now archived)  
**Status**: **Deprecated** - Use `references/` instead

```
docs/
├── archived/                   # Fully deprecated files
│   ├── DMR Weekly Report.md
│   ├── DEPLOYMENT_CHECKLIST.md
│   └── [other old docs...]
│
└── [various .md files]         # To be consolidated into references/
```

**Migration Plan**:
- ✅ Core rules → `references/project-rules.md`
- ✅ Quick start → `references/quick-start.md`
- ✅ Workflow → `references/simplified-workflow.md`
- ⏳ Other docs → Consolidate or archive

---

### `output/` - Generated Reports
**Purpose**: Storage for generated HTML reports and CSV data

```
output/
├── IFWI_Release_Status_2026.26.4.01.html      # Single Orange report
├── DMR_Weekly_Status_Report_20260629.html     # Multi-Orange report
├── OSXML_Summary_2026.26.4.01.csv             # Extracted data
└── [timestamped reports...]
```

**File Naming**:
- Single report: `IFWI_Release_Status_{Orange_ID}.html`
- Multi report: `DMR_Weekly_Status_Report_{YYYYMMDD}.html`
- CSV data: `OSXML_Summary_{Orange_ID}.csv`

---

### `test/` - Test Files
**Purpose**: Test scripts and sample data

```
test/
├── test_artifactory.py         # Artifactory API tests
├── test_detect_platform.py     # Platform detection tests
├── test_*.txt                  # Sample test data
└── [other test files...]
```

---

## 🎯 Skill Standard Compliance

This structure follows the **Claude Code Skill Standard**:

### ✅ Three-Level Loading System

1. **Metadata** (Always loaded)
   - `SKILL.md` frontmatter (name + description)
   - ~100 words, always in context

2. **Skill Body** (Loaded when skill triggers)
   - `SKILL.md` main content
   - <500 lines ideal
   - Clear pointers to references/

3. **Bundled Resources** (Loaded as needed)
   - `scripts/` - Execute without loading
   - `references/` - Load specific files when needed

### ✅ Progressive Disclosure Pattern

**Keep SKILL.md concise:**
- Overview and quick start in SKILL.md
- Detailed rules in `references/project-rules.md`
- Specific guides in other `references/*.md` files

**Clear pointers:**
```markdown
## Critical Rules

Read `references/project-rules.md` for complete rule set. Key rules:
- Rule 0: Simplified Workflow
- Rule 0.5: Platform-Specific Reports
- ...

[Brief summary in SKILL.md]
[Full details in references/project-rules.md]
```

### ✅ Script Organization

**When repeated work is detected across test cases:**
- Extract common logic into `scripts/`
- Make scripts reusable and parameterized
- Bundle with skill so future invocations can use them

**Example**: All test cases independently constructed Artifactory URLs
→ Created `construct_artifactory_url.py` once, reused everywhere

---

## 📋 File Count Summary

```
Root files:       5 (SKILL.md, README.md, STRUCTURE.md, requirements.txt, etc.)
scripts/:        15 Python + PowerShell scripts
references/:      8 reference documents
docs/:          ~30 files (legacy, to be consolidated)
output/:        Generated files (varies)
test/:           5+ test files
```

---

## 🔄 Migration Status

### ✅ Completed
- [x] Created `SKILL.md` with skill definition
- [x] Created `references/` directory
- [x] Copied core rules to `references/project-rules.md`
- [x] Copied quick start to `references/quick-start.md`
- [x] Created `references/README.md` index
- [x] Updated root `README.md` with skill structure

### ⏳ Pending
- [ ] Consolidate remaining `docs/*.md` into `references/`
- [ ] Archive fully deprecated `docs/archived/` files
- [ ] Add table of contents to `references/project-rules.md`
- [ ] Create `references/troubleshooting.md` from scattered docs
- [ ] Add examples to `references/` (sample CSVs, HTML outputs)

### 🗑️ To Archive
- [ ] `docs/archived/` - Move to separate archive directory
- [ ] Duplicate documentation across `docs/` and `references/`
- [ ] Old PowerShell test scripts in `scripts/legacy/`

---

## 🎓 For Developers

### Adding New Features

1. **Check rules first**: Read `references/project-rules.md`
2. **Add scripts**: Put new scripts in `scripts/`
3. **Document**: Update relevant `references/*.md` file
4. **Update SKILL.md**: Add brief pointer if it's a major feature
5. **Test**: Add test cases to `test/`

### Modifying Existing Logic

1. **Find the rule**: Search `references/project-rules.md`
2. **Understand context**: Read why the rule exists
3. **Update code**: Modify relevant scripts
4. **Update docs**: Keep references in sync
5. **Test all platforms**: AP1 A0, AP1 B0, AP2 A0

### Adding Documentation

**For reference material** (API guides, rules, workflows):
→ Add to `references/` and update `references/README.md`

**For examples** (sample outputs, test cases):
→ Add to `test/` or `references/examples/`

**For implementation notes** (code comments):
→ Keep minimal, explain WHY not WHAT

---

## 📚 Documentation Philosophy

### Skill vs. Reference Separation

**SKILL.md should be:**
- Concise (<500 lines)
- Action-oriented (how to use)
- High-level overview
- Clear pointers to references

**references/*.md should be:**
- Detailed and exhaustive
- Rule-based and authoritative
- Technical specifications
- Edge cases and examples

### Example Split

**In SKILL.md:**
```markdown
## Unified Patch Extraction

Extract UP version from binary filename based on platform.
See `references/project-rules.md` Rule 0.5 for details.

Key pattern: Check 2nd digit of version number.
```

**In references/project-rules.md:**
```markdown
## Rule 0.5: Unified Patch Extraction

**Critical**: Check 2nd digit of UP version, NOT position in filename.

| Platform | Pattern | Example |
|----------|---------|---------|
| AP1 A0   | 800009xx | 800009AA |
| AP1 B0   | 51xxxxxx | 51000312 |
| AP2 A0   | 52xxxxxx | 52000210 |

[Detailed extraction logic with code examples...]
[Edge cases...]
[Troubleshooting...]
```

---

## 🔍 Navigation Quick Reference

**I want to...**

- **Use this skill as Claude** → Read `SKILL.md`
- **Get started as human** → Read `README.md` then `references/quick-start.md`
- **Understand a rule** → Search `references/project-rules.md`
- **Run the workflow** → Execute `scripts/Generate-IFWI-Report-From-Artifactory.ps1`
- **Debug platform detection** → Check `references/platform-rules.md`
- **Fix Simics path issue** → Check `references/simics-requirements.md` and Rule 7
- **Get API token** → Follow `references/api-token-guide.md`
- **See all documentation** → Browse `references/README.md`

---

**Version**: 1.0  
**Last Updated**: 2026-07-03  
**Maintained By**: DMR IFWI Team
