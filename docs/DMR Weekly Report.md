# DMR Weekly Report - 使用说明

## 项目概述

DMR Weekly Report 是一个自动化工具，用于从 生成周报数据。该工具通过浏览器自动化技术访问 FIV Portal，提取 OSXML 组件版本、PnP/PM 数据等关键信息，并生成标准化的报告。

## 功能特性

- 🤖 **自动化数据提取** - 无需手动复制粘贴，自动从 FIV Portal 提取数据
- 📊 **多表格识别** - 智能识别并提取页面中的所有数据表格
- 🔍 **关键信息解析** - 自动提取 Orange ID、BIOS ID、Unified Patch 等元数据
- 📁 **多格式输出** - 生成 HTML、CSV 等多种格式的数据文件
- 📋 **标准化报告** - 生成统一格式的 OSXML 汇总报告

## 环境要求

### 必需软件

- **Python 3.8+** - Python 运行环境
- **Google Chrome** - Chrome 浏览器（用于 Selenium 自动化）
- **PowerShell 5.1+** - Windows PowerShell（Windows 10/11 自带）

### Python 依赖包

以下包会在首次运行时自动安装：
- `selenium` - 浏览器自动化框架
- `webdriver-manager` - ChromeDriver 自动管理

## 安装步骤

### 1. 验证 Python 安装

打开 PowerShell 或命令提示符，运行：

```powershell
python --version
```

