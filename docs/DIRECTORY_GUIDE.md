# 📁 目录结构说明

## 项目根目录文件

| 文件/目录 | 作用 | 说明 |
|---------|------|------|
| **📄 README.md** | 项目主页 | 项目简介、快速开始、使用说明 |
| **📄 requirements.txt** | Python依赖 | 列出所有需要安装的Python包 |
| **🚀 START_HERE.bat** | 快速启动器 | 双击运行，快速开始生成报告 |
| **⚙️ .claude/** | Claude配置 | Claude Code的项目配置和记忆 |
| **🔧 __pycache__/** | Python缓存 | Python自动生成的字节码缓存 |

---

## 📚 docs/ - 文档目录

**作用：** 存放所有项目文档、规则说明、操作指南

### 核心文档

| 文件 | 作用 | 优先级 |
|------|------|--------|
| **CLAUDE.md** | 项目规则总纲 | ⭐⭐⭐ 必读！完整的项目约束和规则 |
| **START_HERE.md** | 快速开始指南 | ⭐⭐⭐ 新手入门 |
| **README.md** | 项目概述 | ⭐⭐ 项目简介 |
| **QUICK_START_ARTIFACTORY.md** | Artifactory快速指南 | ⭐⭐⭐ 主要工作流 |
| **SIMPLIFIED_WORKFLOW.md** | 简化工作流 | ⭐⭐ 了解简化流程 |

### 配置指南

| 文件 | 作用 |
|------|------|
| **HOW_TO_GET_API_TOKEN.md** | 如何获取Artifactory API Token |
| **SETUP_ARTIFACTORY.md** | Artifactory环境配置 |
| **INSTALL_TROUBLESHOOTING.md** | 安装问题排查 |
| **DEPLOYMENT_CHECKLIST.md** | 部署检查清单 |

### 规则文档

| 文件 | 作用 |
|------|------|
| **RULES_SUMMARY.md** | 规则总结 |
| **CRITICAL_RULES.md** | 关键规则 |
| **CONSTRAINTS.md** | 项目约束 |
| **PLATFORM_RULES.md** | 平台规则（AP1/AP2/A0/B0） |
| **SIMICS_RIO_RULE.md** | Simics路径检测规则（Rule 7） |
| **SIMICS_REQUIREMENTS.md** | Simics要求说明 |
| **SIMICS_PLATFORM_PATHS.md** | Simics平台路径 |

### 技术细节

| 文件 | 作用 |
|------|------|
| **UNIFIED_PATCH_ORDER.md** | Unified Patch提取顺序 |
| **UP_VERSION_PATTERN_RULES.md** | UP版本模式规则 |
| **UP_IMH_OSXML_EXTRACTION.md** | UP IMH OSXML提取说明 |
| **UP_IMH_OSXML_TEST_RESULTS.md** | UP IMH OSXML测试结果 |
| **SCF_IPSD_RULES.md** | SCF IPSD规则 |
| **SCF_IPSD_VERSION_FORMAT.md** | SCF IPSD版本格式 |
| **ARTIFACTORY_USAGE.md** | Artifactory使用说明 |

### 索引文档

| 文件 | 作用 |
|------|------|
| **DOCUMENTATION_INDEX.md** | 文档索引 |
| **QUICK_REFERENCE.md** | 快速参考 |

### 其他

| 文件 | 作用 |
|------|------|
| **DMR Weekly Report.md** | 原始需求文档 |

**用途场景：**
- 📖 学习项目规则和约束
- 🔍 查找问题解决方案
- 📝 理解技术实现细节
- 🚀 快速上手操作指南

---

## 🔧 scripts/ - 脚本目录

**作用：** 存放所有可执行脚本（PowerShell + Python）

### PowerShell 主脚本

| 文件 | 作用 | 使用场景 |
|------|------|---------|
| **Generate-IFWI-Report-From-Artifactory.ps1** | 主工作流 | ⭐⭐⭐ 从Artifactory生成报告（推荐） |
| **Generate-IFWI-Report.ps1** | FIV工作流 | 从FIV Orange页面生成报告 |
| **Generate-Multi-IFWI-Report.ps1** | 多Orange合并 | 生成包含多个Orange的周报 |
| **Install-Dependencies.ps1** | 安装依赖 | 首次使用时运行 |
| **Cleanup-TempFiles.ps1** | 清理临时文件 | 清理.7z等大文件 |

### PowerShell 辅助脚本

| 文件 | 作用 |
|------|------|
| **Get-BIOSVersionInfo.ps1** | 获取BIOS版本信息 |
| **Get-FIVOSXMLTable.ps1** | 从FIV提取OSXML表 |
| **Get-FIVOSXMLTable-Auto.ps1** | 自动提取FIV OSXML |
| **generate_both_reports.ps1** | 生成两种报告 |
| **run_test_ap1_a0.ps1** | AP1 A0测试 |
| **run_test_ap2_a0.ps1** | AP2 A0测试 |

### Python 核心脚本

| 文件 | 作用 | 调用者 |
|------|------|--------|
| **search_artifactory_by_orange_id.py** | 搜索Artifactory | 主工作流步骤1 |
| **construct_artifactory_url.py** | 构建下载URL | 主工作流步骤2 |
| **extract_artifactory_osxml.py** | 提取OSXML数据 | 主工作流步骤3 |
| **generate_ifwi_report.py** | 生成单个HTML报告 | 主工作流步骤4 |
| **generate_multi_ifwi_report.py** | 生成多Orange周报 | 多Orange场景 |

### Python 辅助脚本

| 文件 | 作用 |
|------|------|
| **extract_fiv_table.py** | 从FIV提取表格（Selenium） |
| **extract_up_imh_osxml.py** | 提取UP IMH OSXML（Rule 0.7） |
| **test_artifactory.py** | Artifactory连接测试 |

**工作流程：**
```
1. search_artifactory_by_orange_id.py   → 查找BIOS ID
2. construct_artifactory_url.py         → 构建下载URL  
3. extract_artifactory_osxml.py         → 下载并解析数据
   ├── extract_up_imh_osxml.py          → 提取UP IMH OSXML
   └── [下载Simics release notes]
4. generate_ifwi_report.py              → 生成HTML报告
```

---

## 📄 output/ - 输出目录

**作用：** 存放所有生成的报告文件

### 文件类型

| 文件类型 | 命名格式 | 作用 |
|---------|---------|------|
| **HTML报告** | `IFWI_Release_Status_{Orange_ID}.html` | 最终HTML报告 |
| **CSV数据** | `OSXML_Summary_{Orange_ID}.csv` | 提取的原始数据 |
| **周报** | `DMR_Weekly_Status_Report_{Date}.html` | 多Orange合并周报 |

### 当前文件

```
output/
├── IFWI_Release_Status_2026.15.3.01.html  # AP1 A0 Post-Si 报告
├── IFWI_Release_Status_2026.21.2.01.html  # Pre-Si 报告
├── IFWI_Release_Status_2026.24.5.01.html  # Pre-Si 报告
├── IFWI_Release_Status_2026.26.4.01.html  # ⭐ 最新：AP1 B0 Pre-Si
├── OSXML_Summary_2026.15.3.01.csv
├── OSXML_Summary_2026.21.2.01.csv
├── OSXML_Summary_2026.24.5.01.csv
└── OSXML_Summary_2026.26.4.01.csv
```

**用途场景：**
- 📧 发送周报给团队
- 🔍 查看历史报告
- 📊 对比不同版本
- 💾 归档和备份

---

## 🧪 test/ - 测试目录

**作用：** 存放测试文件、测试数据、临时文件

### 文件类型

| 文件 | 作用 |
|------|------|
| **test_detect_platform.py** | 平台检测测试脚本 |
| **test_artifactory.py** | Artifactory连接测试 |
| **test_*.txt** | 测试输入数据 |
| **AP1_B0_Version_Summary.txt** | 版本摘要 |
| **temp_input.txt** | 临时输入文件 |

**用途场景：**
- 🧪 开发时测试功能
- 📝 临时存放输入数据
- 🔧 调试脚本

---

## ⚙️ 系统目录

### .claude/
**作用：** Claude Code配置和记忆系统
- 项目特定配置
- 用户偏好记忆
- 会话历史

### __pycache__/
**作用：** Python字节码缓存
- 自动生成
- 加速脚本加载
- 可以删除（会自动重建）

---

## 📊 目录使用频率

```
⭐⭐⭐ 高频使用：
  - scripts/            # 每次生成报告都要用
  - output/             # 查看和分享报告
  - docs/CLAUDE.md      # 查阅规则

⭐⭐ 中频使用：
  - docs/               # 遇到问题时查阅
  - README.md           # 新人入门

⭐ 低频使用：
  - test/               # 开发测试
  - requirements.txt    # 首次安装
```

---

## 🎯 快速导航

### 我想...

| 场景 | 去哪里 |
|------|--------|
| **生成报告** | 运行 `scripts/Generate-IFWI-Report-From-Artifactory.ps1` |
| **查看报告** | 打开 `output/*.html` |
| **学习规则** | 阅读 `docs/CLAUDE.md` |
| **安装环境** | 运行 `scripts/Install-Dependencies.ps1` |
| **获取API Token** | 查看 `docs/HOW_TO_GET_API_TOKEN.md` |
| **清理临时文件** | 运行 `scripts/Cleanup-TempFiles.ps1` |
| **解决问题** | 查看 `docs/INSTALL_TROUBLESHOOTING.md` |
| **了解工作流** | 阅读 `docs/QUICK_START_ARTIFACTORY.md` |

---

**提示：** 
- 🚀 新用户先看 `README.md` 和 `docs/START_HERE.md`
- 📖 开发者必读 `docs/CLAUDE.md`（包含所有规则）
- 🔧 日常使用只需要 `scripts/` 和 `output/` 目录
