"""
Login page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Page object for login page."""
    
    # Locators
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    FORGOTTEN_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten Password")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    CONTINUE_BUTTON = (By.LINK_TEXT, "Continue")
    
    def __init__(self, driver):
        """Initialize login page."""
        super().__init__(driver)
    
    def login(self, email, password):
        """
        Perform login with credentials.
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            AccountPage: Account page object after successful login
        """
        logger.info(f"Logging in with email: {email}")
        self.send_keys_to_element(self.EMAIL_INPUT, email)
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    def get_error_message(self):
        """
        Get error message text.
        
        Returns:
            str: Error message text
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self):
        """
        Check if error message is displayed.
        
        Returns:
            bool: True if error is displayed
        """
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
    
    def click_forgotten_password(self):
        """Click forgotten password link."""
        logger.info("Clicking forgotten password link")
        self.click_element(self.FORGOTTEN_PASSWORD_LINK)
    
    def go_to_register(self):
        """
        Navigate to registration page.
        
        Returns:
            RegisterPage: Registration page object
        """
        logger.info("Navigating to registration page")
        self.click_element(self.CONTINUE_BUTTON)
        
        from .register_page import RegisterPage
        return RegisterPage(self.driver)
    
    def is_page_loaded(self):
        """
        Check if login page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.EMAIL_INPUT, timeout=10)