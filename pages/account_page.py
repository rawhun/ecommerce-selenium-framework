"""
Account page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class AccountPage(BasePage):
    """Page object for account/dashboard page."""
    
    # Locators
    PAGE_HEADING = (By.CSS_SELECTOR, "#content h2")
    EDIT_ACCOUNT_LINK = (By.LINK_TEXT, "Edit Account")
    CHANGE_PASSWORD_LINK = (By.LINK_TEXT, "Password")
    ADDRESS_BOOK_LINK = (By.LINK_TEXT, "Address Book")
    WISHLIST_LINK = (By.LINK_TEXT, "Wish List")
    ORDER_HISTORY_LINK = (By.LINK_TEXT, "Order History")
    DOWNLOADS_LINK = (By.LINK_TEXT, "Downloads")
    RECURRING_PAYMENTS_LINK = (By.LINK_TEXT, "Recurring payments")
    REWARD_POINTS_LINK = (By.LINK_TEXT, "Reward Points")
    RETURNS_LINK = (By.LINK_TEXT, "Returns")
    TRANSACTIONS_LINK = (By.LINK_TEXT, "Transactions")
    NEWSLETTER_LINK = (By.LINK_TEXT, "Newsletter")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def __init__(self, driver):
        """Initialize account page."""
        super().__init__(driver)
    
    def is_logged_in(self):
        """
        Check if user is logged in by verifying account page elements.
        
        Returns:
            bool: True if user is logged in
        """
        return self.is_element_visible(self.EDIT_ACCOUNT_LINK, timeout=10)
    
    def go_to_edit_account(self):
        """
        Navigate to edit account page.
        
        Returns:
            EditAccountPage: Edit account page object
        """
        logger.info("Navigating to edit account page")
        self.click_element(self.EDIT_ACCOUNT_LINK)
        
        from .edit_account_page import EditAccountPage
        return EditAccountPage(self.driver)
    
    def go_to_order_history(self):
        """
        Navigate to order history page.
        
        Returns:
            OrderHistoryPage: Order history page object
        """
        logger.info("Navigating to order history page")
        self.click_element(self.ORDER_HISTORY_LINK)
        
        from .order_history_page import OrderHistoryPage
        return OrderHistoryPage(self.driver)
    
    def go_to_address_book(self):
        """Navigate to address book page."""
        logger.info("Navigating to address book")
        self.click_element(self.ADDRESS_BOOK_LINK)
    
    def go_to_wishlist(self):
        """Navigate to wishlist page."""
        logger.info("Navigating to wishlist")
        self.click_element(self.WISHLIST_LINK)
    
    def go_to_change_password(self):
        """Navigate to change password page."""
        logger.info("Navigating to change password")
        self.click_element(self.CHANGE_PASSWORD_LINK)
    
    def logout(self):
        """
        Logout from account.
        
        Returns:
            HomePage: Home page object after logout
        """
        logger.info("Logging out from account page")
        self.click_element(self.LOGOUT_LINK)
        
        from .home_page import HomePage
        return HomePage(self.driver)
    
    def get_success_message(self):
        """
        Get success message text.
        
        Returns:
            str: Success message text
        """
        if self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5):
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return ""
    
    def is_success_message_displayed(self):
        """
        Check if success message is displayed.
        
        Returns:
            bool: True if success message is displayed
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
    
    def is_page_loaded(self):
        """
        Check if account page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.EDIT_ACCOUNT_LINK, timeout=10)