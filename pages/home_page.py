
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    
    # Locators
    LOGO = (By.CSS_SELECTOR, "#logo a")
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.btn-default")
    MY_ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, "a[title='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    SHOPPING_CART_LINK = (By.CSS_SELECTOR, "a[title='Shopping Cart']")
    CHECKOUT_LINK = (By.LINK_TEXT, "Checkout")
    FEATURED_PRODUCTS = (By.CSS_SELECTOR, ".product-layout")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "button.dropdown-toggle")
    ACCOUNT_LINK = (By.LINK_TEXT, "My Account")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.navigate_to("/")
    
    def search_product(self, product_name):
        logger.info(f"Searching for product: {product_name}")
        self.send_keys_to_element(self.SEARCH_INPUT, product_name)
        self.click_element(self.SEARCH_BUTTON)
        
        from .search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver)
    
    def click_my_account(self):
        logger.info("Clicking My Account dropdown")
        self.click_element(self.MY_ACCOUNT_DROPDOWN)
    
    def go_to_login(self):
        logger.info("Navigating to login page")
        self.click_my_account()
        self.click_element(self.LOGIN_LINK)
        
        from .login_page import LoginPage
        return LoginPage(self.driver)
    
    def go_to_register(self):
        logger.info("Navigating to registration page")
        self.click_my_account()
        self.click_element(self.REGISTER_LINK)
        
        from .register_page import RegisterPage
        return RegisterPage(self.driver)
    
    def go_to_shopping_cart(self):
        logger.info("Navigating to shopping cart")
        self.click_element(self.SHOPPING_CART_LINK)
        
        from .cart_page import CartPage
        return CartPage(self.driver)
    
    def go_to_my_account(self):
        logger.info("Navigating to My Account page")
        self.click_my_account()
        self.click_element(self.ACCOUNT_LINK)
        
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    def logout(self):
        logger.info("Logging out")
        self.click_my_account()
        self.click_element(self.LOGOUT_LINK)
        return HomePage(self.driver)
    
    def is_user_logged_in(self):
        try:
            self.click_my_account()
            is_logged_in = self.is_element_visible(self.LOGOUT_LINK, timeout=3)
            # Click again to close dropdown
            self.click_my_account()
            return is_logged_in
        except Exception as e:
            logger.error(f"Error checking login status: {e}")
            return False
    
    def get_featured_products_count(self):
        elements = self.driver.find_elements(*self.FEATURED_PRODUCTS)
        count = len(elements)
        logger.info(f"Found {count} featured products")
        return count
    
    def is_page_loaded(self):
        return self.is_element_visible(self.LOGO, timeout=10)