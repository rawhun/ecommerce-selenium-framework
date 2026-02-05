
import pytest
from pages.home_page import HomePage
from utils.logger import log_test_start, log_test_end


@pytest.mark.smoke
class TestProductSearch:
    
    def test_search_valid_product(self, driver, test_data):
        log_test_start("test_search_valid_product")
        
        # Navigate to home page
        home_page = HomePage(driver)
        
        # Search for product
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        
        # Verify search results
        assert search_results.get_product_count() > 0, "Search should return products"
        product_names = search_results.get_product_names()
        assert any(search_term.lower() in name.lower() for name in product_names), \
            f"Search results should contain '{search_term}'"
        
        log_test_end("test_search_valid_product", "PASSED")
    
    def test_search_invalid_product(self, driver, test_data):
        log_test_start("test_search_invalid_product")
        
        # Navigate to home page
        home_page = HomePage(driver)
        
        # Search for invalid product
        search_term = test_data['products']['search_terms']['invalid'][0]
        search_results = home_page.search_product(search_term)
        
        # Verify no results
        assert search_results.is_no_results_displayed() or \
               search_results.get_product_count() == 0, \
               "Search should return no results for invalid product"
        
        log_test_end("test_search_invalid_product", "PASSED")
    
    def test_search_multiple_products(self, driver, test_data):
        log_test_start("test_search_multiple_products")
        
        home_page = HomePage(driver)
        search_terms = test_data['products']['search_terms']['valid'][:3]
        
        for search_term in search_terms:
            # Search for product
            search_results = home_page.search_product(search_term)
            
            # Verify results
            assert search_results.get_product_count() > 0, \
                f"Search for '{search_term}' should return products"
            
            # Navigate back to home
            home_page = HomePage(driver)
        
        log_test_end("test_search_multiple_products", "PASSED")
    
    def test_view_product_details(self, driver, test_data):
        log_test_start("test_view_product_details")
        
        # Search for product
        home_page = HomePage(driver)
        search_term = test_data['products']['search_terms']['valid'][0]
        search_results = home_page.search_product(search_term)
        
        # Click on first product
        product_page = search_results.click_first_product()
        
        # Verify product page loaded
        assert product_page.is_page_loaded(), "Product page should be loaded"
        product_name = product_page.get_product_name()
        assert len(product_name) > 0, "Product name should be displayed"
        
        log_test_end("test_view_product_details", "PASSED")