param(
    [Parameter(Mandatory=$true)]
    [string]$BIOSVersion,
    
    [string]$OutputPath = "C:\Work\DMR\Weekly Report"
)

$artifactoryUrl = "https://af01p-or.devtools.intel.com/artifactory/server-bios-staging-local/daily/OakStreamRp/main"
$tempFolder = "$env:TEMP\BIOS_Extract_$([System.Guid]::NewGuid())"
$sevenZipPath = "C:\Program Files\7-Zip\7z.exe"

Write-Host "Starting extraction for BIOS version $BIOSVersion..." -ForegroundColor Cyan

try {
    if (-not (Test-Path $sevenZipPath)) {
        Write-Host "Warning: 7-Zip not found, will try system decompression..." -ForegroundColor Yellow
        $sevenZipPath = $null
    }

    New-Item -ItemType Directory -Path $tempFolder -Force | Out-Null
    Write-Host "Temp folder: $tempFolder"

    $folderName = "OAKSTRM.0.RPB.$BIOSVersion"
    $downloadUrl = "$artifactoryUrl/$folderName/OakStreamRp_DMR_Debug_CLANG/_BuildPkg.7z"
    $downloadPath = "$tempFolder\_BuildPkg.7z"

    Write-Host "Downloading: $downloadUrl"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $downloadPath -ErrorAction Stop
    Write-Host "Download complete!" -ForegroundColor Green

    Write-Host "Extracting..."
    if ($sevenZipPath) {
        & $sevenZipPath x $downloadPath -o"$tempFolder" -y | Out-Null
    } else {
        Expand-Archive -Path $downloadPath -DestinationPath $tempFolder -Force
    }
    Write-Host "Extraction complete!" -ForegroundColor Green

    $htmlFile = Get-ChildItem -Path $tempFolder -Filter "OSXML_Version.html" -Recurse | Select-Object -First 1
    
    if (-not $htmlFile) {
        Write-Host "Error: OSXML_Version.html not found" -ForegroundColor Red
        exit 1
    }

    Write-Host "Found OSXML_Version.html: $($htmlFile.FullName)"

    $htmlContent = Get-Content -Path $htmlFile.FullName -Raw -Encoding UTF8
    
    $pattern = 'PnP-PM Config Recipe.*?</table>'
    if ($htmlContent -match $pattern) {
        $tableContent = $matches[0]
        Write-Host "Found PnP-PM Config Recipe table!" -ForegroundColor Green
        
        Write-Host "`n=== PnP-PM Config Recipe ===" -ForegroundColor Cyan
        Write-Host $tableContent
        
        $outputFile = "$OutputPath\PnP_PM_Config_$BIOSVersion.html"
        $tableContent | Out-File -FilePath $outputFile -Encoding UTF8
        Write-Host "`nResult saved to: $outputFile" -ForegroundColor Green
    } else {
        Write-Host "Warning: PnP-PM Config Recipe table not found" -ForegroundColor Yellow
        Write-Host "HTML file size: $($htmlContent.Length) characters"
    }

} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
} finally {
    if (Test-Path $tempFolder) {
        Remove-Item -Path $tempFolder -Recurse -Force
        Write-Host "Cleaned up temp files" -ForegroundColor Gray
    }
}

Write-Host "`nComplete!" -ForegroundColor Green
