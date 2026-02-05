# Contributing to E-Commerce Selenium Framework

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment for all contributors.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a virtual environment: `python -m venv .venv`
4. Activate virtual environment: `source .venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create a feature branch: `git checkout -b feature/your-feature-name`

## Development Workflow

### Adding New Tests

1. Create test file in appropriate `tests/` subdirectory
2. Follow naming convention: `test_<feature>.py`
3. Use descriptive test names: `test_<action>_<expected_result>`
4. Add appropriate markers: `@pytest.mark.smoke`, `@pytest.mark.critical`
5. Include docstrings explaining test purpose

Example:
```python
@pytest.mark.smoke
def test_user_can_login_with_valid_credentials(self, driver, test_data):
    """Test that user can successfully login with valid credentials."""
    # Test implementation
```

### Adding New Page Objects

1. Create page class in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as class constants
4. Implement page-specific methods
5. Return appropriate page objects from navigation methods
6. Add docstrings for all methods

Example:
```python
class NewPage(BasePage):
    """Page object for new page."""
    
    # Locators
    ELEMENT = (By.ID, "element-id")
    
    def perform_action(self):
        """Perform specific action on page."""
        self.click_element(self.ELEMENT)
```

### Code Style

- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where applicable
- Write descriptive variable and function names

### Running Tests Locally

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_login.py

# Run with specific marker
pytest tests/ -m smoke

# Run in headless mode
pytest tests/ --headless

# Run in parallel
pytest tests/ -n auto
```

### Code Quality Checks

Before submitting a PR, run:

```bash
# Format code
make format

# Run linting
make lint

# Run tests
make test
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Submit PR with clear description
6. Link related issues

### PR Title Format

- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `test: Add tests for feature`
- `refactor: Refactor code`
- `chore: Update dependencies`

## Testing Guidelines

### Test Structure

- **Arrange**: Set up test data and preconditions
- **Act**: Perform the action being tested
- **Assert**: Verify expected outcomes

### Best Practices

- Keep tests independent and isolated
- Use fixtures for common setup
- Avoid hardcoded waits (use explicit waits)
- Clean up test data after execution
- Use meaningful assertions with clear messages
- One logical assertion per test (when possible)

### Test Data

- Store test data in `data/` directory as JSON files
- Use fixtures to load test data
- Generate unique data for tests that create records
- Don't use production data

## Reporting Issues

When reporting issues, include:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, browser)
- Relevant logs

## Questions?

Feel free to open an issue for questions or discussions about the framework.