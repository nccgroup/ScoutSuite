@echo off
title ScoutSuite GUI Launcher
echo ========================================================
echo          Starting ScoutSuite GUI inside WSL...
echo ========================================================
echo.

:: Detect WSL installation
where wsl >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] WSL is not found on this system.
    echo Please install WSL with: wsl --install
    pause
    exit /b 1
)

:: Get current directory in WSL path format
for /f "usebackq tokens=*" %%i in (`wsl wslpath -u "%~dp0."`) do set "WSL_REPO_DIR=%%i"

echo [1/2] Launching ScoutSuite GUI server in WSL background...
start "ScoutSuite WSL Server" wsl -e bash -c "cd '%WSL_REPO_DIR%' && bash gui/start_server.sh"

echo [2/2] Waiting for server to initialize...
timeout /t 4 /nobreak >nul

echo Opening browser at http://localhost:8000 ...
start http://localhost:8000

echo.
echo ========================================================
echo Server running! Close the WSL Server window when finished.
echo ========================================================
