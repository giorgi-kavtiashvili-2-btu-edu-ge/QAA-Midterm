import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RegistrationPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://magento.softwaretestingboard.com/customer/account/create"
        self.first_name_input = (By.ID, "firstname")
        self.last_name_input = (By.ID, "lastname")
        self.email_input = (By.ID, "email_address")
        self.password_input = (By.ID, "password")
        self.confirm_password_input = (By.ID, "password-confirmation")
        self.register_button = (By.XPATH, "//button[@type='submit']")

    def open(self):
        self.driver.get(self.url)

    def register(self, first_name, last_name, email, password):
        self.driver.find_element(*self.first_name_input).send_keys(first_name)
        self.driver.find_element(*self.last_name_input).send_keys(last_name)
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.confirm_password_input).send_keys(password)
        self.driver.find_element(*self.register_button).click()

class AuthorizationPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.ID, "email")
        self.password_input = (By.ID, "pass")
        self.login_button = (By.ID, "send2")

    def login(self, email, password):
        self.driver.find_element(*self.email_input).send_keys(email)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

def positive_registration_test(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.register("John", "Doe", "john.doe@example.com", "password")

    assert "My Account" in driver.title
    assert "Thank you for registering with Main Website Store." in driver.page_source

def negative_registration_test(driver):
    registration_page = RegistrationPage(driver)
    registration_page.open()
    registration_page.register("", "", "", "")  # Empty fields

    assert "This is a required field." in driver.page_source

def positive_authorization_test(driver):
    authorization_page = AuthorizationPage(driver)
    authorization_page.login("john.doe@example.com", "password")

    assert "My Account" in driver.title
    assert "Hello, John Doe!" in driver.page_source

def negative_authorization_test(driver):
    authorization_page = AuthorizationPage(driver)
    authorization_page.login("invalid@example.com", "invalidpassword")

    assert "Invalid login or password." in driver.page_source

if __name__ == "__main__":
    driver = webdriver.Chrome()  # Assuming Chrome webdriver is used
    try:
        positive_registration_test(driver)
        negative_registration_test(driver)
        positive_authorization_test(driver)
        negative_authorization_test(driver)
        print("All tests passed successfully!")
    finally:
        driver.quit()
