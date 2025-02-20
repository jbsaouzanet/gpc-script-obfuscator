@echo off
setlocal

:: Check if a parameter has been passed
if "%~1"=="" (
    echo ❌ No file specified as a parameter.
    echo Usage: %~nx0 "path\to\file.gpc"
    pause >nul
    exit /b 1
)

:: Set the variable for the file passed as a parameter
set "file=%~1"
echo The file passed as a parameter is: "%file%"

:: Set the path of the Python script (make sure it is correct)
set "script_dir=%~dp0"
set "script_python=%script_dir%gpc-script-obfuscator.py"

:: Check if the Python script exists
if not exist "%script_python%" (
    echo ❌ Error: The file "%script_python%" is not found.
    echo Make sure that the Python script is in the same folder as this batch file.
    pause >nul
    exit /b 1
)

:: Execute the Python script with the file as a parameter
python "%script_python%" "%file%"
if errorlevel 1 (
    echo ❌ An error occurred while executing the Python script.
    pause >nul
    exit /b 1
)

echo Obfuscation completed! Press any key to close...
pause >nul
endlocal
