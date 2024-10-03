import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import Select



class TestLogin:

    def setup_method(self):
        # WebDriver setup (adjust for your WebDriver)
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://demo.guru99.com/Agile_Project/Agi_V1/")

    def teardown_method(self):
        # Close browser after test
        self.driver.quit()

    def test_valid_login(self):
        self.driver.find_element(By.NAME, 'uid').send_keys("1303")
        self.driver.find_element(By.NAME, 'password').send_keys("Guru99")
        self.driver.find_element(By.NAME, 'btnLogin').click()
        time.sleep(2)
        assert "Welcome" in self.driver.page_source

    def test_invalid_login(self):
        self.driver.find_element(By.NAME, 'uid').send_keys("wrong_user")
        self.driver.find_element(By.NAME, 'password').send_keys("wrong_pass")
        self.driver.find_element(By.NAME, 'btnLogin').click()
        time.sleep(2)
        try:
            # Switch to the alert
            alert = self.driver.switch_to.alert

            # Get the text from the alert
            alert_text = alert.text

            # Assert that the alert text contains the expected message
            assert "User or Password is not valid" in alert_text

            # Accept the alert (close it)
            alert.accept()
        except TimeoutException:
            # Handle the case where no alert is present within the expected time
            assert False, "Expected alert did not appear."


        except NoAlertPresentException:
            # Handle the case where no alert is present (if necessary)
            assert False, "Alert not found when expected"

    def test_empty_credentials(self):
        self.driver.find_element(By.NAME, 'btnLogin').click()
        time.sleep(3)
        alert = self.driver.switch_to.alert

        # Get the text from the alert
        alert_text = alert.text

        # Verify the alert message
        assert "User or Password is not valid" in alert_text, f"Unexpected alert text: {alert_text}"

        # Accept the alert to close it
        alert.accept()
        time.sleep(3)
    def test_reset_button(self):
        self.driver.find_element(By.NAME, 'uid').send_keys("1303")
        self.driver.find_element(By.NAME, 'password').send_keys("Guru99")
        self.driver.find_element(By.NAME, 'btnReset').click()
        # Assert that fields are cleared
        assert self.driver.find_element(By.NAME, 'uid').get_attribute('value') == ""
        assert self.driver.find_element(By.NAME, 'password').get_attribute('value') == ""
        time.sleep(3)

class TestPaymentGateway:
    def setup_method(self):
        # WebDriver setup
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://demo.guru99.com/payment-gateway/index.php")

    def teardown_method(self):
        self.driver.quit()
        time.sleep(3)
    def test_select_item_and_buy(self):
        select_element = Select(self.driver.find_element(By.NAME, 'quantity'))
        time.sleep(3)
        # Select option by visible text or by index.
        select_element.select_by_index(3)  # selects second item

        # Click the Buy button
        self.driver.find_element(By.XPATH, "//*[@id='three']/div/form/div/div[8]/ul/li/input").click()
        time.sleep(3)

        assert "Payment Process" in self.driver.page_source
        time.sleep(3)

    def test_fill_credit_card(self):
        # Select an item and go to the payment process page
        self.test_select_item_and_buy()

        # Fill in fake credit card details
        self.driver.find_element(By.NAME, 'card_nmuber').send_keys("1234567812345678")
        self.driver.find_element(By.NAME, 'cvv_code').send_keys("123")

        # Select expiration month
        select_month = Select(self.driver.find_element(By.NAME, 'month'))
        select_month.select_by_visible_text("12")  # December

        # Select expiration year
        select_year = Select(self.driver.find_element(By.NAME, 'year'))
        select_year.select_by_visible_text("2025")
        time.sleep(3)

        # Click 'Pay' button
        self.driver.find_element(By.NAME, 'submit').click()

        # Assert a success message or error message
        assert "Payment success" in self.driver.page_source or "Transaction failed" in self.driver.page_source
        time.sleep(5)
