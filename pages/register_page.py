
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class RegisterPage(BasePage):
    
    # Locators
    FIRST_NAME_INPUT = (By.ID, "input-firstname")
    LAST_NAME_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    TELEPHONE_INPUT = (By.ID, "input-telephone")
    PASSWORD_INPUT = (By.ID, "input-password")
    PASSWORD_CONFIRM_INPUT = (By.ID, "input-confirm")
    PRIVACY_POLICY_CHECKBOX = (By.NAME, "agree")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "input[value='Continue']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content h1")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    NEWSLETTER_YES_RADIO = (By.CSS_SELECTOR, "input[name='newsletter'][value='1']")
    NEWSLETTER_NO_RADIO = (By.CSS_SELECTOR, "input[name='newsletter'][value='0']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def register(self, first_name, last_name, email, telephone, password, 
                 subscribe_newsletter=False):
        logger.info(f"Registering new user: {email}")
        
        self.send_keys_to_element(self.FIRST_NAME_INPUT, first_name)
        self.send_keys_to_element(self.LAST_NAME_INPUT, last_name)
        self.send_keys_to_element(self.EMAIL_INPUT, email)
        self.send_keys_to_element(self.TELEPHONE_INPUT, telephone)
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
        self.send_keys_to_element(self.PASSWORD_CONFIRM_INPUT, password)
        
        if subscribe_newsletter:
            self.click_element(self.NEWSLETTER_YES_RADIO)
        else:
            self.click_element(self.NEWSLETTER_NO_RADIO)
        
        self.click_element(self.PRIVACY_POLICY_CHECKBOX)
        self.click_element(self.CONTINUE_BUTTON)
        
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    def get_success_message(self):
        if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return ""
    
    def get_error_message(self):
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""
    
    def is_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=5)
    
    def is_page_loaded(self):
        return self.is_element_visible(self.FIRST_NAME_INPUT, timeout=10)