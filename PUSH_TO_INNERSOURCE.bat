@echo off
echo ========================================
echo  Push to Intel InnerSource
echo ========================================
echo.
echo Before running this script:
echo 1. Create repository on Intel InnerSource
echo 2. Copy the repository URL
echo.
echo Example URL format:
echo git@github.com:intel-innersource/firmware.boot.uefi.iafw.dmr.weekly-report-generator.git
echo.
echo ========================================
echo.

set /p REPO_URL="Enter your InnerSource repository URL: "

echo.
echo Configuring remote repository...
git remote add origin %REPO_URL%

echo.
echo Checking remote configuration...
git remote -v

echo.
echo Renaming branch to main...
git branch -M main

echo.
echo Pushing to InnerSource...
git push -u origin main

echo.
echo ========================================
echo  Push Complete!
echo ========================================
echo.
echo Visit your repository:
echo https://github.com/intel-innersource/YOUR_REPO_NAME
echo.
pause
