"""
Test cases for shopping cart functionality.
"""

import pytest
from pages.home_page import HomePage
from utils.logger import log_test_start, log_test_end


@pytest.mark.smoke
class TestShoppingCart:
    """Test suite for shopping cart functionality."""
    
    def test_add_product_to_cart(self, driver, test_data):
        """Test adding a product to cart."""
        log_test_start("test_add_product_to_cart")
        
        # Search and add product to cart
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        
        product_page = search_results.click_first_product()
        product_name = product_page.get_product_name()
        
        # Add to cart
        assert product_page.add_to_cart(), "Product should be added to cart"
        
        # Verify in cart
        cart_page = home_page.go_to_shopping_cart()
        assert cart_page.get_cart_items_count() > 0, "Cart should contain items"
        assert cart_page.is_product_in_cart(product_name), \
            f"Cart should contain '{product_name}'"
        
        log_test_end("test_add_product_to_cart", "PASSED")
    
    def test_add_multiple_products_to_cart(self, driver, test_data):
        """Test adding multiple products to cart."""
        log_test_start("test_add_multiple_products_to_cart")
        
        home_page = HomePage(driver)
        search_terms = test_data['products']['search_terms']['valid'][:2]
        
        for search_term in search_terms:
            # Search and add product
            search_results = home_page.search_product(search_term)
            product_page = search_results.click_first_product()
            product_page.add_to_cart()
            
            # Navigate back to home
            home_page = HomePage(driver)
        
        # Verify cart has multiple items
        cart_page = home_page.go_to_shopping_cart()
        assert cart_page.get_cart_items_count() >= 2, \
            "Cart should contain at least 2 items"
        
        log_test_end("test_add_multiple_products_to_cart", "PASSED")
    
    def test_update_cart_quantity(self, driver, test_data):
        """Test updating product quantity in cart."""
        log_test_start("test_update_cart_quantity")
        
        # Add product to cart
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        product_page = search_results.click_first_product()
        product_page.add_to_cart()
        
        # Go to cart and update quantity
        cart_page = home_page.go_to_shopping_cart()
        initial_count = cart_page.get_cart_items_count()
        
        # Update quantity
        cart_page.update_quantity(0, 2)
        
        # Verify quantity updated (cart should still have same number of items)
        assert cart_page.get_cart_items_count() == initial_count, \
            "Cart should have same number of items after quantity update"
        
        log_test_end("test_update_cart_quantity", "PASSED")
    
    def test_remove_product_from_cart(self, driver, test_data):
        """Test removing a product from cart."""
        log_test_start("test_remove_product_from_cart")
        
        # Add product to cart
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        product_page = search_results.click_first_product()
        product_page.add_to_cart()
        
        # Go to cart and remove product
        cart_page = home_page.go_to_shopping_cart()
        initial_count = cart_page.get_cart_items_count()
        assert initial_count > 0, "Cart should have items"
        
        cart_page.remove_product(0)
        
        # Verify product removed
        final_count = cart_page.get_cart_items_count()
        assert final_count == initial_count - 1, "Cart should have one less item"
        
        log_test_end("test_remove_product_from_cart", "PASSED")
    
    def test_cart_total_price(self, driver, test_data):
        """Test cart displays total price."""
        log_test_start("test_cart_total_price")
        
        # Add product to cart
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        product_page = search_results.click_first_product()
        product_page.add_to_cart()
        
        # Verify total price displayed
        cart_page = home_page.go_to_shopping_cart()
        total_price = cart_page.get_total_price()
        assert len(total_price) > 0, "Total price should be displayed"
        assert "$" in total_price or "£" in total_price or "€" in total_price, \
            "Total price should contain currency symbol"
        
        log_test_end("test_cart_total_price", "PASSED")