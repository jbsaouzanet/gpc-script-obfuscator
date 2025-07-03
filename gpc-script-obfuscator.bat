@echo off
setlocal

:: Check if at least one parameter has been passed
if "%~1"=="" (
    echo ❌ No GPC file specified as first parameter.
    echo Usage: %~nx0 "path\to\file.gpc" ["path\to\append.txt"]
    pause >nul
    exit /b 1
)

:: Set the variables for the parameters
set "gpc_file=%~1"
set "append_file=%~2"

echo 📄 GPC file: "%gpc_file%"
if not "%append_file%"=="" (
    echo 📎 Append file: "%append_file%"
)

:: Set path of the Python script
set "script_dir=%~dp0"
set "script_python=%script_dir%gpc-script-obfuscator.py"

:: Check if the Python script exists
if not exist "%script_python%" (
    echo Error: The file "%script_python%" is not found.
    pause >nul
    exit /b 1
)

:: Execute the Python script with one or two parameters
if "%append_file%"=="" (
    python "%script_python%" "%gpc_file%"
) else (
    python "%script_python%" "%gpc_file%" "%append_file%"
)
if errorlevel 1 (
    echo An error occurred while executing the Python script.
    pause >nul
    exit /b 1
)

echo Obfuscation completed! Press any key to close...
pause >nul
endlocal
