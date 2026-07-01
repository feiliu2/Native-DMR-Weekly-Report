param(
    [Parameter(Mandatory=$true)]
    [string]$FIVUrl,
    
    [string]$OutputPath = "C:\Work\DMR\Weekly Report"
)

Write-Host "Starting OSXML table extraction from FIV Portal..." -ForegroundColor Cyan
Write-Host "URL: $FIVUrl"

try {
    # Download the HTML content
    Write-Host "Downloading page content..."
    $response = Invoke-WebRequest -Uri $FIVUrl -UseBasicParsing
    $htmlContent = $response.Content
    
    # Save raw HTML for debugging
    $debugFile = "$OutputPath\FIV_Debug_$(Get-Date -Format 'yyyyMMdd_HHmmss').html"
    $htmlContent | Out-File -FilePath $debugFile -Encoding UTF8
    Write-Host "Debug HTML saved to: $debugFile" -ForegroundColor Gray

    # Try to extract OSXML table using multiple patterns
    $patterns = @(
        'OSXML.*?</table>',
        'SoC.*?</table>',
        'version.*?</table>'
    )
    
    $tableContent = $null
    foreach ($pattern in $patterns) {
        if ($htmlContent -match $pattern) {
            $tableContent = $matches[0]
            Write-Host "Found table with pattern: $pattern" -ForegroundColor Green
            break
        }
    }

    if ($tableContent) {
        # Display the table
        Write-Host "`n=== OSXML Table ===" -ForegroundColor Cyan
        Write-Host $tableContent
        
        # Save as HTML
        $tableFile = "$OutputPath\OSXML_Table_$(Get-Date -Format 'yyyyMMdd_HHmmss').html"
        $tableContent | Out-File -FilePath $tableFile -Encoding UTF8
        Write-Host "`nTable saved to: $tableFile" -ForegroundColor Green
        
        # Also try to extract and convert to markdown table
        Write-Host "`n" -ForegroundColor Cyan
        Write-Host "Attempting to convert to text format..." -ForegroundColor Cyan
        
        # Extract rows using regex
        $rows = @()
        $rowPattern = '<tr[^>]*>(.*?)</tr>'
        [regex]::Matches($htmlContent, $rowPattern) | ForEach-Object {
            $rowContent = $_.Groups[1].Value
            $cells = @()
            $cellPattern = '<t[dh][^>]*>(.*?)</t[dh]>'
            [regex]::Matches($rowContent, $cellPattern) | ForEach-Object {
                $cellText = $_.Groups[1].Value
                # Remove HTML tags
                $cellText = $cellText -replace '<[^>]*>', ''
                # Trim whitespace
                $cellText = $cellText.Trim()
                $cells += $cellText
            }
            if ($cells.Count -gt 0) {
                $rows += , $cells
            }
        }
        
        if ($rows.Count -gt 0) {
            Write-Host "Extracted table ($($rows.Count) rows):" -ForegroundColor Green
            $rows | ForEach-Object {
                Write-Host ($_ -join " | ")
            }
            
            # Save as CSV
            $csvFile = "$OutputPath\OSXML_Table_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
            $rows | ConvertTo-Csv -NoTypeInformation | Out-File -FilePath $csvFile -Encoding UTF8
            Write-Host "`nCSV saved to: $csvFile" -ForegroundColor Green
        }
        
    } else {
        Write-Host "Warning: Could not find OSXML table" -ForegroundColor Yellow
        Write-Host "HTML content length: $($htmlContent.Length) characters" -ForegroundColor Gray
        Write-Host "Debug file saved - please check: $debugFile" -ForegroundColor Yellow
    }

} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`nComplete!" -ForegroundColor Green
