# E-Commerce Selenium Automation Framework

[![CI](https://github.com/yourusername/ecommerce-selenium-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/ecommerce-selenium-framework/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-ready Selenium automation framework for e-commerce testing using Python, PyTest, and Page Object Model (POM) architecture.

## Architecture

```
ecommerce-selenium-framework/
├── pages/                  # Page Object Model classes
├── tests/                  # Test modules organized by feature
├── utils/                  # Utilities (driver factory, helpers, logger)
├── data/                   # Test data (JSON/YAML files)
├── config/                 # Configuration files
├── reports/                # Test reports and screenshots
├── .github/workflows/      # CI/CD pipeline
└── requirements.txt        # Python dependencies
```

## Features

- **Page Object Model (POM)** architecture for maintainable test code
- **Parallel execution** support with pytest-xdist
- **Cross-browser testing** (Chrome, Firefox)
- **Headless execution** for CI/CD
- **Comprehensive reporting** with Allure and pytest-html
- **Screenshot capture** on test failures
- **Explicit waits** and robust element handling
- **Test data management** with JSON fixtures
- **CI/CD integration** with GitHub Actions

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Chrome or Firefox browser
- Git (for cloning repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-selenium-framework.git
   cd ecommerce-selenium-framework
   ```

2. **Run setup script**
   
   **Linux/Mac:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   **Windows:**
   ```cmd
   setup.bat
   ```

3. **Activate virtual environment**
   
   **Linux/Mac:**
   ```bash
   source .venv/bin/activate
   ```
   
   **Windows:**
   ```cmd
   .venv\Scripts\activate
   ```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run smoke tests only
pytest tests/ -m smoke

# Run tests in headless mode
pytest tests/ --headless

# Run tests in parallel
pytest tests/ -n auto

# Run specific test file
pytest tests/test_login.py

# Run with specific browser
pytest tests/ --browser firefox
```

## Test Coverage

The framework covers the following e-commerce user flows:

- **Authentication**: Signup, Login, Logout
- **Product Management**: Search, Browse, View Details
- **Shopping Cart**: Add to Cart, Update Quantity, Remove Items
- **Checkout Process**: Guest/Registered Checkout, Payment
- **Account Management**: Profile Update, Order History
- **End-to-End Flows**: Complete purchase journey

## Configuration

### Environment Variables

```bash
export BASE_URL="https://demo.opencart.com"
export BROWSER="chrome"
export HEADLESS="false"
```

### Config File

Edit `config/config.json` for test-specific settings:

```json
{
  "base_url": "https://demo.opencart.com",
  "implicit_wait": 10,
  "explicit_wait": 20,
  "test_users": {
    "valid_user": {
      "email": "test@example.com",
      "password": "password123"
    }
  }
}
```

## Adding New Tests

1. **Create Page Object** in `pages/` directory
2. **Add test data** in `data/` directory
3. **Write test** in appropriate `tests/` subdirectory
4. **Use fixtures** from `conftest.py`
5. **Add markers** for test categorization

Example:
```python
@pytest.mark.smoke
def test_user_login(driver, test_data):
    login_page = LoginPage(driver)
    home_page = login_page.login(
        test_data['users']['valid_user']['email'],
        test_data['users']['valid_user']['password']
    )
    assert home_page.is_user_logged_in()
```

## CI/CD

The framework includes GitHub Actions workflow that:

- Runs tests on multiple Python versions
- Executes tests in headless mode
- Generates and uploads test reports
- Supports parallel execution
- Fails fast on test failures

## Debugging

### Screenshots on Failure

Screenshots are automatically captured on test failures and saved to `reports/screenshots/`.

### Logs

Detailed logs are available in `reports/logs/test.log`.

### Running Single Test with Debug

```bash
pytest tests/test_login.py::test_valid_login -v -s --tb=short
```

## Best Practices

- Use explicit waits instead of sleep()
- Prefer data-* attributes and semantic selectors
- Implement retry mechanisms for flaky elements
- Keep tests isolated and independent
- Use meaningful test data and assertions
- Follow POM principles for maintainability

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Troubleshooting

### Common Issues

- **WebDriver not found**: Ensure webdriver-manager is installed
- **Element not found**: Check selectors and wait conditions
- **Tests failing in CI**: Verify headless mode compatibility
- **Parallel execution issues**: Check test isolation and data management

### Support

For issues and questions, please create an issue in the repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Selenium WebDriver](https://www.selenium.dev/)
- Testing framework: [PyTest](https://pytest.org/)
- Reporting: [Allure Framework](https://docs.qameta.io/allure/)

## Project Status

This project is actively maintained. For the latest updates, see [CHANGELOG.md](CHANGELOG.md).

## Support

- 📖 [Documentation](README.md)
- 🐛 [Report Bug](https://github.com/yourusername/ecommerce-selenium-framework/issues/new?template=bug_report.md)
- 💡 [Request Feature](https://github.com/yourusername/ecommerce-selenium-framework/issues/new?template=feature_request.md)
- 💬 [Discussions](https://github.com/yourusername/ecommerce-selenium-framework/discussions)