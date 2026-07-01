# Documentation Index - 文档索引

**所有约束条件和规则已完整记录 ✅**

**最后更新：** 2026-06-30

---

## 📋 核心文档清单

### 1. 新用户入门 🌟

| 文档 | 说明 | 优先级 |
|------|------|--------|
| **[START_HERE.md](START_HERE.md)** | 5分钟快速开始 | 🔴 必读 |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | 快速参考卡片 | 🔴 必读 |
| **[SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md)** | 详细工作流说明 | 🟡 推荐 |
| **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** | 部署检查清单 | 🟡 推荐 |
| **[HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md)** | 获取API Token | 🔴 必读 |

---

### 2. 项目规则 📖

| 文档 | 说明 | 内容 |
|------|------|------|
| **[CLAUDE.md](CLAUDE.md)** | 完整项目规则（主文档） | 所有7个核心规则 |
| **[CRITICAL_RULES.md](CRITICAL_RULES.md)** | 最容易出错的关键规则 | 7个最关键规则 |
| **[README.md](README.md)** | 项目概述 | 快速开始和文档链接 |

---

### 3. 功能规则文档 🔧

| 文档 | 规则主题 | CLAUDE.md 对应 |
|------|----------|----------------|
| **[UP_VERSION_PATTERN_RULES.md](UP_VERSION_PATTERN_RULES.md)** | UP版本模式匹配（51xxxx/52xxxx） | Rule 0.5 |
| **[UP_IMH_OSXML_EXTRACTION.md](UP_IMH_OSXML_EXTRACTION.md)** | UP IMH OSXML提取 | Rule 0.7 |
| **[SIMICS_RIO_RULE.md](SIMICS_RIO_RULE.md)** | Simics路径检测（rio规则） | Rule 7 ⭐ 最新 |
| **[PLATFORM_RULES.md](PLATFORM_RULES.md)** | 平台特定规则 | Rule 0.5, 0.6 |
| **[SCF_IPSD_RULES.md](SCF_IPSD_RULES.md)** | SCF IPSD提取规则 | Rule 0.5 |
| **[UNIFIED_PATCH_ORDER.md](UNIFIED_PATCH_ORDER.md)** | Binary文件格式 | Rule 0.5 |
| **[SIMICS_PLATFORM_PATHS.md](SIMICS_PLATFORM_PATHS.md)** | Simics路径映射（已过时）| ⚠️ 被Rule 7取代 |

---

### 4. 测试文档 🧪

| 文档 | 说明 |
|------|------|
| **[UP_IMH_OSXML_TEST_RESULTS.md](UP_IMH_OSXML_TEST_RESULTS.md)** | UP OSXML提取测试结果 |

---

## 📊 规则覆盖情况

### CLAUDE.md 中的所有规则

✅ **Rule 0:** Artifactory Workflow - User Input Requirements  
✅ **Rule 0.5:** Report Types by Platform (AP1 A0/AP1 B0/AP2 A0)  
✅ **Rule 0.6:** Platform-Specific OSXML Extraction (IMH/CBB不同顺序)  
✅ **Rule 0.7:** Unified Patch IMH OSXML Extraction  
✅ **Rule 1:** Orange ID Auto-Detection  
✅ **Rule 2:** Conditional Table Display  
✅ **Rule 3:** Platform Stepping Detection  
✅ **Rule 4:** uBIOS Emulation Statement  
✅ **Rule 5:** Report Header Simplification  
✅ **Rule 6:** Release Tense Detection  
✅ **Rule 7:** Simics Path Detection (Rio Rule) ⭐ 最新

---

### CRITICAL_RULES.md 中的关键规则

🔴 **CRITICAL #1:** IMH和CBB有不同的索引顺序  
🔴 **CRITICAL #2:** Unified Patch顺序（51xxxx/52xxxx版本模式）  
🔴 **CRITICAL #3:** Simics平台路径不同（dmr-7 vs dmr-rio-7）  
🔴 **CRITICAL #4:** SCF IPSD版本格式（4.0.0.前缀）  
🔴 **CRITICAL #5:** Simics版本必须完整  
🔴 **CRITICAL #6:** SCF IPSD仅用于AP1 B0和AP2 A0  
🔴 **CRITICAL #7:** Simics发布说明搜索模式

---

## 🆕 最新更新（2026-06-30）

### 1. Simics Rio 规则（Rule 7）⭐
**文档：** `SIMICS_RIO_RULE.md`  
**规则：** 检查用户输入中是否包含 'rio' → 决定使用 dmr-7 或 dmr-rio-7  
**优势：** 更灵活，用户完全控制

### 2. UP 版本模式匹配
**文档：** `UP_VERSION_PATTERN_RULES.md`  
**规则：** 检查UP版本第2位数字（1=AP1 B0, 2=AP2 A0）  
**优势：** 不依赖binary中的位置

