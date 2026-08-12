# DMR IFWI Report Generator

Automated generation of DMR IFWI weekly status reports from Artifactory build packages.

---

## ⚡ Generate a report right now

Paste your release sentence as the argument - that is the whole workflow:

```bash
python dmr_report.py "AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5"
```

Pre-Si platforms (AP1 B0 / AP2 A0) also need the Simics version, and you can pass
several releases at once:

```bash
python dmr_report.py "AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5" \
                     "AP2 A0 Pre-Si Orange IFWI 2026.10.1.05 is trend to be released on WW10.5  dmr-rio-7 2026ww09.1.00_01 Pre500"
```

Prefer not to type? Run `python dmr_report.py` with no arguments (or double-click
**`DMR_REPORT.bat`**) and paste the release lines when prompted.

The script fetches the real BIOS / Unified Patch / OSXML versions from Artifactory,
writes `output/IFWI_Release_Status_<orange-id>.html`, and opens it in your browser.
No Claude Code required.

**First time:** `pip install requests py7zr beautifulsoup4`, be on the Intel network
or VPN, and have your Artifactory API token ready
(https://af01p-or.devtools.intel.com → Edit Profile → API Key). The script asks for
the token once and offers to remember it.

📖 Full usage, release-line format, and troubleshooting: **[HOW_TO_RUN.md](HOW_TO_RUN.md)**

---

## 🎯 What This Does

Automates the entire workflow of:
1. Searching Artifactory for IFWI builds by Orange ID
2. Extracting version data (BIOS, Simics, Unified Patch, OSXML)
3. Generating formatted HTML weekly status reports

Supports three platform types:
- **AP1 A0** (Post-Si) - Simplified reports
- **AP1 B0** (Pre-Si) - Full reports with OSXML tables
- **AP2 A0** (Pre-Si) - Full reports with OSXML tables

---

## 🚀 The release line

The parser pulls four things out of your sentence, in any order and any wording:

| Needs | Looks like | Notes |
|-------|-----------|-------|
| Platform | `AP1 A0`, `AP1 B0`, `AP2 A0` | `DMR-AP-UCC` / `DMR-AP-MCC` prefixes and `o`/`•` bullets are ignored |
| Orange IFWI ID | `2026.10.1.01` | |
| Release week | `... on WW10.5` | |
| Simics version | `dmr-rio-7 2026ww09.1.00_01 Pre500` | **Pre-Si only** (AP1 B0 / AP2 A0) |

Wording controls the tense in the report:

| You write | Report says |
|-----------|-------------|
| `is trend to be released on WW10.5` | is trend to be released on WW10.5 |
| `will be released on WW10.5` | will be released on WW10.5 |
| `released on WW10.5` | has been released on WW10.5 |

---

## 📁 Skill Structure

```
dmr-ifwi-report-generator/
├── dmr_report.py            # ⭐ START HERE - paste release line, get HTML
├── DMR_REPORT.bat           # Double-click launcher for dmr_report.py
├── HOW_TO_RUN.md            # Full usage guide (no Claude Code needed)
├── SKILL.md                 # Skill definition (for Claude Code)
├── README.md                # This file (human quick start)
├── requirements.txt         # Python dependencies
│
├── scripts/                 # 🔧 Executable scripts
│   ├── generate_dmr_report.py  # Pipeline core, used by dmr_report.py
│   ├── Generate-IFWI-Report-From-Artifactory.ps1  # Legacy PowerShell entry point
│   ├── search_artifactory_by_orange_id.py
│   ├── construct_artifactory_url.py
│   ├── extract_artifactory_osxml.py
│   ├── generate_ifwi_report.py
│   └── [other scripts...]
│
├── references/              # 📚 Reference documentation
│   ├── README.md            # Documentation index
│   ├── project-rules.md     # Complete rule set
│   ├── quick-start.md       # Quick start guide
│   ├── artifactory-usage.md # Artifactory API guide
│   └── [other guides...]
│
├── output/                  # 📄 Generated reports
│   └── IFWI_Release_Status_*.html
│
└── test/                    # 🧪 Test files
    └── test_*.py
```

---

## 📖 Documentation

### For Claude Code Users
- **[SKILL.md](SKILL.md)** - Complete skill definition and usage guide

### For Human Users
- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - Generate reports with plain Python, no Claude Code
- **[references/quick-start.md](references/quick-start.md)** - Detailed quick start
- **[references/project-rules.md](references/project-rules.md)** - All generation rules
- **[references/README.md](references/README.md)** - Documentation index

### Legacy Documentation
- **[docs/](docs/)** - Original documentation (archived, use `references/` instead)

---

## 🔑 Platform Types

| Platform | Silicon Type | Report Type | OSXML Table | uBIOS Statement |
|----------|--------------|-------------|-------------|-----------------|
| AP1 A0   | Post-Si      | Simplified  | ❌ No       | ❌ No           |
| AP1 B0   | Pre-Si       | Full        | ✅ Yes      | ✅ Yes          |
| AP2 A0   | Pre-Si       | Full        | ✅ Yes      | ✅ Yes          |

---

## 📝 Example Output

### AP1 B0 Pre-Si Report
```
DMR-AP-UCC AP1 B0 Pre-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

Release version information as below:
- BIOS Binary: 0036.D54
- Simics: dmr-7 2026ww24.3.00_45 Pre712
- Unified Patch: 51000312

[OSXML Table with IMH, CBB, SCF IPSD data]
[PnP/PM Recipe Table with IIO, MC, UNCORE data]

AP1 B0 uBIOS based on BIOSID 0036.D54 will be released on WW26.6
```

### AP1 A0 Post-Si Report (Simplified)
```
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

Release version information as below:
- BIOS Binary: 0036.D54
- Unified Patch: 800009AA
```

---

## 🛠️ Common Operations

### Generate Single Report
```bash
python dmr_report.py "AP1 A0 Post-Si Orange IFWI 2026.10.1.01 is trend to be released on WW10.5"
```

### Generate Several Reports
```bash
# One release line per argument, or one per line in a file
python dmr_report.py "<release line 1>" "<release line 2>"
python dmr_report.py -f releases.txt
```

### Other Flags
```bash
python dmr_report.py --token <tok>    # use a token without saving it
python dmr_report.py --no-browser     # don't pop open the report
python dmr_report.py --help           # show usage
```

### Clean Temporary Files
```powershell
.\scripts\Cleanup-TempFiles.ps1
```

### Install/Update Dependencies
```powershell
.\scripts\Install-Dependencies.ps1
```

---

## 🆘 Troubleshooting

### Authentication Failed
**Solution**: Regenerate API token at https://af01p-or.devtools.intel.com

### Build Not Found
**Solution**: Verify Orange ID exists in Artifactory manually

### Wrong Platform Detected
**Solution**: Check platform detection logic (Rule 3 in `references/project-rules.md`)

### Simics OSXML Missing
**Solution**: Verify Simics version format and 'rio' keyword handling (Rule 7)

For more help: See `docs/INSTALL_TROUBLESHOOTING.md`

---

## 📞 Support

- **Issues**: Check `references/project-rules.md` for all rules
- **API Token**: See `references/api-token-guide.md`
- **Workflow**: See `references/simplified-workflow.md`
- **Full Docs**: See `references/README.md`

---

## 🎓 For Claude Code

When using this skill:
1. **Read `SKILL.md` first** - Contains complete skill instructions
2. **Check `references/project-rules.md`** - All 7 critical rules
3. **Use scripts in `scripts/`** - Pre-built, tested modules
4. **Reference `references/`** - Detailed guides as needed

---

**Version**: 1.0  
**Last Updated**: 2026-07-03  
**Maintained By**: DMR IFWI Team  
**Generated With**: Claude Code
