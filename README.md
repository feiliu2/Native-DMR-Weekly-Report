# DMR IFWI Report Generator

**Claude Code Skill** for automated generation of DMR IFWI weekly status reports from Artifactory build packages.

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

## 🚀 Quick Start (60 seconds)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Get API Token
Visit: https://af01p-or.devtools.intel.com → Edit Profile → Copy API Key

### 3. Run
```powershell
.\scripts\Generate-IFWI-Report-From-Artifactory.ps1
```

### 4. Provide Info
- Platform: `AP1 A0` / `AP1 B0` / `AP2 A0`
- Orange ID: `2026.26.4.01`
- Simics (Pre-Si only): `dmr-7 2026ww24.3.00_45 Pre712`
- Release: `released on WW26.5`
- API Token: `[paste]`

### 5. Done!
HTML report opens automatically in your browser 🎉

---

## 📁 Skill Structure

```
dmr-ifwi-report-generator/
├── SKILL.md                 # ⭐ Skill definition (START HERE for Claude)
├── README.md                # This file (human quick start)
├── requirements.txt         # Python dependencies
│
├── scripts/                 # 🔧 Executable scripts
│   ├── Generate-IFWI-Report-From-Artifactory.ps1  # Main entry point
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
```powershell
.\scripts\Generate-IFWI-Report-From-Artifactory.ps1
# Select 1 Orange IFWI when prompted
```

### Generate Combined Multi-Report
```powershell
.\scripts\Generate-IFWI-Report-From-Artifactory.ps1
# Select multiple Orange IFWIs when prompted
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
