# 如何创建Intel InnerSource仓库

## 📋 概述

Intel InnerSource使用GitHub Enterprise，有两种方式创建仓库：
1. **自助创建**（如果你有权限）
2. **申请创建**（通过团队管理员）

---

## 方式1: 自助创建（推荐）

### 前提条件
- 有Intel GitHub账号
- 已加入某个组织（Organization）

### 步骤详解

#### 1. 访问Intel GitHub
```
https://github.com/intel-innersource
```

或者你的团队组织页面，例如：
```
https://github.com/orgs/intel-innersource/repositories
```

#### 2. 检查你的权限

访问你的团队组织页面，查看右上角是否有 **"New"** 或 **"New repository"** 按钮：

```
如果能看到 "New repository" 按钮 → 你有创建权限，继续步骤3
如果看不到 → 需要申请权限，跳转到"方式2"
```

#### 3. 点击创建新仓库

点击 **"New repository"** 按钮

#### 4. 填写仓库信息

**Owner (所有者):**
```
选择: intel-innersource
或你的团队组织（例如：intel-innersource/firmware）
```

**Repository name (仓库名称):**
```
建议命名规范：
firmware.boot.uefi.iafw.dmr.weekly-report-generator

或参考你们团队的命名规范，例如：
- firmware.boot.uefi.iafw.dmr.ifwi-report-tool
- firmware.boot.uefi.iafw.validation.dmr-weekly-reporter
```

**Description (描述):**
```
DMR Weekly IFWI Report Generator - Automated tool to generate HTML reports 
from Artifactory build packages for AP1/AP2 platforms. Supports OSXML, 
PnP/PM, Simics integration, and Unified Patch extraction.
```

**Visibility (可见性):**
```
选择: Internal
说明: Intel内部可见，外部不可见
```

**Initialize repository (初始化仓库):**
```
❌ 不要勾选 "Add a README file"
❌ 不要勾选 "Add .gitignore"
❌ 不要勾选 "Choose a license"

原因: 我们已经有完整的项目文件，不需要初始化
```

#### 5. 点击 "Create repository"

#### 6. 复制仓库URL

创建成功后，GitHub会显示仓库页面，复制仓库URL：

**SSH格式（推荐）：**
```
git@github.com:intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git
```

**HTTPS格式：**
```
https://github.com/intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git
```

#### 7. 推送代码

```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"

# 添加远程仓库
git remote add origin git@github.com:intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git

# 推送
git branch -M main
git push -u origin main
```

✅ **完成！访问你的仓库：**
```
https://github.com/intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator
```

---

## 方式2: 通过管理员申请

### 如果你没有创建权限

#### 步骤1: 找到你的团队管理员

**方式A: 查看组织成员**

1. 访问组织页面：
   ```
   https://github.com/orgs/intel-innersource/people
   ```

2. 查找有 **"Owner"** 或 **"Admin"** 标签的成员

**方式B: 查看你团队已有仓库的管理员**

1. 找一个你们团队的现有仓库，例如：
   ```
   https://github.com/intel-innersource/firmware.boot.uefi.iafw.validation.fiv-tool.execution-copilot-ai
   ```

2. 点击 **"Insights"** → **"Contributors"** 查看主要贡献者

3. 点击 **"Settings"** → **"Collaborators and teams"** 查看管理员

**方式C: 询问团队同事**

问问团队里的同事：
```
"谁负责管理我们团队的GitHub仓库？"
"我想创建一个新的InnerSource仓库，应该联系谁？"
```

#### 步骤2: 发送申请邮件

**邮件模板：**

```
收件人: [团队管理员邮箱]
主题: Request to Create InnerSource Repository for DMR Weekly Report Tool

Hi [管理员名字],

I would like to request the creation of a new InnerSource repository for our 
DMR Weekly IFWI Report Generator project.

Repository Details:
-------------------
Proposed Name: firmware.boot.uefi.iafw.dmr.weekly-report-generator
Organization: intel-innersource
Visibility: Internal
Purpose: Automated tool to generate HTML reports from Artifactory build packages

Project Description:
-------------------
This tool automates the generation of DMR weekly IFWI status reports by:
- Searching and downloading builds from Artifactory
- Extracting OSXML data from build packages
- Integrating Simics release notes
- Generating HTML reports with platform-specific information
- Supporting AP1 A0 Post-Si, AP1 B0 Pre-Si, and AP2 A0 Pre-Si platforms

The code is ready to push, including:
- Complete documentation (27 docs files)
- PowerShell and Python automation scripts (18 scripts)
- Proper .gitignore configuration
- README and setup guides

Could you please help create this repository or grant me permission to create it?

Thank you!
[你的名字]
```

#### 步骤3: 等待回复并获取仓库URL

管理员创建后会给你：
1. 仓库URL
2. 访问权限（通常是 Write 或 Admin）

#### 步骤4: 推送代码

收到URL后，按照"方式1 步骤7"推送代码即可。

---

## 方式3: 通过JIRA/ServiceNow申请（如果团队有流程）

### 某些大型团队可能需要走正式流程

#### 1. 创建工单

在你们团队的工单系统创建申请：

**JIRA模板示例：**
```
Summary: Create InnerSource Repository for DMR Weekly Report Generator

Description:
Request to create a new InnerSource repository.

Repository Name: firmware.boot.uefi.iafw.dmr.weekly-report-generator
Organization: intel-innersource
Visibility: Internal
Requester: [你的名字]
Team: DMR IFWI Team
Purpose: Automated IFWI report generation tool

Justification:
- Centralize DMR weekly report generation code
- Enable team collaboration and version control
- Share automation tools across DMR team members
```

