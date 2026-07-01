# Installation Troubleshooting Guide

## Common Issues

### Issue 1: PyPI Connection Timeout

**Error:**
```
ERROR: Could not find a version that satisfies the requirement py7zr
ConnectTimeoutError: Connection to pypi.org timed out
```

**Cause:** Network restrictions or proxy requirements at Intel.

**Solutions:**

#### Option A: Use Intel Internal PyPI Mirror (Recommended)

```powershell
# Configure pip to use Intel mirror
pip config set global.index-url https://amrndpi.jf.intel.com/artifactory/api/pypi/pypi-remote/simple
pip config set global.trusted-host amrndpi.jf.intel.com

# Then install packages
pip install py7zr beautifulsoup4 lxml
```

#### Option B: Use HTTP Proxy

```powershell
# Set proxy environment variables
$env:HTTP_PROXY = "http://proxy-dmz.intel.com:911"
$env:HTTPS_PROXY = "http://proxy-dmz.intel.com:912"

# Then install packages
pip install py7zr beautifulsoup4 lxml
```

#### Option C: Configure pip proxy permanently

Create/edit `%APPDATA%\pip\pip.ini`:
```ini
[global]
proxy = http://proxy-dmz.intel.com:911
trusted-host = pypi.org
               pypi.python.org
               files.pythonhosted.org
```

#### Option D: Install from Wheel Files (Offline)

If you have access to pre-downloaded wheel files:
```powershell
pip install py7zr-0.20.0-py3-none-any.whl
pip install beautifulsoup4-4.12.0-py3-none-any.whl
pip install lxml-4.9.0-cp314-cp314-win_amd64.whl
```

---

### Issue 2: Permission Denied

**Error:**
```
ERROR: Could not install packages due to an EnvironmentError: [WinError 5] Access is denied
```

**Solutions:**

```powershell
# Option A: Install to user directory (recommended)
pip install --user py7zr beautifulsoup4 lxml

# Option B: Use virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install py7zr beautifulsoup4 lxml
```

---

### Issue 3: SSL Certificate Verification Failed

**Error:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**

```powershell
# Option A: Use trusted host (temporary)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org py7zr beautifulsoup4 lxml

# Option B: Disable SSL verification (NOT RECOMMENDED for production)
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org py7zr beautifulsoup4 lxml
```

---

### Issue 4: Python Version Incompatibility

**Error:**
```
ERROR: Package 'py7zr' requires a different Python version
```

**Check Python version:**
```powershell
python --version
```

**Required:** Python 3.8 or later

**Solution:**
- Install Python 3.8+ from https://www.python.org/
- Or use `py -3.8` launcher if multiple Python versions installed

---

## Intel-Specific Configuration

### Configure Intel Artifactory as PyPI Mirror

```powershell
# Set index URL
pip config set global.index-url https://amrndpi.jf.intel.com/artifactory/api/pypi/pypi-remote/simple

# Set trusted host
pip config set global.trusted-host amrndpi.jf.intel.com

# Verify configuration
pip config list

# Test installation
pip install --upgrade pip
pip install py7zr beautifulsoup4 lxml
```

### View Current pip Configuration

```powershell
pip config list
pip config debug
```

### Reset pip Configuration

```powershell
# Remove custom settings
pip config unset global.index-url
pip config unset global.trusted-host
pip config unset global.proxy
```

---

## Manual Verification After Installation

### Test Import

```powershell
python -c "import py7zr; print('py7zr:', py7zr.__version__)"
python -c "import bs4; print('beautifulsoup4:', bs4.__version__)"
python -c "import lxml; print('lxml:', lxml.__version__)"
```

### Run Test Script

```powershell
python test_artifactory.py
```

**Expected output:**
```
[OK] requests imported successfully
[OK] py7zr imported successfully
[OK] beautifulsoup4 imported successfully
[OK] lxml imported successfully
```

---

## Alternative: Use Conda

If pip continues to have issues, try Conda:

```powershell
# Install Conda from https://docs.conda.io/en/latest/miniconda.html

# Create environment
conda create -n dmr-report python=3.11

# Activate environment
conda activate dmr-report

# Install packages
conda install -c conda-forge py7zr beautifulsoup4 lxml requests

# Test
python test_artifactory.py
```

---

## Full Installation Steps (Intel Network)

### Step 1: Configure pip for Intel network

```powershell
# Option A: Use Intel Artifactory (recommended)
pip config set global.index-url https://amrndpi.jf.intel.com/artifactory/api/pypi/pypi-remote/simple
pip config set global.trusted-host amrndpi.jf.intel.com

# Option B: Use proxy
$env:HTTP_PROXY = "http://proxy-dmz.intel.com:911"
$env:HTTPS_PROXY = "http://proxy-dmz.intel.com:912"
```

### Step 2: Update pip

```powershell
python -m pip install --upgrade pip
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Verify installation

```powershell
python test_artifactory.py
```

---

## Contact Support

If you continue to experience issues:

1. **Check Intel IT knowledge base** for PyPI/pip configuration
2. **Verify network connectivity** to Intel Artifactory
3. **Request IT support** for proxy/firewall configuration
4. **Use alternative installation method** (Conda, offline wheels)

---

## Quick Reference

### Package Versions (Tested)

```
py7zr>=0.20.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
requests>=2.31.0
selenium>=4.15.0 (for FIV workflow only)
```

### Intel PyPI Mirror URLs

- **Primary:** https://amrndpi.jf.intel.com/artifactory/api/pypi/pypi-remote/simple
- **Alternative:** Check with Intel IT for regional mirrors

### Proxy Settings (Intel)

- **HTTP Proxy:** http://proxy-dmz.intel.com:911
- **HTTPS Proxy:** http://proxy-dmz.intel.com:912

*Note: Proxy addresses may vary by location. Check with your IT admin.*

---

**Last Updated:** 2026-06-30
