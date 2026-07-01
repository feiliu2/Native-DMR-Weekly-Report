# Quick Reference - DMR IFWI Report Generator

**快速生成 IFWI Release Status Report**

---

## 🚀 最快方式（推荐）

### 只需 3 个信息：

```
1. Platform:  AP1 A0 / AP1 B0 / AP2 A0
2. Version:   2026.26.4.01.0036.D.54
3. Release:   released on WW26.5
```

### 运行命令：

```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

**系统自动：**
- ✅ 构建 Artifactory URL
- ✅ 下载构建包
- ✅ 提取 OSXML 数据
- ✅ 生成 HTML 报告
- ✅ 在浏览器打开

---

## 📝 版本格式

**格式:** `IFWI_ID.BIOS_ID`

| 示例 | IFWI ID | BIOS ID |
|------|---------|---------|
| `2026.26.4.01.0036.D.54` | 2026.26.4.01 | 0036.D.54 |
| `2026.25.3.01.0036.D.29` | 2026.25.3.01 | 0036.D.29 |

---

## 🔑 API Token

**首次使用需要获取 API Token：**

1. 访问 [Artifactory](https://af01p-or.devtools.intel.com)
2. 点击用户图标 → "Edit Profile"
3. 输入当前密码
4. 复制 "API Key"

**Token 会被安全保存，之后无需重复输入。**

---

## 📋 平台说明

### AP1 A0 (Post-Silicon)
- **报告类型:** 简化版（BIOS + Unified Patch）
- **Simics:** 不需要
- **OSXML 表格:** 无
- **uBIOS:** 无

### AP1 B0 (Pre-Silicon)
- **报告类型:** 完整版（BIOS + UP + OSXML + PnP/PM + uBIOS）
- **Simics:** 需要提供（例如：`dmr-7 2026ww24.3.00_45 Pre712`）
- **OSXML 表格:** 完整 3 列
- **Unified Patch:** 51xxxxxx（第2位数字=1）

### AP2 A0 (Pre-Silicon)
- **报告类型:** 完整版（BIOS + UP + OSXML + PnP/PM + uBIOS）
- **Simics:** 需要提供（例如：`dmr-rio-7 2026ww25.3.00_03 Pre550`）
- **OSXML 表格:** 完整 3 列
- **Unified Patch:** 52xxxxxx（第2位数字=2）

---

## 💡 完整示例

### 示例 1: AP1 A0 Post-Si

```
Platform: AP1 A0
Version: 2026.26.4.01.0036.D.54
Release: released on WW26.5

输出：
DMR-AP-UCC AP1 A0 Post-Si Orange IFWI 2026.26.4.01 has been released on WW26.5

[简化报告：BIOS Binary + Unified Patch]
```

### 示例 2: AP1 B0 Pre-Si

```
Platform: AP1 B0
Version: 2026.25.3.01.0036.D.29
Release: released on WW25.5
Simics: dmr-7 2026ww24.3.00_45 Pre712

输出：
DMR-AP-UCC AP1 B0 Pre-Si Orange IFWI 2026.25.3.01 has been released on WW25.5

[完整报告：BIOS + Simics + Unified Patch + OSXML + PnP/PM]

AP1 B0 uBIOS based on BIOSID 0036.D29 will be released on WW25.6
```

### 示例 3: AP2 A0 Pre-Si

```
Platform: AP2 A0
Version: 2026.26.4.02.0036.D.54
Release: released on WW26.5
Simics: dmr-rio-7 2026ww25.3.00_03 Pre550

输出：
DMR-AP-MCC AP2 A0 Pre-Si Orange IFWI 2026.26.4.02 has been released on WW26.5

[完整报告：BIOS + Simics + Unified Patch + OSXML + PnP/PM]

AP2 A0 uBIOS based on BIOSID 0036.D54 will be released on WW26.6
```

---

## 🛠️ 常见问题

### Q: 找不到构建包？

**错误信息:**
```
[ERROR] Directory not found (HTTP 404)
```

**检查:**
- 版本号是否正确？
- IFWI ID: `YYYY.WW.X.NN` 格式
- BIOS ID: `BBBB.D.VV` 格式

---

### Q: Unified Patch 提取失败？

**检查平台和 UP 版本匹配:**
- AP1 B0 → 51xxxxxx（第2位是1）
- AP2 A0 → 52xxxxxx（第2位是2）

---

### Q: Simics 版本格式？

**完整格式:**
```
dmr-7 2026ww24.3.00_45 Pre712
^^^^^  ^^^^^^^^^^^^^^^^ ^^^^^^
路径    版本号            Pre编号
```

**简化格式（系统自动补全路径）:**
```
2026ww24.3.00_45
```

**平台路径:**
- AP1 B0 → `dmr-7`
- AP2 A0 → `dmr-rio-7`

---

## 📊 输出文件

**生成的文件:**
```
IFWI_Release_Status_YYYY.WW.X.NN.html
```

**包含内容:**
- ✅ Release statement
- ✅ BIOS Binary version
- ✅ Unified Patch version
- ✅ OSXML versions (Pre-Si only)
  - BIOS OSXML
  - Simics OSXML
  - **Unified Patch OSXML** ⭐ (新功能)
- ✅ SCF IPSD version
- ✅ PnP/PM Recipe config (Pre-Si only)
- ✅ uBIOS release statement (Pre-Si only)

---

## 🔗 相关文档

| 文档 | 说明 |
|------|------|
| [SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md) | 详细工作流说明 |
| [CRITICAL_RULES.md](CRITICAL_RULES.md) | 关键规则（开发者必读） |
| [CLAUDE.md](CLAUDE.md) | 完整项目规则 |
| [HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md) | API Token 获取指南 |

---

## ✨ 新功能

### 🎉 简化输入（2026-06-30）
- 不再需要手动复制 Artifactory URL
- 只需提供：平台 + 版本号
- 系统自动构建 URL

### ⭐ Unified Patch OSXML（2026-06-30）
- 自动提取 UP 包中的 IMH OSXML
- 显示在 OSXML 表格的 Unified Patch 列
- AP1 B0 和 AP2 A0 支持

### 🔧 版本模式匹配（2026-06-30）
- 通过 UP 版本号第2位数字识别平台
- 51xxxxxx = AP1 B0
- 52xxxxxx = AP2 A0
- 不再依赖 binary 文件中的位置

---

## 📞 获取帮助

**遇到问题？**

1. 查看 [SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md) 故障排除章节
2. 检查 [CRITICAL_RULES.md](CRITICAL_RULES.md) 确保遵循关键规则
3. 验证 API Token 是否有效

---

**版本:** 1.0  
**更新日期:** 2026-06-30  
**支持平台:** AP1 A0, AP1 B0, AP2 A0
