# Cleanup Temporary Files
# 清理临时文件，准备打包分发

Write-Host "=== DMR Report Tool - Cleanup Temporary Files ===" -ForegroundColor Cyan
Write-Host ""

# 定义要清理的文件类型
$tempPatterns = @(
    "*.csv",                    # 临时数据文件
    "*BuildPkg*.7z",            # 下载的构建包（所有.7z）
    "*.7z",                     # 所有压缩包
    "OSXML_Version.html",       # 临时HTML文件
    "*_release_notes.csv",      # UP release notes
    "*.html"                    # 生成的报告（可选：取消注释以保留）
)

# 定义要排除的重要文件（不删除）
$excludeFiles = @(
    "requirements.txt"          # 依赖文件（重要！）
)

$totalDeleted = 0
$totalSize = 0

Write-Host "Searching for temporary files..." -ForegroundColor Yellow
Write-Host ""

foreach ($pattern in $tempPatterns) {
    $files = Get-ChildItem -Path . -Filter $pattern -ErrorAction SilentlyContinue

    foreach ($file in $files) {
        # 检查是否在排除列表中
        if ($excludeFiles -contains $file.Name) {
            Write-Host "[SKIP] $($file.Name) (important file)" -ForegroundColor Gray
            continue
        }

        $size = $file.Length
        $totalSize += $size
        $sizeInMB = [math]::Round($size / 1MB, 2)

        Write-Host "[DELETE] $($file.Name) ($sizeInMB MB)" -ForegroundColor Red
        Remove-Item $file.FullName -Force
        $totalDeleted++
    }
}

# 清理 __pycache__ 目录
if (Test-Path "__pycache__") {
    Write-Host "[DELETE] __pycache__/ directory" -ForegroundColor Red
    Remove-Item "__pycache__" -Recurse -Force
    $totalDeleted++
}

Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files deleted: $totalDeleted" -ForegroundColor Green
Write-Host "Space freed: $([math]::Round($totalSize / 1MB, 2)) MB" -ForegroundColor Green
Write-Host ""

# 显示剩余的重要文件
Write-Host "=== Important Files (Kept) ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "Python Scripts:" -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.py" | ForEach-Object { Write-Host "  ✓ $($_.Name)" -ForegroundColor Green }

Write-Host ""
Write-Host "PowerShell Scripts:" -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.ps1" | ForEach-Object { Write-Host "  ✓ $($_.Name)" -ForegroundColor Green }

Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Get-ChildItem -Path . -Filter "*.md" | ForEach-Object { Write-Host "  ✓ $($_.Name)" -ForegroundColor Green }

Write-Host ""
Write-Host "Dependencies:" -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "  ✓ requirements.txt" -ForegroundColor Green
}

Write-Host ""
Write-Host "Ready for packaging!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review DEPLOYMENT_CHECKLIST.md" -ForegroundColor White
Write-Host "  2. Compress this folder to .zip" -ForegroundColor White
Write-Host "  3. Share with team members" -ForegroundColor White
