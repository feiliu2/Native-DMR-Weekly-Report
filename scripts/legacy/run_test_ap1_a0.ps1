# Test AP1 A0 Post-Si Report Generation
# Auto-fill parameters

$ArtifactoryUrl = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/Daily/OakStreamAPIfwi/ap_post_silicon_rel/OAKSTREAMAP.0.RPB.2026.26.4.01.0036.D.54/OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux/OakStreamAPIfwi_ap_post_silicon_rel_OakStreamRp_DMR_1P0_FSP_Glue_Debug_Linux_123_BuildPkg.7z"
$PlatformStepping = "AP1 A0"
$ReleaseInfo = "will be released on WW27.3"

Write-Host "=== AP1 A0 Post-Si Test ===" -ForegroundColor Cyan
Write-Host "URL: $ArtifactoryUrl" -ForegroundColor Gray
Write-Host "Platform: $PlatformStepping" -ForegroundColor Gray
Write-Host "Release: $ReleaseInfo" -ForegroundColor Gray
Write-Host ""

# Prompt for API Token only
Write-Host "Enter Artifactory API Token:" -ForegroundColor Yellow
$SecureToken = Read-Host "API Token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureToken)
$ApiToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

Write-Host ""
Write-Host "Starting report generation..." -ForegroundColor Cyan
Write-Host ""

# Call main script with parameters
.\Generate-IFWI-Report-From-Artifactory.ps1 -ArtifactoryUrl $ArtifactoryUrl -ApiToken $ApiToken -PlatformStepping $PlatformStepping -ReleaseInfo $ReleaseInfo
