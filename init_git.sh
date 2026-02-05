#!/bin/bash

# Git initialization script for E-Commerce Selenium Framework

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     E-Commerce Selenium Framework - Git Initialization      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed. Please install Git first."
    exit 1
fi

echo "✓ Git is installed"
echo ""

# Initialize git repository
echo "Initializing Git repository..."
git init

# Add all files
echo "Adding all files to Git..."
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: E-Commerce Selenium Automation Framework v1.0.0

- Complete Page Object Model (POM) architecture with 10 page objects
- 23 comprehensive test cases covering all e-commerce flows
- WebDriver factory supporting Chrome and Firefox
- Explicit wait helpers with retry mechanisms
- Comprehensive logging and screenshot capture
- GitHub Actions CI/CD pipeline
- Parallel test execution support
- Multiple report formats (Allure, HTML, JUnit XML)
- Complete documentation and contribution guidelines"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Git Initialized Successfully!             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Create a new repository on GitHub"
echo ""
echo "2. Add remote repository:"
echo "   git remote add origin https://github.com/yourusername/ecommerce-selenium-framework.git"
echo ""
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. (Optional) Create a release on GitHub:"
echo "   - Go to your repository on GitHub"
echo "   - Click 'Releases' → 'Create a new release'"
echo "   - Tag: v1.0.0"
echo "   - Title: E-Commerce Selenium Framework v1.0.0"
echo "   - Description: See CHANGELOG.md"
echo ""
echo "✅ Your repository is ready to push to GitHub!"
echo ""