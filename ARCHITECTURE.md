# Framework Architecture

## Overview

This framework follows the Page Object Model (POM) design pattern with clear separation of concerns, making it maintainable, scalable, and easy to understand.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Test Layer                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  test_login.py  │  test_cart.py  │  test_checkout.py │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Page Object Layer                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LoginPage  │  CartPage  │  CheckoutPage  │  etc...  │  │
│  └──────────────────────────────────────────────────────┘  │
│                     (Inherits from)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    BasePage                          │  │
│  │  - Common methods (click, send_keys, wait, etc.)    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Utility Layer                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  WaitHelpers  │  Logger  │  ScreenshotHelper  │ etc. │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      WebDriver Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              DriverFactory                           │  │
│  │  - Chrome/Firefox configuration                      │  │
│  │  - Headless mode support                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Chrome/Firefox)                 │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
ecommerce-selenium-framework/
│
├── pages/                      # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py           # Base class with common methods
│   ├── home_page.py           # Home page object
│   ├── login_page.py          # Login page object
│   ├── product_page.py        # Product page object
│   ├── cart_page.py           # Shopping cart page object
│   ├── checkout_page.py       # Checkout page object
│   ├── account_page.py        # Account dashboard page object
│   └── ...                    # Other page objects
│
├── tests/                      # Test modules
│   ├── __init__.py
│   ├── test_login.py          # Login tests
│   ├── test_product_search.py # Product search tests
│   ├── test_shopping_cart.py  # Shopping cart tests
│   ├── test_checkout.py       # Checkout tests
│   ├── test_account.py        # Account management tests
│   └── test_e2e_flow.py       # End-to-end flow tests
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── driver_factory.py      # WebDriver creation and configuration
│   ├── wait_helpers.py        # Wait and element interaction helpers
│   ├── logger.py              # Logging configuration
│   └── screenshot_helper.py   # Screenshot capture utilities
│
├── data/                       # Test data files
│   ├── test_users.json        # User test data
│   └── products.json          # Product test data
│
├── config/                     # Configuration files
│   ├── config.json            # Active configuration
│   └── config.example.json    # Example configuration template
│
├── reports/                    # Test reports (generated)
│   ├── screenshots/           # Failure screenshots
│   ├── logs/                  # Test execution logs
│   ├── allure/                # Allure report data
│   └── html/                  # HTML reports
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD pipeline
│
├── conftest.py                # Pytest fixtures and configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── .editorconfig              # Editor configuration
├── Makefile                   # Common commands
├── README.md                  # Project documentation
├── CONTRIBUTING.md            # Contribution guidelines
└── ARCHITECTURE.md            # This file
```

## Design Patterns

### 1. Page Object Model (POM)

Each web page is represented by a class that:
- Encapsulates page elements (locators)
- Provides methods for page interactions
- Returns other page objects for navigation
- Hides implementation details from tests

**Benefits:**
- Reduces code duplication
- Improves maintainability
- Makes tests more readable
- Centralizes element locators

### 2. Factory Pattern

`DriverFactory` creates WebDriver instances:
- Supports multiple browsers
- Configures browser options
- Handles headless mode
- Manages driver lifecycle

### 3. Fixture Pattern

Pytest fixtures provide:
- WebDriver instances
- Test data loading
- Configuration management
- Setup and teardown

## Component Details

### Base Page

The `BasePage` class provides common functionality:
- Element interaction methods
- Wait helpers integration
- Navigation methods
- Scroll operations
- Alert handling

All page objects inherit from `BasePage`.

### Wait Helpers

`WaitHelpers` class provides robust waiting mechanisms:
- Explicit waits for element states
- Safe click with retry logic
- Text presence verification
- URL change detection
- Element disappearance

### Logger

Centralized logging with:
- Console output (colored)
- File output (detailed)
- Different log levels
- Test execution tracking

### Screenshot Helper

Automatic screenshot capture:
- On test failures (via pytest hook)
- Full page screenshots
- Element-specific screenshots
- Allure report integration

## Test Organization

### Test Structure

Tests are organized by feature:
- `test_login.py` - Authentication tests
- `test_product_search.py` - Search functionality
- `test_shopping_cart.py` - Cart operations
- `test_checkout.py` - Checkout process
- `test_account.py` - Account management
- `test_e2e_flow.py` - End-to-end scenarios

### Test Markers

- `@pytest.mark.smoke` - Critical smoke tests
- `@pytest.mark.regression` - Full regression suite
- `@pytest.mark.critical` - Critical path tests

## Data Management

### Test Data

- Stored in JSON files under `data/`
- Loaded via fixtures
- Supports multiple test users
- Product search terms and data

### Configuration

- Environment-specific settings in `config/config.json`
- Command-line overrides via pytest options
- Environment variable support

## Reporting

### Multiple Report Formats

1. **Allure Reports**
   - Rich HTML reports
   - Test history
   - Screenshots attached
   - Detailed test steps

2. **Pytest HTML**
   - Self-contained HTML report
   - Test results summary
   - Failure details

3. **JUnit XML**
   - CI/CD integration
   - Test result parsing
   - Trend analysis

## CI/CD Integration

### GitHub Actions Workflow

- Runs on push and PR
- Multiple Python versions
- Parallel test execution
- Artifact upload
- Test result publishing

### Pipeline Stages

1. Setup environment
2. Install dependencies
3. Run smoke tests
4. Run full test suite
5. Generate reports
6. Upload artifacts

## Best Practices

### Element Locators

Priority order:
1. ID attributes
2. Data attributes (data-*)
3. CSS selectors (semantic)
4. XPath (as last resort)

### Waits

- Always use explicit waits
- Never use `time.sleep()`
- Implement retry mechanisms
- Handle stale elements

### Test Independence

- Tests should not depend on each other
- Use unique test data
- Clean up after tests
- Isolate test state

### Error Handling

- Capture screenshots on failure
- Log detailed error information
- Provide meaningful assertions
- Handle expected exceptions

## Scalability

### Adding New Tests

1. Create page object if needed
2. Add test data to JSON files
3. Write test using existing patterns
4. Add appropriate markers
5. Update documentation

### Adding New Pages

1. Create page class inheriting from `BasePage`
2. Define locators as constants
3. Implement page-specific methods
4. Return appropriate page objects
5. Add docstrings

### Extending Utilities

1. Add utility module in `utils/`
2. Follow existing patterns
3. Add logging
4. Write unit tests if applicable
5. Update documentation

## Performance Optimization

- Parallel test execution with pytest-xdist
- Browser reuse where appropriate
- Efficient element location
- Minimal page loads
- Smart wait strategies

## Maintenance

### Regular Tasks

- Update dependencies
- Review and update locators
- Refactor duplicate code
- Update documentation
- Review test coverage

### Monitoring

- Track test execution time
- Monitor flaky tests
- Review failure patterns
- Analyze CI/CD metrics