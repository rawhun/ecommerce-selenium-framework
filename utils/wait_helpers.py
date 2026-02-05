
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException, 
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from selenium.webdriver.common.action_chains import ActionChains

from .logger import get_logger

logger = get_logger(__name__)


class WaitHelpers:
    
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
    
    def wait_for_element_visible(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible within {wait_time}s: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not clickable within {wait_time}s: {locator}")
            raise
    
    def wait_for_element_present(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element present: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not present within {wait_time}s: {locator}")
            raise
    
    def wait_for_text_in_element(self, locator, text, timeout=None):
        wait_time = timeout or self.timeout
        try:
            result = WebDriverWait(self.driver, wait_time).until(
                EC.text_to_be_present_in_element(locator, text)
            )
            logger.debug(f"Text '{text}' found in element: {locator}")
            return result
        except TimeoutException:
            logger.error(f"Text '{text}' not found in element within {wait_time}s: {locator}")
            raise
    
    def wait_for_url_contains(self, url_fragment, timeout=None):
        wait_time = timeout or self.timeout
        try:
            result = WebDriverWait(self.driver, wait_time).until(
                EC.url_contains(url_fragment)
            )
            logger.debug(f"URL contains: {url_fragment}")
            return result
        except TimeoutException:
            logger.error(f"URL does not contain '{url_fragment}' within {wait_time}s")
            raise
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        wait_time = timeout or self.timeout
        try:
            result = WebDriverWait(self.driver, wait_time).until_not(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Element disappeared: {locator}")
            return result
        except TimeoutException:
            logger.error(f"Element still present after {wait_time}s: {locator}")
            raise
    
    def safe_click(self, locator, timeout=None, retries=3):
        wait_time = timeout or self.timeout
        
        for attempt in range(retries):
            try:
                element = self.wait_for_element_clickable(locator, wait_time)
                
                # Scroll element into view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)  # Brief pause after scroll
                
                # Try regular click first
                element.click()
                logger.debug(f"Successfully clicked element: {locator}")
                return True
                
            except (ElementClickInterceptedException, ElementNotInteractableException) as e:
                logger.warning(f"Click intercepted on attempt {attempt + 1}: {e}")
                
                if attempt < retries - 1:
                    # Try JavaScript click as fallback
                    try:
                        element = self.wait_for_element_present(locator, wait_time)
                        self.driver.execute_script("arguments[0].click();", element)
                        logger.debug(f"JavaScript click successful: {locator}")
                        return True
                    except Exception as js_error:
                        logger.warning(f"JavaScript click failed: {js_error}")
                        time.sleep(1)  # Wait before retry
                else:
                    raise
                    
            except StaleElementReferenceException:
                logger.warning(f"Stale element on attempt {attempt + 1}, retrying: {locator}")
                if attempt == retries - 1:
                    raise
                time.sleep(0.5)
                
        return False
    
    def safe_send_keys(self, locator, text, clear_first=True, timeout=None):
        wait_time = timeout or self.timeout
        element = self.wait_for_element_visible(locator, wait_time)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        logger.debug(f"Sent keys to element: {locator}")
    
    def wait_and_get_text(self, locator, timeout=None):
        element = self.wait_for_element_visible(locator, timeout)
        text = element.text.strip()
        logger.debug(f"Got text from element {locator}: {text}")
        return text