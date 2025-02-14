@echo off
:: Path configurations
set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"
set SCRIPT_PATH="C:\3D_Planets_python_scripts\BlenderCode\mainScene.py"
set LOG_FILE="C:\3D_Planets_python_scripts\BlenderCode\debug_log.txt"
set TEMP_LOG="%TEMP%\blender_temp.log"

:: Add timestamp separator to existing log
echo. >> %LOG_FILE%
echo ========== %date% %time% ========== >> %LOG_FILE%

:: Check if Blender is already running
tasklist /FI "IMAGENAME eq blender.exe" | find /I "blender.exe" >nul

if errorlevel 1 (
    echo Starting Blender...
    echo Starting fresh Blender instance... >> %LOG_FILE%
    start /B "" %BLENDER_PATH% --python %SCRIPT_PATH% > %TEMP_LOG% 2>&1
) else (
    echo Closing current Blender instance...
    echo Restarting Blender instance... >> %LOG_FILE%
    taskkill /F /IM blender.exe
    timeout /t 5 /nobreak
    start /B "" %BLENDER_PATH% --python %SCRIPT_PATH% > %TEMP_LOG% 2>&1
)

:: Wait and capture only error lines
timeout /t 30 /nobreak
findstr /i "error exception failed" %TEMP_LOG% >> %LOG_FILE%
del %TEMP_LOG%

echo End of error capture >> %LOG_FILE%
echo ---------------------------------------- >> %LOG_FILE%
