"""
Test cases for login functionality.
"""

import pytest
from pages.home_page import HomePage
from utils.logger import log_test_start, log_test_end


@pytest.mark.smoke
@pytest.mark.critical
class TestLogin:
    """Test suite for login functionality."""
    
    def test_valid_login(self, driver, test_data):
        """Test login with valid credentials."""
        log_test_start("test_valid_login")
        
        # Navigate to home page and go to login
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        
        # Perform login
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        
        # Verify login successful
        assert account_page.is_logged_in(), "User should be logged in"
        
        log_test_end("test_valid_login", "PASSED")
    
    def test_invalid_login(self, driver, test_data):
        """Test login with invalid credentials."""
        log_test_start("test_invalid_login")
        
        # Navigate to login page
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        
        # Attempt login with invalid credentials
        user = test_data['users']['invalid_user']
        login_page.login(user['email'], user['password'])
        
        # Verify error message displayed
        assert login_page.is_error_displayed(), "Error message should be displayed"
        error_message = login_page.get_error_message()
        assert "warning" in error_message.lower() or "no match" in error_message.lower()
        
        log_test_end("test_invalid_login", "PASSED")
    
    def test_login_with_empty_credentials(self, driver):
        """Test login with empty credentials."""
        log_test_start("test_login_with_empty_credentials")
        
        # Navigate to login page
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        
        # Attempt login with empty credentials
        login_page.login("", "")
        
        # Verify error message displayed
        assert login_page.is_error_displayed(), "Error message should be displayed"
        
        log_test_end("test_login_with_empty_credentials", "PASSED")
    
    @pytest.mark.smoke
    def test_logout(self, driver, test_data):
        """Test logout functionality."""
        log_test_start("test_logout")
        
        # Login first
        home_page = HomePage(driver)
        login_page = home_page.go_to_login()
        user = test_data['users']['valid_user']
        account_page = login_page.login(user['email'], user['password'])
        
        # Verify logged in
        assert account_page.is_logged_in(), "User should be logged in"
        
        # Logout
        account_page.logout()
        
        # Verify logged out
        home_page = HomePage(driver)
        assert not home_page.is_user_logged_in(), "User should be logged out"
        
        log_test_end("test_logout", "PASSED")