# Test AP2 A0 Pre-Si Report Generation
# Auto-fill parameters including Simics version

$ArtifactoryUrl = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_pre_silicon_rel/OAKSTREAMAP.0.RPB.2026.25.3.01.0036.D.29/OakStreamRp_DMR_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_pre_silicon_rel_OakStreamRp_DMR_FSP_Glue_Debug_Linux_90_BuildPkg.7z"
$PlatformStepping = "AP2 A0"
$ReleaseInfo = "released on WW25.3"
$SimicsVersion = "2026ww23.6.00_03"

Write-Host "=== AP2 A0 Pre-Si Test ===" -ForegroundColor Cyan
Write-Host "URL: $ArtifactoryUrl" -ForegroundColor Gray
Write-Host "Platform: $PlatformStepping" -ForegroundColor Gray
Write-Host "Release: $ReleaseInfo" -ForegroundColor Gray
Write-Host "Simics: $SimicsVersion" -ForegroundColor Gray
Write-Host ""

# Prompt for API Token only
Write-Host "Enter Artifactory API Token:" -ForegroundColor Yellow
$SecureToken = Read-Host "API Token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureToken)
$ApiToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "Starting report generation..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Extract data with Simics version
Write-Host "Step 1: Extracting data from Artifactory..." -ForegroundColor Yellow
$extractOutput = python extract_artifactory_osxml.py $ArtifactoryUrl $ApiToken "." $PlatformStepping $SimicsVersion 2>&1
Write-Host $extractOutput

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to extract data" -ForegroundColor Red
    exit 1
}

# Find CSV file
$csvPath = $null
foreach ($line in $extractOutput) {
    if ($line -match "CSV_OUTPUT:(.+)") {
        $csvPath = $matches[1].Trim()
        break
    }
}

if (-not $csvPath -or -not (Test-Path $csvPath)) {
    Write-Host "[ERROR] CSV file not found" -ForegroundColor Red
    exit 1
}

# Extract Orange ID
$csvFilename = Split-Path $csvPath -Leaf
if ($csvFilename -match "OSXML_Summary_(\d{4}\.\d+\.\d+\.\d+)\.csv") {
    $orangeId = $matches[1]
}

# Parse release info
$releaseTense = "has been released"
$releaseWeek = "WW25.3"

# Step 2: Generate HTML report
Write-Host ""
Write-Host "Step 2: Generating HTML report..." -ForegroundColor Yellow
python generate_ifwi_report.py $csvPath $orangeId $releaseWeek $releaseTense

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== SUCCESS ===" -ForegroundColor Green
    Write-Host "Report: IFWI_Release_Status_$orangeId.html" -ForegroundColor Cyan
    Start-Process "IFWI_Release_Status_$orangeId.html"
}
