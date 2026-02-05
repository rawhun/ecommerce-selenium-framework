
import pytest
from datetime import datetime
from pages.home_page import HomePage
from utils.logger import log_test_start, log_test_end


@pytest.mark.smoke
@pytest.mark.critical
class TestE2EFlows:
    
    def test_complete_purchase_flow_guest(self, driver, test_data):
        log_test_start("test_complete_purchase_flow_guest")
        
        # Step 1: Search for product
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        assert search_results.get_product_count() > 0, "Should find products"
        
        # Step 2: View product details
        product_page = search_results.click_first_product()
        product_name = product_page.get_product_name()
        assert len(product_name) > 0, "Product name should be displayed"
        
        # Step 3: Add to cart
        assert product_page.add_to_cart(), "Product should be added to cart"
        
        # Step 4: View cart
        cart_page = home_page.go_to_shopping_cart()
        assert cart_page.get_cart_items_count() > 0, "Cart should have items"
        assert cart_page.is_product_in_cart(product_name), \
            f"Cart should contain '{product_name}'"
        
        # Step 5: Proceed to checkout
        checkout_page = cart_page.proceed_to_checkout()
        assert "checkout" in checkout_page.get_current_url().lower(), \
            "Should be on checkout page"
        
        log_test_end("test_complete_purchase_flow_guest", "PASSED")
    
    def test_login_search_add_to_cart_logout(self, driver, test_data):
        log_test_start("test_login_search_add_to_cart_logout")
        
        # Step 1: Login
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        assert account_page.is_logged_in(), "User should be logged in"
        
        # Step 2: Search for product
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][1]
        search_results = home_page.search_product(search_term)
        
        # Step 3: Add product to cart
        product_page = search_results.click_first_product()
        product_name = product_page.get_product_name()
        assert product_page.add_to_cart(), "Product should be added to cart"
        
        # Step 4: Verify cart
        cart_page = home_page.go_to_shopping_cart()
        assert cart_page.is_product_in_cart(product_name), \
            "Cart should contain the product"
        
        # Step 5: Logout
        home_page = HomePage(driver)
        home_page.logout()
        assert not home_page.is_user_logged_in(), "User should be logged out"
        
        log_test_end("test_login_search_add_to_cart_logout", "PASSED")
    
    def test_login_update_profile_view_orders(self, driver, test_data):
        log_test_start("test_login_update_profile_view_orders")
        
        # Step 1: Login
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        assert account_page.is_logged_in(), "User should be logged in"
        
        # Step 2: Update profile
        edit_account_page = account_page.go_to_edit_account()
        new_telephone = f"555{datetime.now().strftime('%H%M%S')}"
        account_page = edit_account_page.update_account(telephone=new_telephone)
        assert account_page.is_success_message_displayed(), \
            "Profile update should be successful"
        
        # Step 3: View order history
        order_history_page = account_page.go_to_order_history()
        assert order_history_page.is_page_loaded(), \
            "Order history page should be loaded"
        
        # Verify either orders exist or no orders message
        assert order_history_page.has_orders() or \
               order_history_page.is_no_orders_message_displayed(), \
               "Should show orders or no orders message"
        
        log_test_end("test_login_update_profile_view_orders", "PASSED")
    
    def test_search_multiple_products_add_to_cart(self, driver, test_data):
        log_test_start("test_search_multiple_products_add_to_cart")
        
        home_page = HomePage(driver)
        search_terms = test_data['products']['search_terms']['valid'][:2]
        added_products = []
        
        # Add multiple products
        for search_term in search_terms:
            search_results = home_page.search_product(search_term)
            if search_results.get_product_count() > 0:
                product_page = search_results.click_first_product()
                product_name = product_page.get_product_name()
                product_page.add_to_cart()
                added_products.append(product_name)
                home_page = HomePage(driver)
        
        # Verify all products in cart
        cart_page = home_page.go_to_shopping_cart()
        assert cart_page.get_cart_items_count() >= len(added_products), \
            "Cart should contain all added products"
        
        for product_name in added_products:
            assert cart_page.is_product_in_cart(product_name), \
                f"Cart should contain '{product_name}'"
        
        log_test_end("test_search_multiple_products_add_to_cart", "PASSED")