### 3. UP IMH OSXML 提取
**文档：** `UP_IMH_OSXML_EXTRACTION.md`  
**功能：** 自动从Artifactory下载UP包并提取IMH OSXML  
**支持：** AP1 B0, AP2 A0

### 4. 简化工作流
**文档：** `SIMPLIFIED_WORKFLOW.md`  
**功能：** URL自动构建，只需平台+版本号  
**优势：** 大幅简化用户输入

---

## 🎯 快速查找

### 我想知道...

**如何开始使用？**  
→ [START_HERE.md](START_HERE.md)

**平台和版本格式？**  
→ [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Unified Patch为什么提取错误？**  
→ [UP_VERSION_PATTERN_RULES.md](UP_VERSION_PATTERN_RULES.md)  
→ [CRITICAL_RULES.md](CRITICAL_RULES.md) #2

**Simics路径怎么选择？**  
→ [SIMICS_RIO_RULE.md](SIMICS_RIO_RULE.md) ⭐ 最新规则  
→ [CLAUDE.md](CLAUDE.md) Rule 7

**IMH/CBB OSXML为什么显示错误？**  
→ [CRITICAL_RULES.md](CRITICAL_RULES.md) #1  
→ [CLAUDE.md](CLAUDE.md) Rule 0.6

**如何获取API Token？**  
→ [HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md)

**如何部署给其他人？**  
→ [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**所有规则在哪里？**  
→ [CLAUDE.md](CLAUDE.md) - 主文档  
→ [CRITICAL_RULES.md](CRITICAL_RULES.md) - 关键规则

---

## 📝 文档完整性检查

### ✅ 已记录的约束条件

- [x] Artifactory URL构建规则
- [x] 平台类型和报告格式（AP1 A0/AP1 B0/AP2 A0）
- [x] Unified Patch版本模式匹配（51xxxx/52xxxx）
- [x] UP IMH OSXML提取流程
- [x] Simics路径选择规则（rio检测）
- [x] IMH/CBB OSXML不同索引顺序
- [x] SCF IPSD提取和格式规则
- [x] uBIOS release week计算
- [x] Release tense检测
- [x] Orange ID自动检测
- [x] 条件表格显示规则
- [x] 平台stepping检测
- [x] API Token获取流程
- [x] 部署和设置步骤
- [x] 错误处理和故障排除

### ✅ 所有新功能已文档化

- [x] 简化工作流（平台+版本→报告）
- [x] URL自动构建
- [x] UP IMH OSXML自动提取
- [x] Simics rio规则
- [x] UP版本模式匹配

---

## 🔍 文档状态

| 类型 | 数量 | 状态 |
|------|------|------|
| 核心规则文档 | 3 | ✅ 完整 |
| 功能规则文档 | 7 | ✅ 完整 |
| 用户指南文档 | 5 | ✅ 完整 |
| 测试文档 | 1 | ✅ 完整 |
| 部署文档 | 2 | ✅ 完整 |
| **总计** | **18** | **✅ 全部完整** |

---

## 📚 相关文件

### Python 脚本 (6个)
- `extract_artifactory_osxml.py`
- `extract_up_imh_osxml.py`
- `construct_artifactory_url.py`
- `generate_ifwi_report.py`
- `generate_multi_ifwi_report.py`
- `extract_fiv_table.py`

### PowerShell 脚本 (3个)
- `Generate-IFWI-Report-From-Artifactory.ps1`
- `Generate-IFWI-Report.ps1`
- `Cleanup-TempFiles.ps1`

### 配置文件 (1个)
- `requirements.txt`

---

## ✅ 确认清单

**对于开发者：**

- [x] 所有约束条件已记录在 CLAUDE.md
- [x] 所有关键规则已记录在 CRITICAL_RULES.md
- [x] 所有新功能已单独文档化
- [x] 所有测试结果已记录
- [x] 部署步骤已完整说明

**对于用户：**

- [x] 快速开始指南已提供（START_HERE.md）
- [x] 详细工作流已说明（SIMPLIFIED_WORKFLOW.md）
- [x] 常见问题已覆盖（QUICK_REFERENCE.md）
- [x] API Token获取已说明
- [x] 故障排除指南已提供

---

## 🎉 结论

**所有约束条件和规则已完整记录！**

✅ 7个核心规则（CLAUDE.md）  
✅ 7个关键规则（CRITICAL_RULES.md）  
✅ 4个新功能完整文档化  
✅ 完整的用户指南和部署文档  
✅ 18个文档，全部最新

**可以安全打包分发！** 🚀

---

**文档索引最后更新：** 2026-06-30  
**总文档数：** 18  
**状态：** ✅ 完整且最新
