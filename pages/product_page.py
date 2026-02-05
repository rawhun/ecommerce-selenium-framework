"""
Product page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class ProductPage(BasePage):
    """Page object for product detail page."""
    
    # Locators
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "h2")
    QUANTITY_INPUT = (By.ID, "input-quantity")
    ADD_TO_CART_BUTTON = (By.ID, "button-cart")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    PRODUCT_DESCRIPTION = (By.ID, "tab-description")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, ".thumbnail")
    WISHLIST_BUTTON = (By.CSS_SELECTOR, "button[onclick*='wishlist.add']")
    COMPARE_BUTTON = (By.CSS_SELECTOR, "button[onclick*='compare.add']")
    AVAILABILITY = (By.CSS_SELECTOR, "ul.list-unstyled li:nth-child(1)")
    
    def __init__(self, driver):
        """Initialize product page."""
        super().__init__(driver)
    
    def get_product_name(self):
        """
        Get product name.
        
        Returns:
            str: Product name
        """
        name = self.get_element_text(self.PRODUCT_NAME)
        logger.info(f"Product name: {name}")
        return name
    
    def get_product_price(self):
        """
        Get product price.
        
        Returns:
            str: Product price
        """
        price = self.get_element_text(self.PRODUCT_PRICE)
        logger.info(f"Product price: {price}")
        return price
    
    def set_quantity(self, quantity):
        """
        Set product quantity.
        
        Args:
            quantity (int): Quantity to set
        """
        logger.info(f"Setting quantity to: {quantity}")
        self.send_keys_to_element(self.QUANTITY_INPUT, str(quantity))
    
    def add_to_cart(self, quantity=1):
        """
        Add product to cart.
        
        Args:
            quantity (int): Quantity to add
            
        Returns:
            bool: True if product added successfully
        """
        logger.info(f"Adding product to cart with quantity: {quantity}")
        
        if quantity > 1:
            self.set_quantity(quantity)
        
        self.click_element(self.ADD_TO_CART_BUTTON)
        return self.is_success_message_displayed()
    
    def is_success_message_displayed(self):
        """
        Check if success message is displayed.
        
        Returns:
            bool: True if success message is displayed
        """
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
    
    def get_success_message(self):
        """
        Get success message text.
        
        Returns:
            str: Success message text
        """
        if self.is_success_message_displayed():
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return ""
    
    def add_to_wishlist(self):
        """Add product to wishlist."""
        logger.info("Adding product to wishlist")
        self.click_element(self.WISHLIST_BUTTON)
    
    def add_to_compare(self):
        """Add product to compare."""
        logger.info("Adding product to compare")
        self.click_element(self.COMPARE_BUTTON)
    
    def get_availability(self):
        """
        Get product availability status.
        
        Returns:
            str: Availability status
        """
        availability = self.get_element_text(self.AVAILABILITY)
        logger.info(f"Product availability: {availability}")
        return availability
    
    def is_page_loaded(self):
        """
        Check if product page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.PRODUCT_NAME, timeout=10)