param(
    [string]$OutputPath = "C:\Work\DMR\Weekly Report"
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  DMR Multi-IFWI Report Generator"  -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Ask how many Orange IFWIs to include
$count = Read-Host "How many Orange IFWIs to include in the report?"
$count = [int]$count

if ($count -le 0) {
    Write-Host "Error: Count must be greater than 0" -ForegroundColor Red
    exit 1
}

$orangeDataList = @()

# Collect information for each Orange IFWI
for ($i = 1; $i -le $count; $i++) {
    Write-Host ""
    Write-Host "=== Orange IFWI #$i ===" -ForegroundColor Yellow
    $FIVUrl = Read-Host "Enter FIV URL"
    $ReleaseInput = Read-Host "Enter release info (e.g., 'released on WW26.5' or 'will be released on WW26.5')"

    # Parse release week and tense from input
    $ReleaseTense = "has been released"
    $ReleaseWeek = ""

    if ($ReleaseInput -match "will be released on (WW\d+\.\d+)") {
        $ReleaseTense = "will be released"
        $ReleaseWeek = $matches[1]
    } elseif ($ReleaseInput -match "(has been released|released) on (WW\d+\.\d+)") {
        $ReleaseTense = "has been released"
        $ReleaseWeek = $matches[2]
    } elseif ($ReleaseInput -match "(WW\d+\.\d+)") {
        # If only week number provided, default to "has been released"
        $ReleaseWeek = $matches[1]
        $ReleaseTense = "has been released"
    }

    Write-Host "Detected: $ReleaseTense on $ReleaseWeek" -ForegroundColor Cyan

    Write-Host ""
    Write-Host "[Step $i/$count] Extracting data from FIV Portal..." -ForegroundColor Green

    # Extract data
    $extractOutput = & python.exe "$OutputPath\extract_fiv_table.py" $FIVUrl $OutputPath 2>&1

    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Data extraction failed for Orange #$i" -ForegroundColor Red
        Write-Host $extractOutput
        exit 1
    }

    # Display output
    $extractOutput | ForEach-Object { Write-Host $_ }

    # Extract Orange ID, CSV filename, and Emulation info from output
    $csvFile = $null
    $OrangeID = $null
    $HasEmulation = $false
    foreach ($line in $extractOutput) {
        if ($line -match "CSV_OUTPUT:(.+)") {
            $csvFile = $matches[1].Trim()
            Write-Host "Found CSV: $csvFile" -ForegroundColor Green
        }
        if ($line -match "Extracted Orange ID:\s*(\S+)") {
            $OrangeID = $matches[1].Trim()
            Write-Host "Auto-detected Orange ID: $OrangeID" -ForegroundColor Cyan
        }
        if ($line -match "Has Emulation Info:\s*True") {
            $HasEmulation = $true
            Write-Host "Detected Emulation Info in Orange Report" -ForegroundColor Cyan
        }
    }

    if (-not $csvFile) {
        Write-Host "Error: Could not find generated CSV file for Orange #$i" -ForegroundColor Red
        exit 1
    }

    if (-not (Test-Path $csvFile)) {
        Write-Host "Error: CSV file does not exist: $csvFile" -ForegroundColor Red
        exit 1
    }

    # If Orange ID was not auto-detected, ask user
    if (-not $OrangeID) {
        Write-Host "Warning: Could not auto-detect Orange ID from URL" -ForegroundColor Yellow
        $OrangeID = Read-Host "Enter Orange IFWI ID manually (e.g., 2026.24.6.01)"
    }

    # Display emulation detection result (no user input needed - auto-calculated)
    if ($HasEmulation) {
        Write-Host "Detected Emulation info - uBIOS release statement will be auto-generated" -ForegroundColor Cyan
    }

    # Add to list
    $orangeDataList += @{
        CSVFile = $csvFile
        OrangeID = $OrangeID
        ReleaseWeek = $ReleaseWeek
        ReleaseTense = $ReleaseTense
    }
}

# Generate combined HTML report
Write-Host ""
Write-Host "==================================================" -ForegroundColor Yellow
Write-Host "Generating Combined HTML Report..." -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Yellow

# Create CSV list file for Python script (use UTF8 without BOM)
$csvListFile = "$OutputPath\temp_csv_list.txt"
$orangeDataList | ForEach-Object {
    "$($_.CSVFile)|$($_.OrangeID)|$($_.ReleaseWeek)|$($_.ReleaseTense)" | Out-File -FilePath $csvListFile -Append -Encoding ASCII
}

# Generate combined report
& python.exe "$OutputPath\generate_multi_ifwi_report.py" $csvListFile

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Report generation failed" -ForegroundColor Red
    exit 1
}

# Clean up temp file
Remove-Item $csvListFile -Force

Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "  SUCCESS! Combined report generated." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "The report has been opened in your browser." -ForegroundColor Green
