
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class SearchResultsPage(BasePage):
    
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
        super().__init__(driver)
    
    def get_product_count(self):
        elements = self.driver.find_elements(*self.PRODUCT_ITEMS)
        count = len(elements)
        logger.info(f"Found {count} products in search results")
        return count
    
    def get_product_names(self):
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        names = [elem.text for elem in elements]
        logger.info(f"Product names: {names}")
        return names
    
    def click_product_by_name(self, product_name):
        logger.info(f"Clicking product: {product_name}")
        product_locator = (By.LINK_TEXT, product_name)
        self.click_element(product_locator)
        
        from .product_page import ProductPage
        return ProductPage(self.driver)
    
    def click_first_product(self):
        logger.info("Clicking first product")
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        if elements:
            elements[0].click()
            from .product_page import ProductPage
            return ProductPage(self.driver)
        else:
            raise Exception("No products found in search results")
    
    def add_first_product_to_cart(self):
        logger.info("Adding first product to cart")
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        if buttons:
            buttons[0].click()
            return self.is_success_message_displayed()
        return False
    
    def is_success_message_displayed(self):
        return self.is_element_visible(self.SUCCESS_MESSAGE, timeout=5)
    
    def get_success_message(self):
        if self.is_success_message_displayed():
            return self.get_element_text(self.SUCCESS_MESSAGE)
        return ""
    
    def is_no_results_displayed(self):
        try:
            message = self.get_element_text(self.NO_RESULTS_MESSAGE)
            return "no product" in message.lower()
        except:
            return False
    
    def sort_by(self, sort_option):
        logger.info(f"Sorting by: {sort_option}")
        self.select_dropdown_by_text(self.SORT_DROPDOWN, sort_option)
    
    def is_page_loaded(self):
        return self.is_element_present(self.PRODUCT_ITEMS, timeout=10) or \
               self.is_element_present(self.NO_RESULTS_MESSAGE, timeout=10)