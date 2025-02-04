@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Define paths
SET BLENDER_PYTHON_PATH=C:\Program Files\Blender Foundation\Blender 4.3\4.3\python\bin
SET BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.3\blender.exe
SET VENV_PATH=C:\3D_Planets_python_scripts\.venv
SET RESTART_SCRIPT_PATH=C:\3D_Planets_python_scripts\BlenderCode\restart_blender.bat
SET PROJECT_PATH=C:\3D_Planets_python_scripts\BlenderCode
SET ROOT_PATH=C:\3D_Planets_python_scripts

:: Ensure Python is available
IF NOT EXIST "%BLENDER_PYTHON_PATH%\python.exe" (
    echo Blender Python not found at "%BLENDER_PYTHON_PATH%\python.exe"
    exit /b
)

:: Check if virtual environment exists
IF NOT EXIST "%VENV_PATH%" (
    echo .venv does not exist. Creating virtual environment...
    python -m venv "%VENV_PATH%"
    IF NOT EXIST "%VENV_PATH%" (
        echo Failed to create .venv. Exiting.
        exit /b
    )
)

:: Activate the virtual environment
echo Activating virtual environment...
CALL "%VENV_PATH%\Scripts\activate"

:: Check for requirements file and install dependencies
IF NOT EXIST "%ROOT_PATH%\requirements.txt" (
    echo requirements.txt file not found. Exiting.
    exit /b
)

echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r "%ROOT_PATH%\requirements.txt"

:: Verify scipy installation in virtual environment
python -c "import scipy; print('scipy version:', scipy.__version__)" >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo scipy not found in virtual environment. Installing scipy...
    pip install scipy --no-cache-dir
)

:: Verify again
python -c "import scipy; print('scipy version:', scipy.__version__)" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install scipy in virtual environment. Trying Blender Python...

    "%BLENDER_PYTHON_PATH%\python.exe" -m pip install --upgrade pip
    "%BLENDER_PYTHON_PATH%\python.exe" -m pip install scipy --no-cache-dir

    "%BLENDER_PYTHON_PATH%\python.exe" -c "import scipy; print('scipy version:', scipy.__version__)" >nul 2>&1
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install scipy in Blender Python. Exiting.
        exit /b
    )
)

echo scipy successfully installed.

:: Run Blender with activated virtual environment
echo Running Blender...
start "" "%BLENDER_PATH%" --python "%PROJECT_PATH%\\mainScene.py"

:: End of script
echo Script completed.
PAUSE
