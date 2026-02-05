"""
Search results page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SearchResultsPage(BasePage):
    """Page object for search results page."""
    
    # Locators
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-layout")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-layout h4 a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".product-layout .price")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[onclick*='cart.add']")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "#content p")
    SORT_DROPDOWN = (By.ID, "input-sort")
    LIMIT_DROPDOWN = (By.ID, "input-limit")
    GRID_VIEW_BUTTON = (By.ID, "grid-view")
    LIST_VIEW_BUTTON = (By.ID, "list-view")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def __init__(self, driver):
        """Initialize search results page."""
        super().__init__(driver)
    
    def get_product_count(self):
        """
        Get count of products in search results.
        
        Returns:
            int: Number of products found
        """
        elements = self.driver.find_elements(*self.PRODUCT_ITEMS)
        count = len(elements)
        logger.info(f"Found {count} products in search results")
        return count
    
    def get_product_names(self):
        """
        Get list of product names.
        
        Returns:
            list: List of product names
        """
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        names = [elem.text for elem in elements]
        logger.info(f"Product names: {names}")
        return names
    
    def click_product_by_name(self, product_name):
        """
        Click on a product by its name.
        
        Args:
            product_name (str): Name of the product to click
            
        Returns:
            ProductPage: Product page object
        """
        logger.info(f"Clicking product: {product_name}")
        product_locator = (By.LINK_TEXT, product_name)
        self.click_element(product_locator)
        
        from .product_page import ProductPage
        return ProductPage(self.driver)
    
    def click_first_product(self):
        """
        Click on the first product in results.
        
        Returns:
            ProductPage: Product page object
        """
        logger.info("Clicking first product")
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        if elements:
            elements[0].click()
            from .product_page import ProductPage
            return ProductPage(self.driver)
        else:
            raise Exception("No products found in search results")
    
    def add_first_product_to_cart(self):
        """
        Add first product to cart from search results.
        
        Returns:
            bool: True if product added successfully
        """
        logger.info("Adding first product to cart")
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()
            return self.is_success_message_displayed()
        return False
    
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
    
    def is_no_results_displayed(self):
        """
        Check if no results message is displayed.
        
        Returns:
            bool: True if no results message is displayed
        """
        try:
            message = self.get_element_text(self.NO_RESULTS_MESSAGE)
            return "no product" in message.lower()
        except:
            return False
    
    def sort_by(self, sort_option):
        """
        Sort products by option.
        
        Args:
            sort_option (str): Sort option text
        """
        logger.info(f"Sorting by: {sort_option}")
        self.select_dropdown_by_text(self.SORT_DROPDOWN, sort_option)
    
    def is_page_loaded(self):
        """
        Check if search results page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_present(self.PRODUCT_ITEMS, timeout=10) or \
               self.is_element_present(self.NO_RESULTS_MESSAGE, timeout=10)