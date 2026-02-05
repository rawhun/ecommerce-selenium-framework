
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from .logger import get_logger

logger = get_logger(__name__)


class DriverFactory:
    
    @staticmethod
    def create_driver(browser="chrome", headless=False, **kwargs):
        browser = browser.lower()
        logger.info(f"Creating {browser} driver (headless: {headless})")
        
        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless, **kwargs)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless, **kwargs)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless=False, **kwargs):
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        # Standard Chrome options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Add custom options if provided
        custom_options = kwargs.get("chrome_options", [])
        for option in custom_options:
            options.add_argument(option)
        
        # Set preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False, **kwargs):
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        # Add custom options if provided
        custom_options = kwargs.get("firefox_options", [])
        for option in custom_options:
            options.add_argument(option)
        
        # Set preferences
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("media.volume_scale", "0.0")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        return driver
    
    @staticmethod
    def configure_driver(driver, implicit_wait=10, page_load_timeout=30):
        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)
        driver.maximize_window()
        
        logger.info(f"Driver configured with implicit_wait={implicit_wait}s, "
                   f"page_load_timeout={page_load_timeout}s")