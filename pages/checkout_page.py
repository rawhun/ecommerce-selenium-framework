
from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CheckoutPage(BasePage):
    
    # Locators - Step 1: Checkout Options
    GUEST_CHECKOUT_RADIO = (By.CSS_SELECTOR, "input[value='guest']")
    REGISTER_RADIO = (By.CSS_SELECTOR, "input[value='register']")
    RETURNING_CUSTOMER_RADIO = (By.CSS_SELECTOR, "input[value='returning']")
    CHECKOUT_OPTION_CONTINUE = (By.ID, "button-account")
    
    # Locators - Step 2: Billing Details
    FIRST_NAME_INPUT = (By.ID, "input-payment-firstname")
    LAST_NAME_INPUT = (By.ID, "input-payment-lastname")
    EMAIL_INPUT = (By.ID, "input-payment-email")
    TELEPHONE_INPUT = (By.ID, "input-payment-telephone")
    ADDRESS_INPUT = (By.ID, "input-payment-address-1")
    CITY_INPUT = (By.ID, "input-payment-city")
    POSTCODE_INPUT = (By.ID, "input-payment-postcode")
    COUNTRY_DROPDOWN = (By.ID, "input-payment-country")
    REGION_DROPDOWN = (By.ID, "input-payment-zone")
    BILLING_CONTINUE = (By.ID, "button-guest")
    
    # Locators - Step 3: Delivery Details
    DELIVERY_CONTINUE = (By.ID, "button-shipping-address")
    
    # Locators - Step 4: Delivery Method
    DELIVERY_METHOD_CONTINUE = (By.ID, "button-shipping-method")
    
    # Locators - Step 5: Payment Method
    TERMS_CHECKBOX = (By.NAME, "agree")
    PAYMENT_METHOD_CONTINUE = (By.ID, "button-payment-method")
    
    # Locators - Step 6: Confirm Order
    CONFIRM_ORDER_BUTTON = (By.ID, "button-confirm")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content h1")
    ORDER_NUMBER = (By.CSS_SELECTOR, "#content p:nth-child(2)")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def select_guest_checkout(self):
        logger.info("Selecting guest checkout")
        if self.is_element_present(self.GUEST_CHECKOUT_RADIO, timeout=5):
            self.click_element(self.GUEST_CHECKOUT_RADIO)
            self.click_element(self.CHECKOUT_OPTION_CONTINUE)
    
    def fill_billing_details(self, first_name, last_name, email, telephone, 
                            address, city, postcode, country="United States", 
                            region="California"):
        logger.info(f"Filling billing details for: {email}")
        
        self.send_keys_to_element(self.FIRST_NAME_INPUT, first_name)
        self.send_keys_to_element(self.LAST_NAME_INPUT, last_name)
        self.send_keys_to_element(self.EMAIL_INPUT, email)
        self.send_keys_to_element(self.TELEPHONE_INPUT, telephone)
        self.send_keys_to_element(self.ADDRESS_INPUT, address)
        self.send_keys_to_element(self.CITY_INPUT, city)
        self.send_keys_to_element(self.POSTCODE_INPUT, postcode)
        
        self.select_dropdown_by_text(self.COUNTRY_DROPDOWN, country)
        self.wait_helper.wait_for_element_visible(self.REGION_DROPDOWN, timeout=5)
        self.select_dropdown_by_text(self.REGION_DROPDOWN, region)
        
        self.click_element(self.BILLING_CONTINUE)
    
    def continue_delivery_details(self):
        logger.info("Continuing delivery details")
        if self.is_element_present(self.DELIVERY_CONTINUE, timeout=5):
            self.click_element(self.DELIVERY_CONTINUE)
    
    def continue_delivery_method(self):
        logger.info("Continuing delivery method")
        if self.is_element_present(self.DELIVERY_METHOD_CONTINUE, timeout=5):
            self.click_element(self.DELIVERY_METHOD_CONTINUE)
    
    def accept_terms_and_continue_payment(self):
        logger.info("Accepting terms and continuing payment")
        if self.is_element_present(self.TERMS_CHECKBOX, timeout=5):
            self.click_element(self.TERMS_CHECKBOX)
            self.click_element(self.PAYMENT_METHOD_CONTINUE)
    
    def confirm_order(self):
        logger.info("Confirming order")
        self.click_element(self.CONFIRM_ORDER_BUTTON)
        return self.is_order_success()
    
    def is_order_success(self):
        try:
            message = self.get_element_text(self.SUCCESS_MESSAGE, timeout=10)
            return "placed" in message.lower() or "success" in message.lower()
        except:
            return False
    
    def get_order_number(self):
        if self.is_order_success():
            text = self.get_element_text(self.ORDER_NUMBER)
            logger.info(f"Order number: {text}")
            return text
        return ""
    
    def complete_guest_checkout(self, billing_details):
        logger.info("Starting guest checkout process")
        
        # Step 1: Select guest checkout
        self.select_guest_checkout()
        
        # Step 2: Fill billing details
        self.fill_billing_details(
            billing_details.get('first_name'),
            billing_details.get('last_name'),
            billing_details.get('email'),
            billing_details.get('telephone'),
            billing_details.get('address'),
            billing_details.get('city'),
            billing_details.get('postcode'),
            billing_details.get('country', 'United States'),
            billing_details.get('region', 'California')
        )
        
        # Step 3: Continue delivery details
        self.continue_delivery_details()
        
        # Step 4: Continue delivery method
        self.continue_delivery_method()
        
        # Step 5: Accept terms and continue payment
        self.accept_terms_and_continue_payment()
        
        # Step 6: Confirm order
        return self.confirm_order()
    
    def is_page_loaded(self):
        return self.is_element_present(self.GUEST_CHECKOUT_RADIO, timeout=10) or \
               self.is_element_present(self.FIRST_NAME_INPUT, timeout=10)