# Generate IFWI Report from Artifactory Build Package
# Simplified workflow - automatically constructs Artifactory URL

param(
    [string]$ApiToken,
    [string]$PlatformStepping,
    [string]$OrangeId,
    [string]$SimicsVersion,
    [string]$ReleaseInfo
)

Write-Host "=== DMR IFWI Report Generator ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Prompt for Platform/Stepping
if (-not $PlatformStepping) {
    Write-Host "Step 1: Select Platform and Stepping" -ForegroundColor Yellow
    Write-Host "Options:" -ForegroundColor Gray
    Write-Host "  1. AP1 A0 (Post-Silicon)" -ForegroundColor Gray
    Write-Host "  2. AP1 B0 (Pre-Silicon)" -ForegroundColor Gray
    Write-Host "  3. AP2 A0 (Pre-Silicon)" -ForegroundColor Gray

    $choice = Read-Host "Enter number (1-3)"

    switch ($choice) {
        "1" { $PlatformStepping = "AP1 A0" }
        "2" { $PlatformStepping = "AP1 B0" }
        "3" { $PlatformStepping = "AP2 A0" }
        default {
            Write-Host "[ERROR] Invalid choice. Please enter 1, 2, or 3" -ForegroundColor Red
            exit 1
        }
    }
}

# Validate platform/stepping
if ($PlatformStepping -notmatch "^AP[12] [AB]0$") {
    Write-Host "[ERROR] Invalid Platform/Stepping format. Expected: AP1 A0, AP1 B0, or AP2 A0" -ForegroundColor Red
    exit 1
}

Write-Host "Platform/Stepping: $PlatformStepping" -ForegroundColor Green

# Step 2: Prompt for Orange ID (IFWI ID)
if (-not $OrangeId) {
    Write-Host ""
    Write-Host "Step 2: Enter Orange ID (IFWI ID)" -ForegroundColor Yellow
    Write-Host "Format: YYYY.WW.X.NN" -ForegroundColor Gray
    Write-Host "Example: 2026.24.5.01" -ForegroundColor Gray
    $OrangeId = Read-Host "Orange ID"
}

# Validate Orange ID format
if ($OrangeId -notmatch '^\d{4}\.\d+\.\d+\.\d+$') {
    Write-Host "[ERROR] Invalid Orange ID format. Expected: YYYY.WW.X.NN (e.g., 2026.24.5.01)" -ForegroundColor Red
    exit 1
}

Write-Host "Orange ID: $OrangeId" -ForegroundColor Green

# Step 3: Prompt for Simics Version (only for AP1 B0 / AP2 A0)
$SimicsFullVersion = $null
if ($PlatformStepping -in @("AP1 B0", "AP2 A0")) {
    if (-not $SimicsVersion) {
        Write-Host ""
        Write-Host "Step 3: Enter Simics Version (REQUIRED for Pre-Si)" -ForegroundColor Yellow
        Write-Host "Format: dmr-7 2026ww27.0.00_45 Pre712" -ForegroundColor Gray
        Write-Host "   or:  2026ww27.0.00_45" -ForegroundColor Gray
        Write-Host "This will be used to fetch OSXML information from Simics release notes" -ForegroundColor Gray
        $SimicsInput = Read-Host "Simics Version"
    } else {
        $SimicsInput = $SimicsVersion
    }

    # Try to extract version number (YYYYwwNN.X.XX_NN)
    if ($SimicsInput -match '(\d{4}ww\d{2}\.\d+\.\d+_\d+)') {
        $SimicsVersion = $matches[1]
        # Full version is the entire input
        $SimicsFullVersion = $SimicsInput.Trim()

        # If user only provided version number, construct full version
        if ($SimicsFullVersion -eq $SimicsVersion) {
            # Determine platform path based on 'rio' keyword in input (Rule 7)
            $platformPath = if ($SimicsInput -match 'rio') { "dmr-rio-7" } else { "dmr-7" }
            $SimicsFullVersion = "$platformPath $SimicsVersion"
        }
    } else {
        Write-Host "[ERROR] Invalid Simics version format" -ForegroundColor Red
        Write-Host "Expected format: dmr-7 2026ww27.0.00_45 Pre712" -ForegroundColor Yellow
        Write-Host "            or: 2026ww27.0.00_45" -ForegroundColor Yellow
        exit 1
    }

    Write-Host "Simics Version: $SimicsFullVersion" -ForegroundColor Green
}

