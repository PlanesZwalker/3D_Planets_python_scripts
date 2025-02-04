@echo off
:: Path to your Blender executable (full path to blender.exe)
set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"

:: Path to your main Python script (full path to the Python script)
set SCRIPT_PATH="C:\3D_Planets_python_scripts\BlenderCode\mainScene.py"

:: Check if Blender is already running
tasklist /FI "IMAGENAME eq blender.exe" | find /I "blender.exe" >nul

if errorlevel 1 (
    echo Blender is not running. Opening it now...
    start "" %BLENDER_PATH% --python %SCRIPT_PATH%
    echo Blender has been opened and the script is running.
    :: Wait for Blender to open and run the script
    timeout /t 5 /nobreak
) else (
    echo Blender is already running. Closing it...
    taskkill /F /IM blender.exe
    echo Waiting for Blender to fully close...
    timeout /t 5 /nobreak
    echo Re-opening Blender and running the script...
    start "" %BLENDER_PATH% --python %SCRIPT_PATH%
    echo Blender has been reopened and the script is running.
)
