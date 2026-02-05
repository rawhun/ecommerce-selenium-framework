@echo off
REM E-Commerce Selenium Framework Setup Script for Windows

echo ==========================================
echo E-Commerce Selenium Framework Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
echo.
echo Creating directory structure...
if not exist "reports\screenshots" mkdir reports\screenshots
if not exist "reports\logs" mkdir reports\logs
if not exist "reports\allure" mkdir reports\allure
if not exist "reports\html" mkdir reports\html

REM Copy example config if config doesn't exist
if not exist "config\config.json" (
    echo.
    echo Creating config.json from example...
    copy config\config.example.json config\config.json
)

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo Next steps:
echo 1. Activate virtual environment: .venv\Scripts\activate
echo 2. Run smoke tests: pytest tests/ -m smoke
echo 3. Run all tests: pytest tests/
echo 4. Generate report: pytest tests/ --alluredir=reports/allure
echo.
echo For more commands, see README.md
echo.
pause