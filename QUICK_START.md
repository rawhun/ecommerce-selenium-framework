# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- Chrome or Firefox browser
- Git (for cloning repository)

## Installation

### Option 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p reports/screenshots reports/logs reports/allure reports/html

# Copy configuration
cp config/config.example.json config/config.json
```

## Running Your First Test

### 1. Run Smoke Tests

```bash
pytest tests/ -m smoke -v
```

This will run critical smoke tests covering:
- Login/Logout
- Product search
- Add to cart
- Complete purchase flow

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run Tests in Headless Mode

```bash
pytest tests/ --headless -v
```

### 4. Run Tests in Parallel

```bash
pytest tests/ -n auto -v
```

## Viewing Reports

### Allure Report (Recommended)

```bash
# Generate and serve report
pytest tests/ --alluredir=reports/allure
allure serve reports/allure
```

### HTML Report

```bash
# Generate HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Open in browser
open reports/report.html  # Mac
xdg-open reports/report.html  # Linux
start reports/report.html  # Windows
```

## Common Commands

### Using Makefile (Linux/Mac)

```bash
make install        # Install dependencies
make test           # Run all tests
make test-smoke     # Run smoke tests
make test-parallel  # Run tests in parallel
make test-headless  # Run in headless mode
make report         # Generate and serve Allure report
make clean          # Clean generated files
```

### Using pytest directly

```bash
# Run specific test file
pytest tests/test_login.py -v

# Run specific test
pytest tests/test_login.py::TestLogin::test_valid_login -v

# Run with specific browser
pytest tests/ --browser firefox -v

# Run with custom base URL
pytest tests/ --base-url https://your-site.com -v

# Run tests matching pattern
pytest tests/ -k "login" -v

# Show print statements
pytest tests/ -v -s
```

## Test Markers

```bash
# Run smoke tests
pytest tests/ -m smoke

# Run critical tests
pytest tests/ -m critical

# Run regression tests
pytest tests/ -m regression
```

## Configuration

### Command Line Options

- `--browser chrome|firefox` - Select browser
- `--headless` - Run in headless mode
- `--base-url URL` - Set base URL

### Environment Variables

```bash
export BASE_URL="https://demo.opencart.com"
export BROWSER="chrome"
export HEADLESS="true"
```

### Config File

Edit `config/config.json`:

```json
{
  "base_url": "https://demo.opencart.com",
  "implicit_wait": 10,
  "explicit_wait": 20,
  "browser": "chrome",
  "headless": false
}
```

## Troubleshooting

### WebDriver Issues

The framework uses `webdriver-manager` which automatically downloads and manages browser drivers. If you encounter issues:

```bash
# Clear webdriver cache
rm -rf ~/.wdm

# Reinstall webdriver-manager
pip install --upgrade webdriver-manager
```

### Test Failures

1. Check screenshots in `reports/screenshots/`
2. Review logs in `reports/logs/`
3. Run single test with verbose output:
   ```bash
   pytest tests/test_login.py::TestLogin::test_valid_login -v -s
   ```

### Browser Not Found

Ensure Chrome or Firefox is installed:

```bash
# Check Chrome
google-chrome --version  # Linux
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version  # Mac

# Check Firefox
firefox --version
```

## Next Steps

1. **Explore Tests**: Review test files in `tests/` directory
2. **Understand Page Objects**: Check `pages/` directory
3. **Read Documentation**: 
   - `README.md` - Main documentation
   - `ARCHITECTURE.md` - Framework architecture
   - `CONTRIBUTING.md` - Contribution guidelines
4. **Add Your Tests**: Follow patterns in existing tests
5. **Customize Configuration**: Update `config/config.json`

## Getting Help

- Review `README.md` for detailed documentation
- Check `ARCHITECTURE.md` for design details
- See `CONTRIBUTING.md` for development guidelines
- Create an issue for bugs or questions

## Example Test Run Output

```
$ pytest tests/ -m smoke -v

======================== test session starts =========================
platform darwin -- Python 3.10.0, pytest-7.4.3
plugins: html-4.1.1, xdist-3.3.1, rerunfailures-12.0, allure-pytest-2.13.2
collected 15 items / 10 deselected / 5 selected

tests/test_login.py::TestLogin::test_valid_login PASSED        [ 20%]
tests/test_login.py::TestLogin::test_logout PASSED             [ 40%]
tests/test_product_search.py::TestProductSearch::test_search_valid_product PASSED [ 60%]
tests/test_shopping_cart.py::TestShoppingCart::test_add_product_to_cart PASSED [ 80%]
tests/test_e2e_flow.py::TestE2EFlows::test_complete_purchase_flow_guest PASSED [100%]

==================== 5 passed in 45.23s ====================
```

## Tips for Success

1. **Start Small**: Run smoke tests first
2. **Use Headless Mode**: Faster execution in CI/CD
3. **Parallel Execution**: Use `-n auto` for faster runs
4. **Review Reports**: Check Allure reports for insights
5. **Keep Tests Updated**: Maintain locators and test data
6. **Use Markers**: Organize tests with pytest markers
7. **Check Logs**: Review logs for debugging
8. **Screenshots**: Automatically captured on failures

Happy Testing! 🚀