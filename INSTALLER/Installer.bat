@echo off
setlocal

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    :: Download Python installer
    curl -O https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
    :: Install Python silently
    start /wait python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-3.11.0-amd64.exe
    echo Python has been installed.
) else (
    echo Python is already installed.
)

:: Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing pip...
    python -m ensurepip
    python -m pip install --upgrade pip
    echo pip has been installed.
) else (
    echo pip is already installed.
)

:: Install required modules
echo Installing required modules...
python -m pip install pycryptodome
echo Required modules have been installed.

endlocal
pause
