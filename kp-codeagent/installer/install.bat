@echo off
setlocal enabledelayedexpansion

echo ========================================
echo KP Code Agent - Installation Script
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Not running as Administrator. Some features may require admin rights.
    echo.
)

REM Step 1: Check Python
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Installing Python 3.12...
    echo Please wait, this may take a few minutes...

    REM Use winget to install Python if available
    winget --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] winget not found. Please install Python manually:
        echo https://www.python.org/downloads/
        pause
        exit /b 1
    )

    winget install Python.Python.3.12 -e --silent

    REM Refresh environment variables
    echo Refreshing environment...
    call refreshenv >nul 2>&1

    REM Check again
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python installation failed. Please install manually.
        pause
        exit /b 1
    )
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION% found
echo.

REM Step 2: Check Ollama
echo [2/4] Checking Ollama installation...
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running or not installed.
    echo.
    echo Would you like to install Ollama now? (Y/N)
    set /p INSTALL_OLLAMA="> "

    if /i "!INSTALL_OLLAMA!"=="Y" (
        echo Downloading Ollama installer...
        powershell -Command "Invoke-WebRequest -Uri 'https://ollama.ai/download/OllamaSetup.exe' -OutFile '%TEMP%\OllamaSetup.exe'"

        if exist "%TEMP%\OllamaSetup.exe" (
            echo Installing Ollama...
            start /wait "%TEMP%\OllamaSetup.exe"
            del "%TEMP%\OllamaSetup.exe"

            echo Waiting for Ollama to start...
            timeout /t 5 /nobreak >nul
        ) else (
            echo [ERROR] Failed to download Ollama installer.
            echo Please install manually from: https://ollama.ai/download
            pause
            exit /b 1
        )
    ) else (
        echo [WARNING] Ollama is required for KP Code Agent to work.
        echo Please install it from: https://ollama.ai/download
        echo Then run this installer again.
        pause
        exit /b 1
    )
)
echo [OK] Ollama is available
echo.

REM Step 3: Install KP Code Agent
echo [3/4] Installing KP Code Agent...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip --quiet

REM Install KP Code Agent
if exist "%~dp0..\requirements.txt" (
    echo Installing from requirements.txt...
    python -m pip install -r "%~dp0..\requirements.txt" --quiet
) else (
    echo Installing from package...
    python -m pip install kp-codeagent --quiet
)

if errorlevel 1 (
    echo [ERROR] Installation failed!
    pause
    exit /b 1
)

echo [OK] KP Code Agent installed successfully
echo.

REM Step 4: Download CodeLlama model
echo [4/4] Setting up CodeLlama model...
echo This will download approximately 4GB of data.
echo It may take 5-15 minutes depending on your internet connection.
echo.

set /p DOWNLOAD_MODEL="Download CodeLlama 7B model now? (Y/N): "

if /i "!DOWNLOAD_MODEL!"=="Y" (
    echo.
    echo Downloading CodeLlama 7B model...
    echo Please be patient, this will take a while...
    echo.

    ollama pull codellama:7b

    if errorlevel 1 (
        echo [WARNING] Model download failed or was interrupted.
        echo You can download it later by running:
        echo   ollama pull codellama:7b
        echo.
    ) else (
        echo [OK] Model downloaded successfully
        echo.
    )
) else (
    echo.
    echo [INFO] Model download skipped.
    echo You'll need to download it before using KP Code Agent:
    echo   ollama pull codellama:7b
    echo.
)

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo KP Code Agent is now installed.
echo.
echo Quick Start:
echo   1. Open a new terminal window
echo   2. Navigate to your project folder
echo   3. Run: kp-codeagent "your task here"
echo.
echo Examples:
echo   kp-codeagent "create a Python function to calculate fibonacci"
echo   kp-codeagent "add error handling to my code"
echo.
echo For help: kp-codeagent --help
echo To check setup: kp-codeagent check
echo.
echo ========================================
pause
