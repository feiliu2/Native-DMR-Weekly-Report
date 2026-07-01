# 🏢 Intel InnerSource Setup Guide

## 📍 目标仓库

根据你的项目类型，建议使用以下命名空间：

```
组织: intel-innersource
仓库命名建议:
  firmware.boot.uefi.iafw.dmr.weekly-report-generator
  或
  firmware.boot.uefi.iafw.validation.dmr-ifwi-report-tool
```

**参考示例:**
```
https://github.com/intel-innersource/firmware.boot.uefi.iafw.validation.fiv-tool.execution-copilot-ai
```

---

## 🚀 推送到Intel InnerSource

### 步骤1: 创建InnerSource仓库

1. **访问Intel InnerSource**
   - 打开: https://github.com/intel-innersource
   - 或者访问你的团队组织页面

2. **创建新仓库**
   - 点击 "New repository" 或联系团队管理员
   - **仓库名称建议:**
     ```
     firmware.boot.uefi.iafw.dmr.weekly-report-generator
     ```
   - **描述:**
     ```
     DMR Weekly IFWI Report Generator - Automated tool to generate HTML reports from Artifactory build packages for AP1/AP2 platforms
     ```
   - **可见性:** Internal（Intel内部可见）
   - **不要**勾选 "Initialize with README"（我们已经有了）

3. **记录仓库URL**
   ```
   https://github.com/intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator
   ```

---

### 步骤2: 配置SSH密钥（推荐）

**如果还没有配置SSH密钥：**

1. **生成SSH密钥**
   ```bash
   # 使用你的Intel邮箱
   ssh-keygen -t ed25519 -C "your.email@intel.com"
   
   # 按提示操作（可以直接按Enter使用默认路径）
   # 默认保存位置: ~/.ssh/id_ed25519
   ```

2. **添加SSH密钥到GitHub**
   ```bash
   # 复制公钥内容
   cat ~/.ssh/id_ed25519.pub
   ```
   
   - 访问: https://github.com/settings/keys
   - 点击 "New SSH key"
   - Title: "My Work Laptop" 或其他描述
   - Key: 粘贴公钥内容
   - 点击 "Add SSH key"

3. **测试SSH连接**
   ```bash
   ssh -T git@github.com
   # 应该显示: Hi username! You've successfully authenticated...
   ```

---

### 步骤3: 推送代码到InnerSource

#### 方式A: 使用SSH（推荐）

```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"

# 添加远程仓库（替换实际仓库名）
git remote add origin git@github.com:intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git

# 重命名分支为main
git branch -M main

# 推送到InnerSource
git push -u origin main

# 推送所有标签（如果有）
git push --tags
```

#### 方式B: 使用HTTPS（需要输入凭据）

```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"

# 添加远程仓库
git remote add origin https://github.com/intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git

# 重命名分支为main
git branch -M main

# 推送（会提示输入GitHub用户名和密码/Token）
git push -u origin main
```

---

### 步骤4: 验证推送

1. **访问仓库页面**
   ```
   https://github.com/intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator
   ```

2. **检查内容**
   - ✅ README.md 显示正常
   - ✅ docs/ 文件夹完整
   - ✅ scripts/ 文件夹完整
   - ✅ .gitignore 已生效（output/, test/等未被推送）

3. **查看提交历史**
   - 点击 "Commits" 查看提交记录
   - 应该看到2次提交

---

## 📋 推荐的仓库配置

### Repository Settings

在仓库设置页面（Settings）建议配置：

#### 1. **General**
- **Description:**
  ```
  Automated DMR Weekly IFWI Report Generator for AP1/AP2 platforms. 
  Generates HTML reports from Artifactory build packages with OSXML, 
  PnP/PM, and Simics data.
  ```
- **Topics:** 添加标签
  ```
  dmr, ifwi, bios, automation, reporting, artifactory, python, powershell
  ```

#### 2. **Branches**
- **Default branch:** main
- **Branch protection rules:**
  - Require pull request reviews before merging
  - Require status checks to pass

#### 3. **Collaborators**
- 添加团队成员
- 设置权限：Write / Maintain / Admin

---

## 📝 更新README徽章（可选）

在README.md顶部添加徽章：

