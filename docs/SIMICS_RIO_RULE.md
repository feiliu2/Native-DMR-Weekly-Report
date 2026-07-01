# Simics Path Rule - Rio Detection

**最新规则（2026-06-30 更新）**

---

## 🎯 核心规则（超简单！）

**检查用户提供的 Simics 输入中是否包含 `rio` 字符串：**

```python
# 简单检查
if 'rio' in simics_version.lower():
    platform_path = 'dmr-rio-7'
else:
    platform_path = 'dmr-7'
```

---

## 📋 规则说明

### 包含 'rio' → `dmr-rio-7`

**用户输入示例：**
```
dmr-rio-7 2026ww23.6.00_03 Pre539
```

**检测：** ✅ 包含 'rio'  
**路径：** `dmr-rio-7`  
**URL：** `https://af02p-or.devtools.intel.com/.../platforms/dmr-rio-7/2026ww23.6.00_03/...`

---

### 不包含 'rio' → `dmr-7`

**用户输入示例：**
```
dmr-7 2026ww24.3.00_45 Pre712
```

**检测：** ❌ 不包含 'rio'  
**路径：** `dmr-7`  
**URL：** `https://af02p-or.devtools.intel.com/.../platforms/dmr-7/2026ww24.3.00_45/...`

---

## 💡 为什么这样简单？

**旧规则（复杂）：**
- 根据 `platform_stepping` 参数决定
- AP1 B0 → dmr-7
- AP2 A0 → dmr-rio-7
- 不够灵活

**新规则（简单）：**
- 只看用户输入的字符串
- 有 'rio' → dmr-rio-7
- 没 'rio' → dmr-7
- ✅ 更灵活
- ✅ 用户完全控制
- ✅ 支持特殊情况

---

## 📊 示例对照表

| 用户输入 | 包含 rio? | Simics 路径 | 适用平台 |
|----------|-----------|-------------|----------|
| `dmr-rio-7 2026ww23.6.00_03 Pre539` | ✅ Yes | `dmr-rio-7` | AP1 B0, AP2 A0 |
| `dmr-7 2026ww24.3.00_45 Pre712` | ❌ No | `dmr-7` | AP1 B0 |
| `2026ww25.3.00_03` | ❌ No | `dmr-7` | 默认 |
| `RIO 2026ww23.6.00_03` | ✅ Yes | `dmr-rio-7` | 任意（大小写不敏感）|

---

## 🔧 实现细节

### 代码位置
**文件：** `extract_artifactory_osxml.py`  
**函数：** `download_simics_release_notes()`  
**行号：** ~25-55

### 实现代码

```python
def download_simics_release_notes(simics_version, api_token, platform_stepping):
    """Download Simics release notes and extract IMH/CBB OSXML versions.

    NEW RULE: Determine path from simics_version string
    - If 'rio' in simics_version -> use dmr-rio-7
    - If 'rio' not in simics_version -> use dmr-7
    """
    # Extract pure version number for URL construction
    import re
    version_match = re.search(r'(\d{4}ww\d{2}\.\d+\.\d+_\d+)', simics_version)
    pure_version = version_match.group(1) if version_match else simics_version

    print(f"\nDownloading Simics release notes for version: {pure_version}")

    # NEW RULE: Check if 'rio' is in the FULL simics_version string
    if 'rio' in simics_version.lower():
        platform_path = 'dmr-rio-7'
        print(f"[INFO] Detected 'rio' in Simics version -> using path: {platform_path}")
    else:
        platform_path = 'dmr-7'
        print(f"[INFO] No 'rio' detected in Simics version -> using path: {platform_path}")

    # Build URL with pure version
    url = f"https://af02p-or.devtools.intel.com/artifactory/simics-local/vp-release-its/platforms/{platform_path}/{pure_version}/release_notes/daily_release_notification.md"
```

---

## ✅ 优势

### 1. 灵活性
- ✅ 用户输入什么路径就用什么路径
- ✅ 不依赖 platform_stepping 参数
- ✅ 支持特殊测试场景

