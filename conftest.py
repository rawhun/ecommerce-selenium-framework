import json
import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from utils.logger import get_logger
from utils.screenshot_helper import capture_screenshot

logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://demo.opencart.com",
        help="Base URL for the application under test"
    )


@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.json")
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Config file not found at {config_path}, using defaults")
        return {
            "base_url": "https://demo.opencart.com",
            "implicit_wait": 10,
            "explicit_wait": 20
        }


@pytest.fixture(scope="session")
def test_data():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    test_data = {}
    
    # Load users data
    users_path = os.path.join(data_dir, "test_users.json")
    if os.path.exists(users_path):
        with open(users_path, 'r') as f:
            test_data['users'] = json.load(f)
    
    # Load products data
    products_path = os.path.join(data_dir, "products.json")
    if os.path.exists(products_path):
        with open(products_path, 'r') as f:
            test_data['products'] = json.load(f)
    
    return test_data


@pytest.fixture(scope="function")
def driver(request, config):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base-url")
    
    logger.info(f"Starting {browser} browser (headless: {headless})")
    
    driver_instance = None
    
    try:
        if browser == "chrome":
            chrome_options = ChromeOptions()
            if headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            service = ChromeService(ChromeDriverManager().install())
            driver_instance = webdriver.Chrome(service=service, options=chrome_options)
            
        elif browser == "firefox":
            firefox_options = FirefoxOptions()
            if headless:
                firefox_options.add_argument("--headless")
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            
            service = FirefoxService(GeckoDriverManager().install())
            driver_instance = webdriver.Firefox(service=service, options=firefox_options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Configure timeouts
        driver_instance.implicitly_wait(config.get("implicit_wait", 10))
        driver_instance.maximize_window()
        
        # Store base URL for easy access
        driver_instance.base_url = base_url
        
        yield driver_instance
        
    except Exception as e:
        logger.error(f"Failed to create driver: {str(e)}")
        raise
    finally:
        if driver_instance:
            logger.info("Closing browser")
            driver_instance.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = None
        for fixture_name in item.fixturenames:
            if fixture_name == "driver":
                driver = item.funcargs.get("driver")
                break
        
        if driver:
            test_name = item.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{test_name}_{timestamp}.png"
            
            try:
                capture_screenshot(driver, screenshot_name)
                logger.info(f"Screenshot captured: {screenshot_name}")
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {str(e)}")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical path test"
    )


def pytest_collection_modifyitems(config, items):
    for item in items:
        # Add smoke marker to tests with 'smoke' in name
        if "smoke" in item.name.lower():
            item.add_marker(pytest.mark.smoke)
        
        # Add critical marker to login/checkout tests
        if any(keyword in item.name.lower() for keyword in ["login", "checkout", "purchase"]):
            item.add_marker(pytest.mark.critical)