# Step 4: Prompt for Release Info
if (-not $ReleaseInfo) {
    Write-Host ""
    Write-Host "Step 4: Enter release information" -ForegroundColor Yellow
    Write-Host "Examples:" -ForegroundColor Gray
    Write-Host "  - 'will be released on WW27.3' (future release)" -ForegroundColor Gray
    Write-Host "  - 'released on WW27.3' (past release)" -ForegroundColor Gray

    $ReleaseInfo = Read-Host "Release info"
}

# Parse release tense and week
$releaseTense = $null
$releaseWeek = $null

if ($ReleaseInfo -match "(will be released) on (WW\d+\.\d+)") {
    $releaseTense = $matches[1]
    $releaseWeek = $matches[2]
}
elseif ($ReleaseInfo -match "(released) on (WW\d+\.\d+)") {
    $releaseTense = "has been released"
    $releaseWeek = $matches[2]
}
elseif ($ReleaseInfo -match "(has been released) on (WW\d+\.\d+)") {
    $releaseTense = $matches[1]
    $releaseWeek = $matches[2]
}
else {
    Write-Host "[ERROR] Invalid release info format" -ForegroundColor Red
    Write-Host "Expected: 'will be released on WWxx.x' or 'released on WWxx.x'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Release: $releaseTense on $releaseWeek" -ForegroundColor Green

# Step 5: Prompt for API Token (last, so it's not exposed long)
if (-not $ApiToken) {
    Write-Host ""
    Write-Host "Step 5: Enter Artifactory API Token" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "How to get API Token:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://af01p-or.devtools.intel.com/" -ForegroundColor Gray
    Write-Host "  2. Click your username (top right) -> 'Edit Profile'" -ForegroundColor Gray
    Write-Host "  3. Scroll to 'API Key' section" -ForegroundColor Gray
    Write-Host "  4. Click 'Generate API Key' or 'Regenerate'" -ForegroundColor Gray
    Write-Host "  5. Copy the token (starts with AKCp...)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "(Token will not be displayed)" -ForegroundColor Gray
    $SecureToken = Read-Host "API Token" -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureToken)
    $ApiToken = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
}

if ([string]::IsNullOrWhiteSpace($ApiToken)) {
    Write-Host "[ERROR] API Token is required" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Searching Artifactory ===" -ForegroundColor Cyan
Write-Host ""

# Step 6: Search Artifactory for builds matching Orange ID
Write-Host "Searching for Orange ID: $OrangeId..." -ForegroundColor Cyan

$searchOutput = python search_artifactory_by_orange_id.py "$PlatformStepping" "$OrangeId" "$ApiToken" 2>&1
$searchExitCode = $LASTEXITCODE
Write-Host $searchOutput

if ($searchExitCode -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to search Artifactory" -ForegroundColor Red
    exit 1
}

# Parse search results
$BiosId = $null
$VersionString = $null

# Check for single match
foreach ($line in $searchOutput) {
    if ($line -match "^BIOS_ID:(.+)$") {
        $BiosId = $matches[1].Trim()
    }
    if ($line -match "^VERSION:(.+)$") {
        $VersionString = $matches[1].Trim()
    }
}

# Check for multiple matches
$multipleMatches = @()
foreach ($line in $searchOutput) {
    if ($line -match "^MATCH_(\d+)_BIOS_ID:(.+)$") {
        $index = [int]$matches[1]
        $biosIdValue = $matches[2].Trim()
        if ($multipleMatches.Count -le $index) {
            $multipleMatches += @{ BiosId = $biosIdValue }
        } else {
            $multipleMatches[$index].BiosId = $biosIdValue
        }
    }
    if ($line -match "^MATCH_(\d+)_VERSION:(.+)$") {
        $index = [int]$matches[1]
        $versionValue = $matches[2].Trim()
        if ($multipleMatches[$index]) {
            $multipleMatches[$index].Version = $versionValue
        }
    }
}

# Handle multiple matches - ask user to choose
if ($multipleMatches.Count -gt 0) {
    Write-Host ""
    Write-Host "Multiple builds found. Please select one:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $multipleMatches.Count; $i++) {
        Write-Host "  $($i+1). BIOS ID: $($multipleMatches[$i].BiosId)" -ForegroundColor Gray
    }

    $choice = Read-Host "Enter number (1-$($multipleMatches.Count))"
    $choiceIndex = [int]$choice - 1

    if ($choiceIndex -lt 0 -or $choiceIndex -ge $multipleMatches.Count) {
        Write-Host "[ERROR] Invalid choice" -ForegroundColor Red
        exit 1
    }

    $BiosId = $multipleMatches[$choiceIndex].BiosId
    $VersionString = $multipleMatches[$choiceIndex].Version
}