### 2. 简单性
- ✅ 只需检查一个关键词
- ✅ 容易理解和维护
- ✅ 不会出错

### 3. 用户友好
- ✅ 用户知道自己的 Simics 版本应该用哪个路径
- ✅ 直接在输入中体现出来
- ✅ 减少系统猜测

---

## 🎯 使用场景

### 场景 1: AP1 B0 使用 dmr-rio-7

**情况：** AP1 B0 的某个特定 Simics 版本使用 RichIO 路径

**用户输入：**
```
Platform: AP1 B0
Simics: dmr-rio-7 2026ww23.6.00_03 Pre539
```

**结果：** ✅ 系统使用 `dmr-rio-7` 路径（因为输入包含 'rio'）

---

### 场景 2: AP2 A0 使用 dmr-7

**情况：** AP2 A0 的某个旧版本使用标准路径

**用户输入：**
```
Platform: AP2 A0
Simics: dmr-7 2026ww20.0.00_10 Pre400
```

**结果：** ✅ 系统使用 `dmr-7` 路径（因为输入不包含 'rio'）

---

### 场景 3: 简化输入（自动补全）

**用户输入（只提供版本号）：**
```
Simics: 2026ww24.3.00_45
```

**结果：** ✅ 系统使用 `dmr-7`（默认路径）

---

## 📝 与旧规则的对比

### 旧规则（已废弃）

```python
# 基于平台参数
if platform_stepping == 'AP1 B0':
    platform_path = 'dmr-7'
elif platform_stepping == 'AP2 A0':
    platform_path = 'dmr-rio-7'
```

**问题：**
- ❌ 不灵活（固定映射）
- ❌ 无法处理特殊情况
- ❌ 平台和路径强绑定

---

### 新规则（当前）

```python
# 基于输入字符串
if 'rio' in simics_version.lower():
    platform_path = 'dmr-rio-7'
else:
    platform_path = 'dmr-7'
```

**优势：**
- ✅ 灵活（由用户输入决定）
- ✅ 支持所有情况
- ✅ 平台无关

---

## 🧪 测试验证

### 测试 1: 包含 'rio'
```python
simics_version = "dmr-rio-7 2026ww23.6.00_03 Pre539"
# Expected: platform_path = 'dmr-rio-7'
# Result: ✅ PASS
```

### 测试 2: 不包含 'rio'
```python
simics_version = "dmr-7 2026ww24.3.00_45 Pre712"
# Expected: platform_path = 'dmr-7'
# Result: ✅ PASS
```

### 测试 3: 大小写不敏感
```python
simics_version = "DMR-RIO-7 2026ww23.6.00_03"
# Expected: platform_path = 'dmr-rio-7' (使用 .lower())
# Result: ✅ PASS
```

### 测试 4: 只有版本号
```python
simics_version = "2026ww25.3.00_03"
# Expected: platform_path = 'dmr-7' (默认)
# Result: ✅ PASS
```

---

## 📚 相关文档

- [CLAUDE.md](CLAUDE.md) - 完整项目规则
- [CRITICAL_RULES.md](CRITICAL_RULES.md) - 关键规则
- [extract_artifactory_osxml.py](extract_artifactory_osxml.py) - 实现代码

---

## ⚠️ 重要提示

**对于开发者：**

1. ✅ **传递完整的 simics_version 字符串**
   - 不要只传递纯版本号
   - 需要包含 'dmr-7' 或 'dmr-rio-7' 前缀

2. ✅ **不要删除 .lower()**
   - 大小写不敏感检查很重要
   - 用户可能输入 'RIO' 或 'Rio'

3. ✅ **保留默认路径**
   - 如果没有 'rio'，使用 `dmr-7`
   - 这是最常见的情况

---

**规则更新日期：** 2026-06-30  
**状态：** ✅ 已实现并测试  
**优先级：** 🟢 标准规则（取代旧的平台映射规则）
