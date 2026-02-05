"""
Home page object for e-commerce site.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class HomePage(BasePage):
    """Page object for home page."""
    
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
        """Initialize home page."""
        super().__init__(driver)
        self.navigate_to("/")
    
    def search_product(self, product_name):
        """
        Search for a product.
        
        Args:
            product_name (str): Product name to search
            
        Returns:
            SearchResultsPage: Search results page object
        """
        logger.info(f"Searching for product: {product_name}")
        self.send_keys_to_element(self.SEARCH_INPUT, product_name)
        self.click_element(self.SEARCH_BUTTON)
        
        from .search_results_page import SearchResultsPage
        return SearchResultsPage(self.driver)
    
    def click_my_account(self):
        """Click My Account dropdown."""
        logger.info("Clicking My Account dropdown")
        self.click_element(self.MY_ACCOUNT_DROPDOWN)
    
    def go_to_login(self):
        """
        Navigate to login page.
        
        Returns:
            LoginPage: Login page object
        """
        logger.info("Navigating to login page")
        self.click_my_account()
        self.click_element(self.LOGIN_LINK)
        
        from .login_page import LoginPage
        return LoginPage(self.driver)
    
    def go_to_register(self):
        """
        Navigate to registration page.
        
        Returns:
            RegisterPage: Registration page object
        """
        logger.info("Navigating to registration page")
        self.click_my_account()
        self.click_element(self.REGISTER_LINK)
        
        from .register_page import RegisterPage
        return RegisterPage(self.driver)
    
    def go_to_shopping_cart(self):
        """
        Navigate to shopping cart.
        
        Returns:
            CartPage: Cart page object
        """
        logger.info("Navigating to shopping cart")
        self.click_element(self.SHOPPING_CART_LINK)
        
        from .cart_page import CartPage
        return CartPage(self.driver)
    
    def go_to_my_account(self):
        """
        Navigate to account page.
        
        Returns:
            AccountPage: Account page object
        """
        logger.info("Navigating to My Account page")
        self.click_my_account()
        self.click_element(self.ACCOUNT_LINK)
        
        from .account_page import AccountPage
        return AccountPage(self.driver)
    
    def logout(self):
        """
        Logout from the application.
        
        Returns:
            HomePage: Home page object after logout
        """
        logger.info("Logging out")
        self.click_my_account()
        self.click_element(self.LOGOUT_LINK)
        return HomePage(self.driver)
    
    def is_user_logged_in(self):
        """
        Check if user is logged in.
        
        Returns:
            bool: True if user is logged in
        """
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
        """
        Get count of featured products on home page.
        
        Returns:
            int: Number of featured products
        """
        elements = self.driver.find_elements(*self.FEATURED_PRODUCTS)
        count = len(elements)
        logger.info(f"Found {count} featured products")
        return count
    
    def is_page_loaded(self):
        """
        Check if home page is loaded.
        
        Returns:
            bool: True if page is loaded
        """
        return self.is_element_visible(self.LOGO, timeout=10)