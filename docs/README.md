# DMR Weekly Report

从 FIV Portal 或 Artifactory 自动提取固件版本信息并生成周报的工具。

## 快速开始

💡 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 快速参考卡片（新手推荐！）

---

### 方式 1: 从 FIV Portal（原有方式）

```powershell
.\Generate-IFWI-Report.ps1
```

适用于 Pre-Silicon 发布（包含 Simics 数据）

### 方式 2: 从 Artifactory（新方式）⭐

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

适用于 Post-Silicon 和 Pre-Silicon 发布（直接从构建包提取）

**🎉 简化输入（推荐）：**
1. **平台选择**（从菜单：AP1 A0/AP1 B0/AP2 A0）
2. **版本号**（格式：`2026.26.4.01.0036.D.54`）
3. **Release Info**（格式：`released on WWxx.x`）

系统自动构建 Artifactory URL，无需手动复制！

**传统输入（仍支持）：**
1. Download Link（完整 Artifactory URL）
2. Platform/Stepping
3. Release Info

## 环境要求

### FIV Portal 方式
- Python 3.8+
- Selenium + ChromeDriver
- PowerShell 5.1+

### Artifactory 方式（推荐）
- Python 3.8+
- Artifactory API Token
- PowerShell 5.1+

首次使用运行：
```powershell
.\Install-Dependencies.ps1
```

## 完整文档

### ⚠️ 开发者必读

🔴 **[CRITICAL_RULES.md](CRITICAL_RULES.md)** - **最容易出错的关键规则（修改代码前必读！）**

### 使用指南

🌟 **[SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md)** - 简化工作流：从平台+版本直接生成报告（最新！）

📖 **[SETUP_ARTIFACTORY.md](SETUP_ARTIFACTORY.md)** - Artifactory 数据源设置指南

📖 **[ARTIFACTORY_USAGE.md](ARTIFACTORY_USAGE.md)** - Artifactory 工作流详细使用说明

📖 **[DMR Weekly Report.md](DMR%20Weekly%20Report.md)** - FIV Portal 工作流使用说明

### 技术规则

📖 **[CLAUDE.md](CLAUDE.md)** - 项目规则和约束（完整版）

📖 **[PLATFORM_RULES.md](PLATFORM_RULES.md)** - 平台特定规则

📖 **[SCF_IPSD_RULES.md](SCF_IPSD_RULES.md)** - SCF IPSD 提取规则

📖 **[UP_IMH_OSXML_EXTRACTION.md](UP_IMH_OSXML_EXTRACTION.md)** - Unified Patch IMH OSXML 提取（新功能⭐）

---

**两种数据源对比：**

| 特性 | FIV Portal | Artifactory ⭐ |
|------|-----------|---------------|
| 认证方式 | 浏览器自动化 | API Token |
| 速度 | 较慢（15-30秒） | 较快（5-10秒） |
| 适用场景 | Pre-Silicon | Post-Silicon |
| Simics 数据 | ✓ 有 | 可能没有 |
| OSXML 数据 | ✓ 有 | ✓ 有 |
| PnP/PM 数据 | ✓ 有 | ✓ 有 |