if (-not $BiosId -or -not $VersionString) {
    Write-Host "[ERROR] Could not determine BIOS ID from search results" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Found build" -ForegroundColor Green
Write-Host "BIOS ID: $BiosId" -ForegroundColor Cyan
Write-Host "Full Version: $VersionString" -ForegroundColor Cyan

Write-Host ""
Write-Host "Constructing Artifactory URL..." -ForegroundColor Cyan

# Call Python script to construct URL
$constructOutput = python construct_artifactory_url.py "$PlatformStepping" "$VersionString" "$ApiToken" 2>&1
$constructExitCode = $LASTEXITCODE
Write-Host $constructOutput

if ($constructExitCode -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to construct Artifactory URL" -ForegroundColor Red
    exit 1
}

# Extract URL from output
$ArtifactoryUrl = $null
foreach ($line in $constructOutput) {
    if ($line -match "^URL: (https://.+)$") {
        $ArtifactoryUrl = $matches[1]
        break
    }
}

if (-not $ArtifactoryUrl) {
    Write-Host "[ERROR] Could not extract URL from output" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Constructed URL successfully" -ForegroundColor Green
Write-Host "URL: $ArtifactoryUrl" -ForegroundColor Gray

Write-Host ""
Write-Host "=== Processing ===" -ForegroundColor Cyan
Write-Host ""

# Step 7: Extract OSXML data from Artifactory
Write-Host "Downloading and extracting OSXML data..." -ForegroundColor Cyan

# Pass Simics version if provided (use FULL version to preserve 'rio' keyword)
$extractArgs = @("$ArtifactoryUrl", "$ApiToken", ".", "$PlatformStepping")
if ($SimicsFullVersion) {
    $extractArgs += $SimicsFullVersion
}

$extractOutput = python extract_artifactory_osxml.py @extractArgs 2>&1
Write-Host $extractOutput

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to extract data from Artifactory" -ForegroundColor Red
    exit 1
}

# Find the CSV file path from output
$csvPath = $null
foreach ($line in $extractOutput) {
    if ($line -match "CSV_OUTPUT:(.+)") {
        $csvPath = $matches[1].Trim()
        break
    }
}

if (-not $csvPath -or -not (Test-Path $csvPath)) {
    Write-Host "[ERROR] CSV file not generated" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Data extraction complete" -ForegroundColor Green

# Extract Orange ID from CSV filename
$csvFilename = Split-Path $csvPath -Leaf
if ($csvFilename -match "OSXML_Summary_(\d{4}\.\d+\.\d+\.\d+)\.csv") {
    $orangeId = $matches[1]
    Write-Host "Orange ID: $orangeId" -ForegroundColor Cyan
}
else {
    Write-Host "[ERROR] Could not extract Orange ID from CSV filename" -ForegroundColor Red
    exit 1
}

# Step 8: Generate HTML report
Write-Host ""
Write-Host "Generating HTML report..." -ForegroundColor Cyan

# Call Python report generator with all parameters
$reportOutput = python generate_ifwi_report.py "$csvPath" "$orangeId" "$releaseWeek" "$releaseTense" 2>&1
Write-Host $reportOutput

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Failed to generate report" -ForegroundColor Red
    exit 1
}

# Find generated HTML report
$htmlReport = "IFWI_Release_Status_$orangeId.html"
if (Test-Path $htmlReport) {
    Write-Host ""
    Write-Host "=== SUCCESS ===" -ForegroundColor Green
    Write-Host "Generated report: $htmlReport" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Summary:" -ForegroundColor Cyan
    Write-Host "  Platform: $PlatformStepping" -ForegroundColor White
    Write-Host "  Orange ID: $orangeId" -ForegroundColor White
    Write-Host "  Release: $releaseTense on $releaseWeek" -ForegroundColor White
    Write-Host ""

    # Auto-open in browser
    Start-Process $htmlReport
    Write-Host "Report opened in browser" -ForegroundColor Green

    # Cleanup reminder
    Write-Host ""
    Write-Host "=== Cleanup Reminder ===" -ForegroundColor Yellow
    Write-Host "Temporary files (BuildPkg.7z, CSV) are still in this directory." -ForegroundColor Gray
    Write-Host "To clean up and free disk space, run:" -ForegroundColor Gray
    Write-Host "  .\Cleanup-TempFiles.ps1" -ForegroundColor Cyan
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "[ERROR] HTML report not found: $htmlReport" -ForegroundColor Red
    exit 1
}
