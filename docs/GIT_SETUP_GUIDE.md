# Git Setup Guide - DMR Weekly Report

## 📋 目录
1. [初始化Git仓库](#1-初始化git仓库)
2. [首次提交](#2-首次提交)
3. [连接到GitHub/GitLab](#3-连接到githubgitlab)
4. [日常使用](#4-日常使用)
5. [团队协作](#5-团队协作)

---

## 1. 初始化Git仓库

### 检查是否已安装Git
```bash
git --version
```

如果未安装，下载：https://git-scm.com/downloads

### 初始化仓库
```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"
git init
```

### 配置用户信息（首次使用）
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@intel.com"
```

---

## 2. 首次提交

### 查看当前状态
```bash
git status
```

### 添加所有文件到暂存区
```bash
# 添加所有文件（.gitignore会自动排除不需要的文件）
git add .

# 或者选择性添加
git add README.md
git add docs/
git add scripts/
git add requirements.txt
```

### 查看将要提交的文件
```bash
git status
```

### 提交到本地仓库
```bash
git commit -m "Initial commit: DMR Weekly Report Generator

- Added project documentation (docs/)
- Added PowerShell and Python scripts (scripts/)
- Added README.md and project structure
- Added .gitignore for Python and temporary files"
```

---

## 3. 连接到GitHub/GitLab

### 选项A: GitHub

#### 3.1 在GitHub上创建新仓库
1. 访问 https://github.com/
2. 点击 "New repository"
3. 仓库名称：`dmr-weekly-report` 或 `native-dmr-weekly-report`
4. 选择 Private（推荐，因为包含内部工具）
5. **不要**勾选 "Initialize with README"（我们已经有了）
6. 点击 "Create repository"

#### 3.2 连接到GitHub
```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/dmr-weekly-report.git

# 或使用SSH（如果已配置SSH密钥）
git remote add origin git@github.com:YOUR_USERNAME/dmr-weekly-report.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 选项B: Intel GitLab

#### 3.1 在Intel GitLab创建新项目
1. 访问 https://gitlab.devtools.intel.com/
2. 点击 "New project"
3. 项目名称：`dmr-weekly-report`
4. Visibility Level: Private
5. 点击 "Create project"

#### 3.2 连接到GitLab
```bash
# 添加远程仓库
git remote add origin https://gitlab.devtools.intel.com/YOUR_USERNAME/dmr-weekly-report.git

# 或使用SSH
git remote add origin git@gitlab.devtools.intel.com:YOUR_USERNAME/dmr-weekly-report.git

# 推送到GitLab
git branch -M main
git push -u origin main
```

### 验证远程仓库
```bash
git remote -v
```

---

## 4. 日常使用

### 查看修改
```bash
# 查看修改的文件
git status

# 查看具体修改内容
git diff

# 查看某个文件的修改
git diff scripts/extract_artifactory_osxml.py
```

### 提交修改
```bash
# 添加修改的文件
git add scripts/extract_artifactory_osxml.py
git add docs/CLAUDE.md

# 或添加所有修改
git add .

# 提交
git commit -m "Fix: Corrected Simics path detection for dmr-rio-7

- Updated extract_artifactory_osxml.py to detect 'rio' keyword
- Modified Rule 7 in CLAUDE.md
- Tested with AP1 B0 Pre-Si builds"

# 推送到远程仓库
git push
```

### 拉取最新代码
```bash
# 拉取远程仓库的最新代码
git pull

# 或者
git fetch origin
git merge origin/main
```

### 查看提交历史
```bash
# 查看提交历史
git log

# 简洁版
git log --oneline

# 查看最近5次提交
git log -5

# 查看某个文件的历史
git log scripts/extract_artifactory_osxml.py
```

---

## 5. 团队协作

### 创建分支
```bash
# 创建并切换到新分支
git checkout -b feature/add-ap3-support

# 或分两步
git branch feature/add-ap3-support
git checkout feature/add-ap3-support

# 查看所有分支
git branch -a
```

### 合并分支
```bash
# 切换回主分支
git checkout main

# 合并功能分支
git merge feature/add-ap3-support

# 推送到远程
git push
```

### 删除分支
```bash
# 删除本地分支
git branch -d feature/add-ap3-support

# 删除远程分支
git push origin --delete feature/add-ap3-support
```

---

## 6. 常用Git命令速查

| 命令 | 说明 |
|------|------|
| `git status` | 查看当前状态 |
| `git add .` | 添加所有修改 |
| `git add <file>` | 添加指定文件 |
| `git commit -m "message"` | 提交修改 |
| `git push` | 推送到远程 |
| `git pull` | 拉取最新代码 |
| `git log` | 查看历史 |
| `git diff` | 查看修改内容 |
| `git checkout <branch>` | 切换分支 |
| `git branch` | 查看分支 |
| `git clone <url>` | 克隆仓库 |

---

## 7. 提交信息规范

### 建议格式
```
<type>: <subject>

<body>

<footer>
```

### Type 类型
- `feat`: 新功能
- `fix`: 修复Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构代码
- `test`: 测试相关
- `chore`: 构建/工具链相关

### 示例
```bash
git commit -m "feat: Add support for AP2 B0 platform

- Added AP2 B0 detection in extract_artifactory_osxml.py
- Updated platform rules in CLAUDE.md
- Added test cases for AP2 B0

Closes #123"
```

---

## 8. 忽略已提交的文件

如果不小心提交了不该提交的文件：

```bash
# 停止追踪某个文件（但保留本地文件）
git rm --cached output/IFWI_Release_Status_2026.26.4.01.html

# 停止追踪整个目录
git rm --cached -r output/

# 提交修改
git commit -m "chore: Remove output files from version control"
git push
```

---

## 9. .gitignore 说明

项目的 `.gitignore` 文件已配置排除：

✅ **已排除（不会提交到Git）：**
- `__pycache__/` - Python缓存
- `.claude/` - Claude配置
- `output/*.html` - 生成的报告（可选）
- `output/*.csv` - CSV数据（可选）
- `test/` - 测试文件（可选）
- `*.7z` - 大型压缩包
- `*.token` - 敏感数据

❓ **可选排除：**
如果想提交报告示例或测试文件，编辑 `.gitignore`：
```bash
# 注释掉这些行即可
# output/*.html
# output/*.csv
# test/
```

---

## 10. 快速开始命令集

### 首次设置
```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"
git init
git add .
git commit -m "Initial commit: DMR Weekly Report Generator"
git remote add origin https://github.com/YOUR_USERNAME/dmr-weekly-report.git
git push -u origin main
```

### 日常使用
```bash
# 修改代码后
git add .
git commit -m "描述你的修改"
git push
```

### 从其他机器克隆
```bash
git clone https://github.com/YOUR_USERNAME/dmr-weekly-report.git
cd dmr-weekly-report
.\scripts\Install-Dependencies.ps1
```

---

## 11. 问题排查

### 问题：推送失败 (Permission denied)
**解决方案：** 配置Git凭据
```bash
# Windows
git config --global credential.helper manager

# 或使用SSH密钥
# 生成SSH密钥
ssh-keygen -t ed25519 -C "your.email@intel.com"

# 添加到GitHub/GitLab
# 复制 ~/.ssh/id_ed25519.pub 内容到网站设置
```

### 问题：误提交了敏感文件
**解决方案：** 从历史中删除
```bash
# 注意：这会重写历史，慎用！
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

### 问题：合并冲突
**解决方案：** 手动解决冲突
```bash
# 拉取时出现冲突
git pull

# 编辑冲突文件，删除冲突标记 <<<<<<<, =======, >>>>>>>

# 标记为已解决
git add <conflicted-file>

# 完成合并
git commit
git push
```

---

## 12. 推荐工作流

### 单人开发
```
main (主分支) → 直接在main上开发和提交
```

### 团队协作
```
main (稳定版本)
  ↓
develop (开发分支)
  ↓
feature/xxx (功能分支)
```

### 操作流程
```bash
# 1. 创建功能分支
git checkout -b feature/add-simics-rio-support

# 2. 开发和提交
git add .
git commit -m "feat: Add Simics Rio support"

# 3. 推送到远程
git push -u origin feature/add-simics-rio-support

# 4. 在GitHub/GitLab创建Pull Request/Merge Request

# 5. 代码审查通过后，合并到main

# 6. 删除功能分支
git branch -d feature/add-simics-rio-support
```

---

## 📚 参考资源

- **Git官方文档**: https://git-scm.com/doc
- **GitHub指南**: https://guides.github.com/
- **GitLab文档**: https://docs.gitlab.com/
- **Git速查表**: https://training.github.com/downloads/github-git-cheat-sheet/

---

**提示：** 
- 💾 经常提交，每个功能点提交一次
- 📝 写清楚的提交信息
- 🔍 提交前用 `git status` 和 `git diff` 检查
- 🚫 不要提交敏感信息（API Token、密码等）
- 🌿 大功能用分支开发，小修改直接在main
