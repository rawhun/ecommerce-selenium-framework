
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CartPage(BasePage):
    
    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".table-responsive tbody tr")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(2) a")
    PRODUCT_PRICES = (By.CSS_SELECTOR, ".table-responsive tbody tr td:nth-child(5)")
    QUANTITY_INPUTS = (By.CSS_SELECTOR, "input[name^='quantity']")
    UPDATE_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Update']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Remove']")
    CHECKOUT_BUTTON = (By.LINK_TEXT, "Checkout")
    CONTINUE_SHOPPING_BUTTON = (By.LINK_TEXT, "Continue Shopping")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".table-responsive tfoot tr:last-child td:last-child")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "#content p")
    COUPON_INPUT = (By.ID, "input-coupon")
    APPLY_COUPON_BUTTON = (By.ID, "button-coupon")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_cart_items_count(self):
        try:
            elements = self.driver.find_elements(*self.CART_ITEMS)
            count = len(elements)
            logger.info(f"Cart contains {count} items")
            return count
        except:
            return 0
    
    def get_product_names(self):
        elements = self.driver.find_elements(*self.PRODUCT_NAMES)
        names = [elem.text for elem in elements]
        logger.info(f"Products in cart: {names}")
        return names
    
    def is_product_in_cart(self, product_name):
        product_names = self.get_product_names()
        return product_name in product_names
    
    def update_quantity(self, product_index, quantity):
        logger.info(f"Updating quantity for product {product_index} to {quantity}")
        quantity_inputs = self.driver.find_elements(*self.QUANTITY_INPUTS)
        update_buttons = self.driver.find_elements(*self.UPDATE_BUTTONS)
        
        if product_index < len(quantity_inputs):
            quantity_inputs[product_index].clear()
            quantity_inputs[product_index].send_keys(str(quantity))
            update_buttons[product_index].click()
    
    def remove_product(self, product_index):
        logger.info(f"Removing product at index {product_index}")
        remove_buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
        
        if product_index < len(remove_buttons):
            remove_buttons[product_index].click()
    
    def remove_all_products(self):
        logger.info("Removing all products from cart")
        while self.get_cart_items_count() > 0:
            self.remove_product(0)
    
    def get_total_price(self):
        price = self.get_element_text(self.TOTAL_PRICE)
        logger.info(f"Total cart price: {price}")
        return price
    
    def proceed_to_checkout(self):
        logger.info("Proceeding to checkout")
        self.click_element(self.CHECKOUT_BUTTON)
        
        from .checkout_page import CheckoutPage
        return CheckoutPage(self.driver)
    
    def continue_shopping(self):
        logger.info("Continuing shopping")
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
        
        from .home_page import HomePage
        return HomePage(self.driver)
    
    def is_cart_empty(self):
        try:
            message = self.get_element_text(self.EMPTY_CART_MESSAGE)
            return "empty" in message.lower()
        except:
            return self.get_cart_items_count() == 0
    
    def apply_coupon(self, coupon_code):
        logger.info(f"Applying coupon: {coupon_code}")
        self.send_keys_to_element(self.COUPON_INPUT, coupon_code)
        self.click_element(self.APPLY_COUPON_BUTTON)
    
    def is_page_loaded(self):
        return self.is_element_present(self.CART_ITEMS, timeout=10) or \
               self.is_element_present(self.EMPTY_CART_MESSAGE, timeout=10)