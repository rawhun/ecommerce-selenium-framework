
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.wait_helpers import WaitHelpers
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait_helper = WaitHelpers(driver)
        self.base_url = getattr(driver, 'base_url', 'https://demo.opencart.com')
    
    def navigate_to(self, url):
        full_url = url if url.startswith('http') else f"{self.base_url}{url}"
        logger.info(f"Navigating to: {full_url}")
        self.driver.get(full_url)
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_page_title(self):
        return self.driver.title
    
    def is_element_present(self, locator, timeout=5):
        try:
            self.wait_helper.wait_for_element_present(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_helper.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def click_element(self, locator, timeout=None):
        self.wait_helper.safe_click(locator, timeout)
    
    def send_keys_to_element(self, locator, text, clear_first=True, timeout=None):
        self.wait_helper.safe_send_keys(locator, text, clear_first, timeout)
    
    def get_element_text(self, locator, timeout=None):
        return self.wait_helper.wait_and_get_text(locator, timeout)
    
    def get_element_attribute(self, locator, attribute, timeout=None):
        element = self.wait_helper.wait_for_element_present(locator, timeout)
        return element.get_attribute(attribute)
    
    def select_dropdown_by_text(self, locator, text, timeout=None):
        element = self.wait_helper.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(text)
        logger.debug(f"Selected dropdown option: {text}")
    
    def select_dropdown_by_value(self, locator, value, timeout=None):
        element = self.wait_helper.wait_for_element_visible(locator, timeout)
        select = Select(element)
        select.select_by_value(value)
        logger.debug(f"Selected dropdown value: {value}")
    
    def wait_for_page_load(self, timeout=30):
        self.driver.implicitly_wait(0)  # Temporarily disable implicit wait
        try:
            self.wait_helper.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.debug("Page loaded completely")
        except TimeoutException:
            logger.warning(f"Page did not load completely within {timeout}s")
        finally:
            self.driver.implicitly_wait(10)  # Restore implicit wait
    
    def scroll_to_element(self, locator, timeout=None):
        element = self.wait_helper.wait_for_element_present(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        logger.debug(f"Scrolled to element: {locator}")
    
    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.debug("Scrolled to top of page")
    
    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.debug("Scrolled to bottom of page")
    
    def refresh_page(self):
        logger.info("Refreshing page")
        self.driver.refresh()
        self.wait_for_page_load()
    
    def switch_to_window(self, window_handle):
        self.driver.switch_to.window(window_handle)
        logger.debug(f"Switched to window: {window_handle}")
    
    def get_window_handles(self):
        return self.driver.window_handles
    
    def close_current_window(self):
        self.driver.close()
        logger.debug("Closed current window")
    
    def accept_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()
        logger.debug("Accepted alert")
    
    def dismiss_alert(self):
        alert = self.driver.switch_to.alert
        alert.dismiss()
        logger.debug("Dismissed alert")
    
    def get_alert_text(self):
        alert = self.driver.switch_to.alert
        text = alert.text
        logger.debug(f"Alert text: {text}")
        return text