```markdown
# DMR Weekly Report Generator

[![License](https://img.shields.io/badge/license-Intel%20Proprietary-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.14%2B-blue.svg)]()
[![PowerShell](https://img.shields.io/badge/powershell-7.0%2B-blue.svg)]()

> Automated tool to generate HTML reports from Artifactory build packages
```

---

## 🔒 安全最佳实践

### ✅ 已配置（.gitignore）
- ❌ API Tokens不会被提交
- ❌ 临时文件不会被提交
- ❌ Claude配置不会被提交
- ❌ 输出文件不会被提交

### ⚠️ 注意事项
1. **不要提交API Token** - 使用环境变量或配置文件
2. **不要提交密码** - 使用Git凭据管理器
3. **代码审查** - 提交前检查敏感信息

---

## 📊 项目结构（将在InnerSource显示）

```
firmware.boot.uefi.iafw.dmr.weekly-report-generator/
│
├── README.md                    # 项目主页
├── GIT_QUICK_START.md          # Git快速指南
├── requirements.txt             # Python依赖
├── .gitignore                   # Git忽略规则
│
├── docs/                        # 📚 完整文档（27个文件）
│   ├── CLAUDE.md               # 项目规则
│   ├── GIT_SETUP_GUIDE.md      # Git教程
│   └── ...
│
└── scripts/                     # 🔧 可执行脚本（18个文件）
    ├── Generate-IFWI-Report-From-Artifactory.ps1
    ├── search_artifactory_by_orange_id.py
    └── ...
```

---

## 🔄 日常工作流

### 开发新功能
```bash
# 1. 创建功能分支
git checkout -b feature/add-ap3-support

# 2. 开发和提交
git add .
git commit -m "feat: Add AP3 platform support"

# 3. 推送分支
git push -u origin feature/add-ap3-support

# 4. 在GitHub创建Pull Request

# 5. 代码审查后合并

# 6. 切换回main并拉取最新代码
git checkout main
git pull
```

### 修复Bug
```bash
git checkout -b fix/simics-path-detection
git add .
git commit -m "fix: Correct Simics Rio path detection

- Updated regex pattern in extract_artifactory_osxml.py
- Added test case for dmr-rio-7 path
- Closes #123"
git push -u origin fix/simics-path-detection
```

---

## 🎯 完整命令总结

### 首次推送到InnerSource

```bash
# 进入项目目录
cd "c:\Work\DMR\AI\Native DMR Weekly Report"

# 添加远程仓库（使用实际的仓库URL）
git remote add origin git@github.com:intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git

# 查看远程仓库配置
git remote -v

# 重命名分支为main（如果当前是master）
git branch -M main

# 推送到InnerSource
git push -u origin main

# 推送所有标签
git push --tags
```

### 验证推送成功

```bash
# 查看远程分支
git branch -r

# 查看提交日志
git log --oneline --graph --all
```

---

## 📞 获取帮助

### 如果遇到问题

1. **权限问题**
   - 联系仓库管理员添加你到协作者
   - 确认SSH密钥已正确配置

2. **推送失败**
   ```bash
   # 检查远程仓库配置
   git remote -v
   
   # 测试SSH连接
   ssh -T git@github.com
   
   # 强制推送（慎用！）
   git push -u origin main --force
   ```

3. **仓库命名咨询**
   - 联系团队Lead确认命名规范
   - 参考现有项目命名

---

## ✅ 检查清单

推送前确认：

- [ ] 已创建InnerSource仓库
- [ ] 已配置SSH密钥（或HTTPS凭据）
- [ ] 已检查.gitignore（无敏感文件）
- [ ] 已测试脚本功能正常
- [ ] README.md描述清晰
- [ ] 文档完整
- [ ] 提交信息清晰

推送后确认：

- [ ] 访问仓库页面正常
- [ ] README显示正确
- [ ] 文件结构完整
- [ ] 提交历史正确
- [ ] 添加协作者
- [ ] 设置分支保护规则

---

## 🎉 完成！

执行上面的命令后，你的项目将出现在：

```
https://github.com/intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator
```

团队成员可以通过以下方式克隆：

```bash
git clone git@github.com:intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git
```

---

**注意：** 仓库名称需要根据你的实际团队命名规范调整。联系你的团队Lead确认正确的命名空间。
