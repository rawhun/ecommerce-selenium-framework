"""
Edit account page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class EditAccountPage(BasePage):
    """Page object for edit account page."""
    
    # Locators
    FIRST_NAME_INPUT = (By.ID, "input-firstname")
    LAST_NAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    TELEPHONE_INPUT = (By.ID, "input-telephone")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[value='Continue']")
    BACK_BUTTON = (By.LINK_TEXT, "Back")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def __init__(self, driver):
        """Initialize edit account page."""
        super().__init__(driver)
    
    def update_account(self, first_name=None, last_name=None, email=None, telephone=None):
        """
        Update account information.
        
        Args:
            first_name (str): New first name (optional)
            last_name (str): New last name (optional)
            email (str): New email (optional)
            telephone (str): New telephone (optional)
            
        Returns:
            AccountPage: Account page object after update
        """
        logger.info("Updating account information")
        
        if first_name:
            self.send_keys_to_element(self.FIRST_NAME_INPUT, first_name)
        
        if last_name:
            self.send_keys_to_element(self.LAST_NAME_INPUT, last_name)
        
        if email:
            self.send_keys_to_element(self.EMAIL_INPUT, email)
        
        if telephone:
            self.send_keys_to_element(self.TELEPHONE_INPUT, telephone)
        
        self.click_element(self.CONTINUE_BUTTON)
        
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    def get_current_first_name(self):
        """Get current first name value."""
        return self.get_element_attribute(self.FIRST_NAME_INPUT, "value")
    
    def get_current_last_name(self):
        """Get current last name value."""
        return self.get_element_attribute(self.LAST_NAME_INPUT, "value")
    
    def get_current_email(self):
        """Get current email value."""
        return self.get_element_attribute(self.EMAIL_INPUT, "value")
    
    def get_current_telephone(self):
        """Get current telephone value."""
        return self.get_element_attribute(self.TELEPHONE_INPUT, "value")
    
    def is_page_loaded(self):
        """
        Check if edit account page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.FIRST_NAME_INPUT, timeout=10)