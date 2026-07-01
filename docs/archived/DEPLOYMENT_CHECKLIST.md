# Deployment Checklist - 部署检查清单

**给其他人使用前的准备**

---

## 📦 打包前检查（发送方）

### 需要包含的文件

```
✅ Python 脚本
   - extract_artifactory_osxml.py
   - extract_up_imh_osxml.py
   - construct_artifactory_url.py
   - generate_ifwi_report.py
   - generate_multi_ifwi_report.py
   - extract_fiv_table.py

✅ PowerShell 脚本
   - Generate-IFWI-Report-From-Artifactory.ps1
   - Generate-IFWI-Report.ps1

✅ 依赖文件
   - requirements.txt

✅ 文档（重要！）
   - README.md
   - QUICK_REFERENCE.md
   - SIMPLIFIED_WORKFLOW.md
   - HOW_TO_GET_API_TOKEN.md
   - CRITICAL_RULES.md
   - CLAUDE.md
   - 其他所有 .md 文件
```

### 可以删除的文件（临时文件）

```
❌ *.csv (临时数据文件)
❌ *.html (已生成的报告)
❌ *.7z (下载的构建包)
❌ OSXML_Version.html (临时文件)
❌ *_release_notes.csv (临时文件)
❌ __pycache__/ (Python缓存)
```

### 打包命令示例

**选项 1: 压缩为 .zip**
```powershell
# 在 PowerShell 中
Compress-Archive -Path "Native DMR Weekly Report" -DestinationPath "DMR_IFWI_Report_Tool.zip"
```

**选项 2: 手动选择**
```
1. 复制整个文件夹到新位置
2. 删除上述"可以删除的文件"
3. 压缩文件夹
```

---

## 🚀 接收方设置步骤（新用户）

### Step 1: 解压文件
```powershell
# 解压到任意位置
Expand-Archive -Path "DMR_IFWI_Report_Tool.zip" -DestinationPath "C:\Tools\DMR_Report"
cd "C:\Tools\DMR_Report"
```

### Step 2: 检查 Python 环境
```powershell
# 检查 Python 版本（需要 3.8+）
python --version

# 应该显示：Python 3.8.x 或更高
```

如果没有 Python：
- 下载安装：https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

### Step 3: 安装依赖
```powershell
# 安装所有必需的 Python 包
pip install -r requirements.txt

# 等待安装完成（约 1-2 分钟）
```

### Step 4: 获取 API Token
```
1. 访问 https://af01p-or.devtools.intel.com
2. 点击用户图标 → "Edit Profile"
3. 输入当前密码
4. 复制 "API Key"
```

详细说明：参考 `HOW_TO_GET_API_TOKEN.md`

### Step 5: 测试运行
```powershell
# 运行主脚本
.\Generate-IFWI-Report-From-Artifactory.ps1

# 按提示操作：
# - 选择 "Simple mode"
# - 选择平台
# - 输入版本
# - 粘贴 API Token
```

---

## ✅ 验证清单

**安装成功的标志：**

```
✅ Python 版本 >= 3.8
✅ pip install 无错误
✅ 脚本可以启动（不报错）
✅ 能够构建 Artifactory URL
✅ 能够下载构建包
✅ 能够生成 HTML 报告
```

**测试命令：**
```powershell
# 1. 检查 Python
python --version

# 2. 检查依赖
pip list | findstr "requests beautifulsoup4 py7zr"

# 3. 测试脚本（应该显示帮助信息）
python construct_artifactory_url.py
```

---

## 🔧 常见问题

### Q1: "pip 不是内部或外部命令"

**解决：**
```powershell
# 使用 python -m pip
python -m pip install -r requirements.txt
```

### Q2: "无法加载脚本，因为在此系统上禁用了脚本执行"

**解决：**
```powershell
# 在 PowerShell 中执行（管理员权限）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q3: "ModuleNotFoundError: No module named 'xxx'"

**解决：**
```powershell
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### Q4: "HTTP 403 Authentication failed"

**解决：**
- API Token 已过期或无效
- 重新获取新的 API Token
- 参考 `HOW_TO_GET_API_TOKEN.md`

### Q5: "HTTP 404 Directory not found"

**解决：**
- 检查版本号是否正确
- 格式：`YYYY.WW.X.NN.BBBB.D.VV`
- 例如：`2026.26.4.01.0036.D.54`

---

## 📚 快速入门指南

**新用户推荐阅读顺序：**

1. 📖 **[README.md](README.md)** - 项目概述
2. 📖 **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - 快速参考（推荐）
3. 📖 **[SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md)** - 详细工作流
4. 📖 **[HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md)** - API Token 获取

**开发者阅读：**
- 📖 **[CRITICAL_RULES.md](CRITICAL_RULES.md)** - 关键规则
- 📖 **[CLAUDE.md](CLAUDE.md)** - 完整项目规则

---

## 🎯 快速测试（5分钟）

**完整测试流程：**

```powershell
# 1. 进入目录
cd "C:\Tools\DMR_Report"

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行脚本
.\Generate-IFWI-Report-From-Artifactory.ps1

# 4. 按提示操作
# 输入示例：
#   Platform: AP1 A0
#   Version: 2026.26.4.01.0036.D.54
#   Release: released on WW26.5
#   API Token: [粘贴您的token]

# 5. 等待生成
# 预期：浏览器自动打开 HTML 报告
```

**成功标志：**
```
✅ 看到 "Constructing Artifactory URL..."
✅ 看到 "Downloading from Artifactory..."
✅ 看到 "Generating HTML report..."
✅ 浏览器自动打开显示报告
```

---

## 📞 获取帮助

**遇到问题？**

1. 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) 常见问题章节
2. 查看 [SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md) 故障排除
3. 检查 Python 版本和依赖安装
4. 验证 API Token 是否有效

---

## 📋 系统要求

**最低要求：**
- ✅ Windows 10/11
- ✅ Python 3.8 或更高
- ✅ PowerShell 5.1 或更高
- ✅ 网络连接（访问 Artifactory）
- ✅ 有效的 Artifactory API Token

**推荐配置：**
- ✅ Python 3.10+
- ✅ PowerShell 7+
- ✅ 10 GB 可用磁盘空间（用于临时文件）

---

## ✨ 版本信息

**工具版本：** 1.0  
**更新日期：** 2026-06-30  
**支持平台：** AP1 A0, AP1 B0, AP2 A0

---

**部署检查完成！** ✅
