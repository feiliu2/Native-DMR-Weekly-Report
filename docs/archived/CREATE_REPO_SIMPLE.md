# 创建InnerSource仓库 - 3种方法

## 🎯 最快方法：直接问同事

```
找你团队的任何同事问：
"我想创建一个InnerSource仓库，应该联系谁？"

或者问：
"谁负责我们的GitHub仓库管理？"
```

---

## 方法1️⃣: 自己创建（如果有权限）

### 1. 访问
```
https://github.com/intel-innersource
```

### 2. 检查权限
- 看右上角有没有 **"New repository"** 按钮
- 有 → 继续下一步
- 没有 → 用方法2

### 3. 点击 "New repository"

### 4. 填写信息
```
Owner: intel-innersource
Name: firmware.boot.uefi.iafw.dmr.weekly-report-generator
Description: DMR Weekly IFWI Report Generator
Visibility: Internal
❌ 不要勾选任何初始化选项
```

### 5. 点击 "Create repository"

### 6. 复制URL并推送
```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"
git remote add origin git@github.com:intel-innersource/[仓库名].git
git branch -M main
git push -u origin main
```

✅ 完成！

---

## 方法2️⃣: 通过管理员创建

### 1. 找管理员

**方式A: 看已有仓库**
```
访问类似仓库:
https://github.com/intel-innersource/firmware.boot.uefi.iafw.validation.fiv-tool.execution-copilot-ai

点击 Settings → Collaborators
查看谁有Admin权限
```

**方式B: 问同事**
```
"谁是我们团队的GitHub管理员？"
```

### 2. 发邮件

**复制这个模板发给管理员：**

```
主题: 请帮忙创建InnerSource仓库

Hi [管理员],

请帮忙创建一个InnerSource仓库：

仓库名: firmware.boot.uefi.iafw.dmr.weekly-report-generator
组织: intel-innersource  
可见性: Internal
用途: DMR周报自动化生成工具

项目已准备好，等仓库URL就可以推送代码。

谢谢！
[你的名字]
```

### 3. 等待回复

- 通常几小时到1天
- 管理员会给你仓库URL

### 4. 推送代码

```bash
cd "c:\Work\DMR\AI\Native DMR Weekly Report"
git remote add origin [管理员给的URL]
git branch -M main
git push -u origin main
```

✅ 完成！

---

## 方法3️⃣: 临时方案（先用自己的）

### 如果找不到管理员，可以暂时：

1. **创建在你自己的账号下**
   ```
   https://github.com/[你的用户名]/dmr-weekly-report
   ```

2. **推送代码**
   ```bash
   cd "c:\Work\DMR\AI\Native DMR Weekly Report"
   git remote add origin git@github.com:[你的用户名]/dmr-weekly-report.git
   git branch -M main
   git push -u origin main
   ```

3. **等找到管理员后再转移**
   - GitHub支持转移仓库所有权
   - Settings → Transfer ownership

---

## 🔍 常见问题

### Q: 不知道组织名称？
**A:** 问同事或查看你们团队已有的仓库URL

### Q: 没有GitHub账号？
**A:** 用Intel邮箱注册 https://github.com/

### Q: 仓库名称怎么起？
**A:** 参考团队已有仓库的命名规范，或问管理员

### Q: 找不到管理员？
**A:** 
1. 在Slack/Teams团队频道问
2. 团队会议上问
3. 联系IT Help Desk

---

## 📞 需要帮助？

### 最简单的办法
```
1. 在你的团队Slack/Teams频道发消息：
   "Hi team, 我想创建一个InnerSource仓库，应该找谁？"

2. 或者直接找最近创建过仓库的同事问
```

---

## 📚 详细文档

如需更详细的指南，查看：
- **[HOW_TO_CREATE_INNERSOURCE_REPO.md](HOW_TO_CREATE_INNERSOURCE_REPO.md)** - 完整创建指南
- **[INTEL_INNERSOURCE_SETUP.md](INTEL_INNERSOURCE_SETUP.md)** - InnerSource配置
- **[GIT_QUICK_START.md](GIT_QUICK_START.md)** - Git快速开始

---

**记住：最快的方法就是直接问你的同事！** 😊
