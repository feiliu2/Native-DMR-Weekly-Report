# Install Python dependencies for DMR IFWI Report Generator

Write-Host "=== Installing Python Dependencies ===" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host "Python version: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if pip is installed
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] pip is not installed" -ForegroundColor Red
    Write-Host "Please reinstall Python with pip included" -ForegroundColor Yellow
    exit 1
}

Write-Host "pip version: $pipVersion" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Installation Complete ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Cyan
    Write-Host "  .\Generate-IFWI-Report-From-Artifactory.ps1" -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "[ERROR] Installation failed" -ForegroundColor Red
    exit 1
}
