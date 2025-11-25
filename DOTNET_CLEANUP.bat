@echo off
REM filepath: c:\Users\bdekh\OneDrive - University of Surrey\Work Benaissa Dekhici\Funnding Applications\PyADM1ODE\DOTNET_CLEANUP.bat
REM This script cleans up corrupted .NET installation files

echo.
echo ========================================
echo .NET Cleanup Script
echo ========================================
echo.
echo WARNING: This will remove corrupted .NET files.
echo You must be running as Administrator.
echo.
pause

REM Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo Stopping Windows services...
net stop msiserver
timeout /t 2

echo Removing corrupted package cache...
rmdir /s /q "C:\ProgramData\Package Cache\" 2>nul

echo Removing .NET installation folders...
rmdir /s /q "C:\Program Files\dotnet\" 2>nul

echo Cleaning Windows temporary files...
rmdir /s /q "%TEMP%\*dotnet*" 2>nul
rmdir /s /q "%TEMP%\*Microsoft*" 2>nul

echo Restarting Windows services...
net start msiserver

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Download .NET 6 LTS from:
echo    https://dotnet.microsoft.com/download/dotnet/6.0
echo 2. Run the installer as Administrator
echo 3. Restart your computer
echo 4. Run: python main.py
echo.
pause