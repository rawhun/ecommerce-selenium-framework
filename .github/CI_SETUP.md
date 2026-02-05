# CI/CD Setup Guide

## Overview

This project uses GitHub Actions for continuous integration and testing. The workflow is configured to handle testing against an external demo site with appropriate resilience and error handling.

## Workflow Features

### Test Job
- **Multi-version testing**: Tests run on Python 3.9, 3.10, and 3.11
- **Site availability check**: Verifies demo site is accessible before running tests
- **Retry logic**: Attempts to reach the demo site up to 3 times
- **Parallel execution**: Tests run in parallel (limited to 2 workers for stability)
- **Timeout protection**: 30-minute job timeout, 5-10 minute test timeouts
- **Graceful failure**: Tests continue even if some fail (external site dependency)

### Lint Job
- Code quality checks with flake8
- Code formatting verification with black
- Import sorting checks with isort

## Understanding CI Status

### Why Tests Might Fail

This framework tests against `https://demo.opencart.com`, an external demo site. Tests may fail due to:

1. **Demo site unavailability**: The site may be down or slow
2. **Site structure changes**: The demo site owner may update the site
3. **Network issues**: GitHub Actions runners may have connectivity issues
4. **Rate limiting**: Too many requests to the demo site

### What Gets Checked

✅ **Always checked:**
- Code linting and formatting
- Python syntax and imports
- Framework structure and dependencies

⚠️ **May fail due to external factors:**
- Functional tests against demo site
- UI element interactions
- End-to-end user flows

## Artifacts

The workflow generates several artifacts for debugging:

- **Test Results**: HTML and JUnit XML reports
- **Allure Reports**: Detailed test execution reports
- **Screenshots**: Captured on test failures
- **Logs**: Detailed execution logs

Artifacts are retained for 30 days and can be downloaded from the Actions tab.

## Running Tests Locally

To avoid external site dependencies, you can:

1. **Run against a local instance**:
   ```bash
   pytest tests/ --base-url http://localhost:8080
   ```

2. **Run specific test suites**:
   ```bash
   pytest tests/test_login.py -v
   ```

3. **Run in headless mode**:
   ```bash
   pytest tests/ --headless --browser chrome
   ```

## Scheduled Runs

Tests run automatically:
- On every push to `main` or `develop` branches
- On every pull request
- Daily at 2 AM UTC (to monitor demo site health)
- Manually via workflow dispatch

## Improving CI Reliability

To make tests more reliable:

1. **Use a stable test environment**: Deploy your own test instance
2. **Mock external dependencies**: Use tools like WireMock
3. **Add retry logic**: Use `pytest-rerunfailures` for flaky tests
4. **Implement health checks**: Verify site availability before tests

## Troubleshooting

### Tests timeout
- Check if demo site is accessible: `curl -I https://demo.opencart.com`
- Increase timeout values in workflow
- Reduce parallel workers

### Tests fail intermittently
- Add `@pytest.mark.flaky(reruns=2)` to unstable tests
- Increase wait times in page objects
- Check for race conditions

### Artifacts not generated
- Ensure report directories are created
- Check file paths in workflow
- Verify upload-artifact action configuration