应显示类似 `Python 3.x.x` 的版本信息。如果未安装，请从 [python.org](https://www.python.org/downloads/) 下载安装。

### 2. 验证 Chrome 浏览器

确保系统已安装 Google Chrome 浏览器。工具会自动下载匹配的 ChromeDriver。

### 3. 准备工作目录

将以下文件放在同一目录下：
```
C:\Work\DMR\Weekly Report\
├── Get-FIVOSXMLTable-Auto.ps1
└── extract_fiv_table.py
```

## 使用方法

### 快速开始 ⚡

只需提供 FIV Portal 的 Orange Report 链接即可：

```powershell
.\Get-FIVOSXMLTable-Auto.ps1 -FIVUrl "你的Orange Report完整链接"
```

**示例：**
```powershell
.\Get-FIVOSXMLTable-Auto.ps1 -FIVUrl "https://fiv-ifwi.intel.com/test_report/report_wrap/26401/232/Orange/2026.25.3.01/"
```

**就这么简单！** 脚本会自动：
- 安装所需的 Python 依赖包
- 访问并解析页面
- 提取所有数据
- 生成报告文件到当前目录

### 详细步骤

1. **打开 PowerShell**

2. **切换到工作目录**：
   ```powershell
   cd "C:\Work\DMR\Weekly Report"
   ```

3. **复制 FIV Portal 的 Orange Report 链接**
   - 从浏览器地址栏复制完整 URL
   - 例如：`https://fiv-portal.intel.com/Orange/2026.25.3.01/`

4. **执行脚本**：
   ```powershell
   .\Get-FIVOSXMLTable-Auto.ps1 -FIVUrl "粘贴你的链接"
   ```

5. **等待完成**
   - 首次运行会自动安装依赖（约30秒）
   - 数据提取通常需要10-30秒
   - 完成后所有文件保存在当前目录

### 可选：自定义输出路径

如需指定其他输出位置：
```powershell
.\Get-FIVOSXMLTable-Auto.ps1 -FIVUrl "你的链接" -OutputPath "D:\Reports"
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| `FIVUrl` | String | 是 | FIV Portal 的完整 URL | `https://fiv-portal.../Orange/2026.25.3.01/` |
| `OutputPath` | String | 否 | 输出文件保存路径 | 默认: `C:\Work\DMR\Weekly Report` |

## 输出文件说明

工具执行后会在输出目录生成以下文件：

### 1. 原始表格文件

每个检测到的表格会生成一组文件：

- **FIV_Table_N.html** - 表格的 HTML 源代码
- **FIV_Table_N.csv** - 表格数据的 CSV 格式

其中 N 为表格序号（1, 2, 3...）

### 2. 标准化汇总报告

- **OSXML_Summary_{Orange_ID}.csv** - 核心数据汇总文件

示例文件名：`OSXML_Summary_2026.25.3.01.csv`

#### 汇总报告内容结构

```csv
Orange_ID,2026.25.3.01
BIOSID,0035.D12

Component,OSXML_BIOS,OSXML_Simics,Unified_Patch
IMH_OSXML,1.2.3.4,1.2.3.5,5200020E
CBB_OSXML,2.0.1.0,N/A,N/A
SCF_IPSD,3.1.0.0,N/A,N/A

Domain,PnP_Version,PM_Version
Domain1,v1.0,v2.0
Domain2,v1.5,v2.5
```

## 提取的数据项

### 元数据信息

- **Orange ID** - 版本标识符（如 2026.25.3.01）
- **BIOS ID** - BIOS 版本号（如 0035.D12）
- **Unified Patch** - 统一补丁版本（8位十六进制，如 5200020E）

### OSXML 组件版本

- **IMH OSXML** - BIOS 和 Simics 版本
- **CBB OSXML** - CBB 组件版本
- **SCF IPSD** - SCF IPSD 版本

### PnP/PM 数据

各 Domain 的：
- PnP Version（Plug and Play 版本）
- PM Version（Power Management 版本）

## 执行流程

```
1. 启动脚本
   ↓
2. 自动安装 Python 依赖包
   ↓
3. 启动无头 Chrome 浏览器
   ↓
4. 访问 FIV Portal URL
   ↓
5. 等待页面加载完成
   ↓
6. 识别并提取所有表格
   ↓
7. 解析 OSXML 和 PnP/PM 数据
   ↓
8. 提取元数据（Orange ID、BIOS ID等）
   ↓
9. 生成 HTML 和 CSV 文件
   ↓
10. 生成标准化汇总报告
    ↓
11. 完成并关闭浏览器
```

## 故障排除

### 问题 1：Python 未找到

**错误信息：**
```
Error: Python not found. Please install Python 3.8+
```

**解决方法：**
- 从 [python.org](https://www.python.org/downloads/) 下载并安装 Python
- 安装时勾选 "Add Python to PATH"
- 重启 PowerShell 后重试

### 问题 2：ChromeDriver 下载失败

**错误信息：**
```
Could not download ChromeDriver...
```

**解决方法：**
- 检查网络连接
- 确保 Chrome 浏览器已安装并是较新版本
- 如在企业网络环境，可能需要配置代理

### 问题 3：页面加载超时

**错误信息：**
```
Timeout waiting for table to load
```

**解决方法：**
- 检查 FIV Portal URL 是否正确
- 确保有权限访问该页面
- 检查网络连接速度
- 可以在 `extract_fiv_table.py` 中增加超时时间（第32行）

### 问题 4：表格未识别

**现象：**
输出显示 "OSXML Table: Not found"

**解决方法：**
- 检查 FIV Portal 页面结构是否有变化
- 确认页面确实包含 OSXML 表格
- 查看生成的 `FIV_Table_N.csv` 文件，手动确认表格内容

### 问题 5：执行策略限制

**错误信息：**
```
无法加载文件，因为在此系统上禁止运行脚本
```

**解决方法：**
以管理员身份运行 PowerShell，执行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 使用示例

### 示例 1：标准使用（最常用）

**步骤：**
1. 在浏览器打开 Orange Report 页面
2. 复制完整 URL
3. 执行：

```powershell
.\Get-FIVOSXMLTable-Auto.ps1 -FIVUrl "https://fiv-portal.intel.com/Orange/2026.25.3.01/"
```

**自动生成的文件：**
- ✅ `OSXML_Summary_2026.25.3.01.csv` - **核心汇总报告**（这是你需要的）
- `FIV_Table_1.html` / `FIV_Table_1.csv` - 原始表格1
- `FIV_Table_2.html` / `FIV_Table_2.csv` - 原始表格2
- ... 以及其他所有检测到的表格

### 示例 2：指定输出路径

```powershell
.\Get-FIVOSXMLTable-Auto.ps1 `
    -FIVUrl "https://fiv-portal.intel.com/Orange/2026.24.6.01/" `
    -OutputPath "D:\Weekly_Reports\2026W26"
```

### 示例 3：批量处理多个版本

创建批处理脚本 `batch_extract.ps1`：

```powershell
$versions = @(
    "2026.25.3.01",
    "2026.24.6.01",
    "2026.23.4.01"
)

foreach ($ver in $versions) {
    $url = "https://fiv-portal.intel.com/Orange/$ver/"
    Write-Host "Processing $ver..." -ForegroundColor Cyan
    .\Get-FIVOSXMLTable-Auto.ps1 -FIVUrl $url
    Write-Host "Completed $ver`n" -ForegroundColor Green
}
```

## 最佳实践

1. **定期更新** - 保持 Chrome 浏览器和 Python 包为最新版本
2. **验证 URL** - 执行前先在浏览器中验证 FIV Portal URL 可访问
3. **备份数据** - 定期备份生成的报告文件
4. **检查输出** - 执行后检查控制台输出，确认数据提取完整
5. **版本管理** - 为不同周的报告创建独立的输出目录

## 脚本维护

### 更新依赖包

```powershell
pip install --upgrade selenium webdriver-manager
```

### 查看当前依赖版本

```powershell
pip list | Select-String "selenium|webdriver"
```

## 技术支持

如遇到问题，请检查：

1. **控制台输出** - 查看详细的错误信息
2. **生成的 CSV 文件** - 验证数据是否正确提取
3. **Chrome 版本兼容性** - 确保 Chrome 浏览器版本与 ChromeDriver 兼容

## 附录

### A. 支持的表格格式

工具支持两种 OSXML 表格格式：

**格式 A：** 行标签包含组件名和类型
```
IMH OSXML | 1.2.3.4 | 1.2.3.5
CBB OSXML | 2.0.1.0 | N/A
```

**格式 B：** 独立的表头行
```
SoC | OSXML in BIOS | OSXML in Simics
IMH | 1.2.3.4 | 1.2.3.5
CBB | 2.0.1.0 | N/A
```

### B. Orange ID 格式说明

Orange ID 格式：`YYYY.WW.X.YY`
- `YYYY` - 年份（如 2026）
- `WW` - 工作周（如 25）
- `X` - 主版本号
- `YY` - 次版本号

示例：`2026.25.3.01` = 2026年第25周，版本 3.01

---

**文档版本：** 1.0  
**最后更新：** 2026-06-29  
**适用工具版本：** extract_fiv_table.py v1.0
