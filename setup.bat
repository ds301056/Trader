@echo off
echo Setting up the Python virtual environment and installing required packages...

REM Check for Python 3.10 or higher
python3 -V > nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.10 or higher is required. Please install it from https://www.python.org/downloads/
    exit /b 1
)

REM Set up Python virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install required packages from requirements.txt
pip install -r requirements.txt

REM Apply Jupyter theme
jt -t onedork -f roboto -cellw 95%

echo Setup is complete. Virtual environment is ready to use.
echo To activate the virtual environment, run: call venv\Scripts\activate
echo To deactivate it, run: call venv\Scripts\deactivate

REM Deactivate virtual environment
call venv\Scripts\deactivate
