import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os


@pytest.fixture
def setup():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
def test_valid_login(setup):
    setup.get("https://demo.guru99.com/Agile_Project/Agi_V1/")
    setup.find_element(By.NAME, 'uid').send_keys("1303")
    setup.find_element(By.NAME, 'password').send_keys("Guru99")
    setup.find_element(By.NAME, 'btnLogin').click()
    assert "Welcome" in setup.page_source

# Fixture for Payment Gateway Project
@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    driver.get("https://demo.guru99.com/payment-gateway/index.php")
    request.cls.driver = driver
    yield
    driver.quit()

# Fixture for Bank Project
