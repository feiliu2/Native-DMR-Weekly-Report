# 🚀 START HERE - 新用户快速开始

**欢迎使用 DMR IFWI Report Generator！**

---

## ⚡ 5 分钟快速开始

### Step 1: 安装依赖（仅首次）
```powershell
pip install -r requirements.txt
```

### Step 2: 获取 API Token
- 访问 https://af01p-or.devtools.intel.com
- 用户图标 → Edit Profile
- 复制 API Key

详细说明：[HOW_TO_GET_API_TOKEN.md](HOW_TO_GET_API_TOKEN.md)

### Step 3: 运行脚本
```powershell
.\Generate-IFWI-Report-From-Artifactory.ps1
```

### Step 4: 输入信息
```
选择模式: 1 (Simple mode)
选择平台: 1 (AP1 A0) / 2 (AP1 B0) / 3 (AP2 A0)
输入版本: 2026.26.4.01.0036.D.54
输入 API Token: [粘贴你的token]
```

### Step 5: 完成！
- HTML 报告会自动在浏览器打开 🎉

---

## 📚 详细文档

| 文档 | 说明 |
|------|------|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 快速参考卡片 ⭐ |
| [SIMPLIFIED_WORKFLOW.md](SIMPLIFIED_WORKFLOW.md) | 详细工作流 |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | 部署检查清单 |
| [README.md](README.md) | 完整项目说明 |

---

## ❓ 遇到问题？

1. 检查 Python 版本（需要 3.8+）
   ```powershell
   python --version
   ```

2. 重新安装依赖
   ```powershell
   pip install -r requirements.txt --force-reinstall
   ```

3. 查看 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) 常见问题章节

---

## 💡 使用示例

### 生成 AP1 A0 报告（Post-Silicon）
```
Platform: AP1 A0
Version: 2026.26.4.01.0036.D.54
Release: released on WW26.5
```

### 生成 AP1 B0 报告（Pre-Silicon）
```
Platform: AP1 B0
Version: 2026.25.3.01.0036.D.29
Simics: dmr-7 2026ww24.3.00_45 Pre712
Release: released on WW25.5
```

### 生成 AP2 A0 报告（Pre-Silicon）
```
Platform: AP2 A0
Version: 2026.26.4.02.0036.D.54
Simics: dmr-rio-7 2026ww25.3.00_03 Pre550
Release: released on WW26.5
```

---

## ✅ 系统要求

- ✅ Windows 10/11
- ✅ Python 3.8+
- ✅ PowerShell 5.1+
- ✅ 网络连接
- ✅ Artifactory API Token

---

**开始生成报告吧！** 🎉