#### 2. 等待审批和创建

通常1-3个工作日内会处理。

---

## 🔍 常见问题

### Q1: 我没有Intel GitHub账号怎么办？

**答：** 申请Intel GitHub账号

1. 访问：https://github.com/
2. 用你的Intel邮箱注册或登录
3. 访问Intel SSO页面完成认证
4. 或联系IT Help Desk申请GitHub Enterprise访问权限

### Q2: 找不到intel-innersource组织？

**答：** 可能的原因

1. **还未加入组织**
   - 联系团队管理员邀请你加入
   - 或访问组织页面申请加入

2. **组织名称不同**
   - 你们团队可能使用不同的组织名
   - 询问同事确认正确的组织名称

3. **权限问题**
   - 确认你的GitHub账号已完成Intel SSO认证

### Q3: 仓库命名有规范吗？

**答：** 是的，通常遵循以下格式

**Intel Firmware项目命名规范：**
```
格式: firmware.boot.uefi.iafw.[category].[project-name]

示例:
✅ firmware.boot.uefi.iafw.dmr.weekly-report-generator
✅ firmware.boot.uefi.iafw.validation.dmr-ifwi-report
✅ firmware.boot.uefi.iafw.tools.dmr-automation

参考现有仓库:
- firmware.boot.uefi.iafw.validation.fiv-tool.execution-copilot-ai
```

**建议咨询你的团队管理员确认具体命名规范。**

### Q4: 应该创建在哪个组织下？

**答：** 取决于你的团队结构

**选项1: intel-innersource（顶层）**
```
适用: 公司级别共享的工具
URL: github.com/intel-innersource/your-repo
```

**选项2: 团队子组织**
```
适用: 特定团队的项目
URL: github.com/intel-innersource/team-name/your-repo
```

**建议：** 询问团队同事或管理员确认正确的组织。

### Q5: 创建仓库需要多久？

**答：** 取决于方式

- **自助创建：** 立即（<1分钟）
- **管理员创建：** 几小时到1天
- **正式流程申请：** 1-3个工作日

---

## 📞 寻求帮助的渠道

### 1. 团队内部渠道

**Slack/Teams频道:**
```
发消息: "Hi team, I need to create an InnerSource repo for our 
         DMR report tool. Who should I contact?"
```

**团队会议:**
```
在站会或周会上提出
```

### 2. 直接找同事

**找最近创建过仓库的同事:**
```
"Hi, I saw you created [repo name]. Can you help me create one too 
 or point me to the right person?"
```

### 3. IT Support

**Intel IT Help Desk:**
```
电话: [内部IT热线]
邮件: it.help@intel.com
工单: ServiceNow
主题: GitHub Enterprise - InnerSource Repository Creation
```

### 4. GitHub文档

**Intel GitHub文档 (内网):**
```
搜索内网Wiki: "Intel GitHub InnerSource"
或: "How to create InnerSource repository"
```

---

## ✅ 创建前检查清单

在申请创建仓库前，确认：

- [ ] 我已有Intel GitHub账号
- [ ] 我知道要使用的组织名称（intel-innersource或其他）
- [ ] 我已确认仓库命名规范
- [ ] 我已准备好仓库描述
- [ ] 我知道要联系的管理员（或有申请渠道）
- [ ] 本地Git仓库已准备好推送

---

## 🎯 推荐操作流程

### 最快路径（大部分情况）

```
1. 访问 https://github.com/intel-innersource
   ↓
2. 看是否有 "New repository" 按钮
   ↓
   有 → 直接创建（方式1）
   ↓
   没有 → 找同事问："谁是我们的GitHub管理员？"
   ↓
3. 联系管理员，发送邮件模板（见上面"步骤2"）
   ↓
4. 等待回复，获取仓库URL
   ↓
5. 推送代码
```

---

## 📋 创建后的配置

仓库创建成功后，建议配置：

### 1. 添加团队成员

**Settings → Collaborators and teams → Add teams/people**

```
角色说明:
- Admin: 完全控制权限（管理仓库设置）
- Write: 可以推送代码
- Read: 只读权限
```

### 2. 设置分支保护

**Settings → Branches → Add rule**

```
保护main分支:
☑ Require pull request reviews before merging
☑ Require status checks to pass before merging
☑ Include administrators
```

### 3. 配置Topics (标签)

**Repository页面 → About → Settings (齿轮图标) → Topics**

```
添加标签:
dmr, ifwi, bios, automation, reporting, artifactory, python, powershell
```

### 4. 设置仓库描述

**About → Settings**

```
Description: DMR Weekly IFWI Report Generator for AP1/AP2 platforms
Website: [如果有内部Wiki链接]
```

---

## 🎉 完成检查

仓库创建并推送后，检查：

✅ 能访问仓库页面  
✅ README.md正常显示  
✅ 所有文件已推送（docs/, scripts/等）  
✅ .gitignore生效（output/, test/未推送）  
✅ 提交历史完整  
✅ 团队成员能访问  

---

## 📚 参考资源

- **Intel GitHub文档**: 搜索内网"GitHub InnerSource Guide"
- **GitHub Enterprise文档**: https://docs.github.com/en/enterprise-server
- **本项目Git指南**: 
  - [GIT_QUICK_START.md](GIT_QUICK_START.md)
  - [INTEL_INNERSOURCE_SETUP.md](INTEL_INNERSOURCE_SETUP.md)
  - [docs/GIT_SETUP_GUIDE.md](docs/GIT_SETUP_GUIDE.md)

---

**总结：最简单的方式就是直接问你的团队同事："我想创建一个InnerSource仓库，应该找谁？" 😊**
