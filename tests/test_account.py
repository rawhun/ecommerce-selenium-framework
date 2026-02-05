
import pytest
from datetime import datetime
from pages.home_page import HomePage
from utils.logger import log_test_start, log_test_end


class TestAccount:
    
    def test_update_account_information(self, driver, test_data):
        log_test_start("test_update_account_information")
        
        # Login
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        
        # Go to edit account
        edit_account_page = account_page.go_to_edit_account()
        
        # Update telephone
        new_telephone = "9999999999"
        account_page = edit_account_page.update_account(telephone=new_telephone)
        
        # Verify success message
        assert account_page.is_success_message_displayed(), \
            "Success message should be displayed"
        
        log_test_end("test_update_account_information", "PASSED")
    
    def test_view_order_history(self, driver, test_data):
        log_test_start("test_view_order_history")
        
        # Login
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        
        # Go to order history
        order_history_page = account_page.go_to_order_history()
        
        # Verify page loaded
        assert order_history_page.is_page_loaded(), \
            "Order history page should be loaded"
        
        # Check if orders exist or no orders message displayed
        has_orders = order_history_page.has_orders()
        no_orders_msg = order_history_page.is_no_orders_message_displayed()
        
        assert has_orders or no_orders_msg, \
            "Should either have orders or display no orders message"
        
        log_test_end("test_view_order_history", "PASSED")
    
    def test_account_navigation(self, driver, test_data):
        log_test_start("test_account_navigation")
        
        # Login
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        
        # Verify account page loaded
        assert account_page.is_logged_in(), "User should be logged in"
        
        # Navigate to edit account
        edit_account_page = account_page.go_to_edit_account()
        assert edit_account_page.is_page_loaded(), \
            "Edit account page should be loaded"
        
        # Navigate back to account
        driver.back()
        account_page = HomePage(driver).go_to_my_account()
        
        # Navigate to order history
        order_history_page = account_page.go_to_order_history()
        assert order_history_page.is_page_loaded(), \
            "Order history page should be loaded"
        
        log_test_end("test_account_navigation", "PASSED")