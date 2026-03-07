@echo off
setlocal EnableDelayedExpansion

:: ============================================================
::  Advanced File Search — Launcher
::  Checks Python, sets up venv, installs PyQt6, runs app
:: ============================================================

title Advanced File Search — Setup ^& Launch
color 0B

echo.
echo  ============================================================
echo    Advanced File Search  ^|  Launcher
echo  ============================================================
echo.

:: ── Locate this script's directory so paths are always correct ──
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%.venv"
set "APP_FILE=%SCRIPT_DIR%advanced_search.py"
set "REQ_FILE=%SCRIPT_DIR%requirements.txt"

:: ── Check the app file exists ──────────────────────────────────
if not exist "%APP_FILE%" (
    echo  [ERROR] advanced_search.py not found in:
    echo          %SCRIPT_DIR%
    echo.
    echo  Make sure launch.bat and advanced_search.py are in the same folder.
    goto :error_exit
)

:: ── Check Python is installed ──────────────────────────────────
echo  [1/4] Checking Python installation...

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo  [ERROR] Python was not found on your PATH.
    echo.
    echo  Please install Python 3.10 or later from:
    echo    https://www.python.org/downloads/
    echo.
    echo  Make sure to tick "Add Python to PATH" during installation.
    goto :error_exit
)

:: Capture version string for display
for /f "tokens=2" %%V in ('python --version 2^>^&1') do set "PY_VER=%%V"

:: Enforce minimum Python 3.10
for /f "tokens=1,2 delims=." %%A in ("%PY_VER%") do (
    set "PY_MAJOR=%%A"
    set "PY_MINOR=%%B"
)
if %PY_MAJOR% LSS 3 (
    echo  [ERROR] Python 3.10+ required. Found: %PY_VER%
    goto :error_exit
)
if %PY_MAJOR% EQU 3 if %PY_MINOR% LSS 10 (
    echo  [ERROR] Python 3.10+ required. Found: %PY_VER%
    echo  Please upgrade at https://www.python.org/downloads/
    goto :error_exit
)

echo         OK  ^(Python %PY_VER%^)

:: ── Create virtual environment if it doesn't exist ────────────
echo  [2/4] Checking virtual environment...

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo         Not found — creating venv at:
    echo         %VENV_DIR%
    python -m venv "%VENV_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo  [ERROR] Failed to create virtual environment.
        goto :error_exit
    )
    echo         Created successfully.
) else (
    echo         OK  ^(existing venv found^)
)

:: ── Activate the venv ─────────────────────────────────────────
call "%VENV_DIR%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo  [ERROR] Could not activate the virtual environment.
    goto :error_exit
)

:: ── Install / verify PyQt6 ────────────────────────────────────
echo  [3/4] Checking PyQt6...

python -c "import PyQt6" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo         Not installed — installing PyQt6 ^(this may take a minute^)...
    echo.

    :: Write a minimal requirements file if one doesn't exist
    if not exist "%REQ_FILE%" (
        echo PyQt6>=6.4.0 > "%REQ_FILE%"
    )

    pip install --upgrade pip --quiet
    pip install PyQt6
    if %ERRORLEVEL% neq 0 (
        echo.
        echo  [ERROR] PyQt6 installation failed.
        echo  Check your internet connection and try again.
        goto :error_exit
    )
    echo.
    echo         PyQt6 installed successfully.
) else (
    :: Print installed version for info
    for /f "tokens=2" %%P in ('pip show PyQt6 2^>nul ^| findstr /i "^Version"') do set "QT_VER=%%P"
    echo         OK  ^(PyQt6 !QT_VER!^)
)

:: ── Launch the app ────────────────────────────────────────────
echo  [4/4] Launching Advanced File Search...
echo.
echo  ============================================================
echo.

:: Run the app — use pythonw to suppress the console window once launched,
:: but keep this console open to catch startup errors.
python "%APP_FILE%"

set "EXIT_CODE=%ERRORLEVEL%"
if %EXIT_CODE% neq 0 (
    echo.
    echo  [ERROR] The application exited with code %EXIT_CODE%.
    goto :error_exit
)

goto :clean_exit

:: ── Exit handlers ─────────────────────────────────────────────
:error_exit
echo.
echo  ============================================================
echo   Setup failed. Press any key to close.
echo  ============================================================
pause >nul
exit /b 1

:clean_exit
exit /b 0
