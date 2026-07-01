# Generate Both AP1 A0 and AP2 A0 Reports
# Only ask for API Token once, then generate both reports

Write-Host "=== DMR IFWI Dual Report Generator ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Will generate:" -ForegroundColor Yellow
Write-Host "  1. AP1 A0 Post-Si (WW27.3)" -ForegroundColor Gray
Write-Host "  2. AP2 A0 Pre-Si (WW25.3)" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host "How to Get Artifactory API Token" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Login to Artifactory:" -ForegroundColor White
Write-Host "   https://af01p-or.devtools.intel.com/" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Click your username (top right corner)" -ForegroundColor White
Write-Host ""
Write-Host "3. Select 'Edit Profile'" -ForegroundColor White
Write-Host ""
Write-Host "4. In Profile page, find 'API Key' section" -ForegroundColor White
Write-Host ""
Write-Host "5. Click 'Generate API Key' or 'Regenerate'" -ForegroundColor White
Write-Host ""
Write-Host "6. Copy the token (starts with AKCp...)" -ForegroundColor White
Write-Host ""
Write-Host "7. Paste it below when prompted" -ForegroundColor White
Write-Host ""
Write-Host "============================================" -ForegroundColor Yellow
Write-Host ""

# Get API Token once
Write-Host "Enter Artifactory API Token (used for both reports):" -ForegroundColor Yellow
$SecureToken = Read-Host "API Token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureToken)
$ApiToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Report 1: AP1 A0 Post-Si" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$Url1 = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z"

Write-Host "Extracting data..." -ForegroundColor Yellow
$extract1 = python extract_artifactory_osxml.py $Url1 $ApiToken "." "AP1 A0" 2>&1
Write-Host $extract1

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] AP1 A0 extraction failed" -ForegroundColor Red
    exit 1
}

# Find CSV
$csv1 = $null
foreach ($line in $extract1) {
    if ($line -match "CSV_OUTPUT:(.+)") {
        $csv1 = $matches[1].Trim()
        break
    }
}

# Extract Orange ID
if ($csv1 -match "OSXML_Summary_(\d{4}\.\d+\.\d+\.\d+)\.csv") {
    $orangeId1 = $matches[1]
}

Write-Host ""
Write-Host "Generating HTML report..." -ForegroundColor Yellow
python generate_ifwi_report.py $csv1 $orangeId1 "WW27.3" "will be released"

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] AP1 A0 report generated: IFWI_Release_Status_$orangeId1.html" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Report 2: AP2 A0 Pre-Si" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$Url2 = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_pre_silicon_rel/OAKSTREAMAP.0.RPB.2026.25.3.01.0036.D.29/OakStreamRp_DMR_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_pre_silicon_rel_OakStreamRp_DMR_FSP_Glue_Debug_Linux_90_BuildPkg.7z"
$SimicsVer = "2026ww23.6.00_03"

Write-Host "Extracting data (with Simics version)..." -ForegroundColor Yellow
$extract2 = python extract_artifactory_osxml.py $Url2 $ApiToken "." "AP2 A0" $SimicsVer 2>&1
Write-Host $extract2

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] AP2 A0 extraction failed" -ForegroundColor Red
    exit 1
}

# Find CSV
$csv2 = $null
foreach ($line in $extract2) {
    if ($line -match "CSV_OUTPUT:(.+)") {
        $csv2 = $matches[1].Trim()
        break
    }
}

# Extract Orange ID
if ($csv2 -match "OSXML_Summary_(\d{4}\.\d+\.\d+\.\d+)\.csv") {
    $orangeId2 = $matches[1]
}

Write-Host ""
Write-Host "Generating HTML report..." -ForegroundColor Yellow
python generate_ifwi_report.py $csv2 $orangeId2 "WW25.3" "has been released"

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] AP2 A0 report generated: IFWI_Release_Status_$orangeId2.html" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "BOTH REPORTS COMPLETED" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Write-Host "  1. IFWI_Release_Status_$orangeId1.html (AP1 A0 Post-Si)" -ForegroundColor White
Write-Host "  2. IFWI_Release_Status_$orangeId2.html (AP2 A0 Pre-Si)" -ForegroundColor White
Write-Host ""

# Open both reports
Start-Process "IFWI_Release_Status_$orangeId1.html"
Start-Process "IFWI_Release_Status_$orangeId2.html"

Write-Host "Reports opened in browser" -ForegroundColor Green
