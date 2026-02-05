#!/bin/bash

# Verification script for E-Commerce Selenium Framework

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     E-Commerce Selenium Framework - Setup Verification      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

errors=0

# Check Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python $python_version installed"
else
    echo "❌ Python 3 not found"
    errors=$((errors + 1))
fi
echo ""

# Check virtual environment
echo "Checking virtual environment..."
if [ -d ".venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "⚠ Virtual environment not found (run ./setup.sh)"
fi
echo ""

# Check required files
echo "Checking required files..."
required_files=(
    "README.md"
    "requirements.txt"
    "conftest.py"
    "pytest.ini"
    "LICENSE"
    "CHANGELOG.md"
    ".gitignore"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "❌ $file missing"
        errors=$((errors + 1))
    fi
done
echo ""

# Check directories
echo "Checking directories..."
required_dirs=(
    "pages"
    "tests"
    "utils"
    "config"
    "data"
    ".github/workflows"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ $dir/"
    else
        echo "❌ $dir/ missing"
        errors=$((errors + 1))
    fi
done
echo ""

# Check Python files compile
echo "Checking Python files..."
if command -v python3 &> /dev/null; then
    compile_errors=0
    while IFS= read -r -d '' file; do
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            echo "❌ Syntax error in $file"
            compile_errors=$((compile_errors + 1))
        fi
    done < <(find . -name "*.py" -type f ! -path "./.venv/*" -print0)
    
    if [ $compile_errors -eq 0 ]; then
        echo "✓ All Python files compile successfully"
    else
        echo "❌ $compile_errors Python file(s) have syntax errors"
        errors=$((errors + compile_errors))
    fi
fi
echo ""

# Summary
echo "╔══════════════════════════════════════════════════════════════╗"
if [ $errors -eq 0 ]; then
    echo "║                  ✅ ALL CHECKS PASSED!                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Your framework is ready to use!"
    echo ""
    echo "Next steps:"
    echo "1. Run tests: pytest tests/ -m smoke"
    echo "2. Initialize Git: ./init_git.sh"
    echo "3. Push to GitHub"
else
    echo "║              ⚠ FOUND $errors ERROR(S)                        ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Please fix the errors above before proceeding."
fi
echo ""