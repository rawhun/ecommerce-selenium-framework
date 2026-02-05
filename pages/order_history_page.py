"""
Order history page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class OrderHistoryPage(BasePage):
    """Page object for order history page."""
    
    # Locators
    PAGE_HEADING = (By.CSS_SELECTOR, "#content h1")
    ORDER_ROWS = (By.CSS_SELECTOR, ".table-responsive tbody tr")
    ORDER_IDS = (By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(1)")
    ORDER_DATES = (By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(3)")
    ORDER_STATUSES = (By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(4)")
    ORDER_TOTALS = (By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(5)")
    VIEW_BUTTONS = (By.CSS_SELECTOR, "a[data-original-title='View']")
    NO_ORDERS_MESSAGE = (By.CSS_SELECTOR, "#content p")
    CONTINUE_BUTTON = (By.LINK_TEXT, "Continue")
    
    def __init__(self, driver):
        """Initialize order history page."""
        super().__init__(driver)
    
    def get_orders_count(self):
        """
        Get count of orders in history.
        
        Returns:
            int: Number of orders
        """
        try:
            elements = self.driver.find_elements(*self.ORDER_ROWS)
            count = len(elements)
            logger.info(f"Found {count} orders in history")
            return count
        except:
            return 0
    
    def get_order_ids(self):
        """
        Get list of order IDs.
        
        Returns:
            list: List of order IDs
        """
        elements = self.driver.find_elements(*self.ORDER_IDS)
        order_ids = [elem.text for elem in elements]
        logger.info(f"Order IDs: {order_ids}")
        return order_ids
    
    def get_order_statuses(self):
        """
        Get list of order statuses.
        
        Returns:
            list: List of order statuses
        """
        elements = self.driver.find_elements(*self.ORDER_STATUSES)
        statuses = [elem.text for elem in elements]
        logger.info(f"Order statuses: {statuses}")
        return statuses
    
    def get_order_totals(self):
        """
        Get list of order totals.
        
        Returns:
            list: List of order totals
        """
        elements = self.driver.find_elements(*self.ORDER_TOTALS)
        totals = [elem.text for elem in elements]
        logger.info(f"Order totals: {totals}")
        return totals
    
    def view_order(self, order_index=0):
        """
        View order details.
        
        Args:
            order_index (int): Index of order to view (0-based)
        """
        logger.info(f"Viewing order at index {order_index}")
        view_buttons = self.driver.find_elements(*self.VIEW_BUTTONS)
        
        if order_index < len(view_buttons):
            view_buttons[order_index].click()
    
    def has_orders(self):
        """
        Check if there are any orders in history.
        
        Returns:
            bool: True if orders exist
        """
        return self.get_orders_count() > 0
    
    def is_no_orders_message_displayed(self):
        """
        Check if no orders message is displayed.
        
        Returns:
            bool: True if no orders message is displayed
        """
        try:
            message = self.get_element_text(self.NO_ORDERS_MESSAGE)
            return "no orders" in message.lower() or "not made" in message.lower()
        except:
            return False
    
    def continue_to_account(self):
        """
        Continue back to account page.
        
        Returns:
            AccountPage: Account page object
        """
        logger.info("Continuing to account page")
        self.click_element(self.CONTINUE_BUTTON)
        
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    def is_page_loaded(self):
        """
        Check if order history page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.PAGE_HEADING, timeout=10)