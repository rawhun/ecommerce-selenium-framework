#!/bin/bash

# E-Commerce Selenium Framework Setup Script

echo "=========================================="
echo "E-Commerce Selenium Framework Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p reports/screenshots
mkdir -p reports/logs
mkdir -p reports/allure
mkdir -p reports/html

# Copy example config if config doesn't exist
if [ ! -f "config/config.json" ]; then
    echo ""
    echo "Creating config.json from example..."
    cp config/config.example.json config/config.json
fi

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Run smoke tests: pytest tests/ -m smoke"
echo "3. Run all tests: pytest tests/"
echo "4. Generate report: pytest tests/ --alluredir=reports/allure && allure serve reports/allure"
echo ""
echo "For more commands, see README.md or run: make help"
echo ""