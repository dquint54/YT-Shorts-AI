import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import Variables
from TestObjects import test_objects


def login(username, password):
    # Create a Chrome web driver instance
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(Variables.chromedriver_path, chrome_options=options)

    # importing the test objects from TestObjects.py

    login_button = test_objects.get("login_button")
    sign_in_email = test_objects.get("sign_in_email")
    next_button = test_objects.get("next_button")
    sign_in_password = test_objects.get("sign_in_password")


    # navigate to YouTube and identify test objects
    # Click on test objects then sleep until webpages are loaded properly
    try:

        driver.get('https://www.youtube.com')
        driver.maximize_window()
        time.sleep(5)

        login_b = driver.find_element_by_xpath(login_button.locator)
        login_b.click()

        sign_in_b = driver.find_element_by_xpath(sign_in_email.locator)
        sign_in_b.click()
        sign_in_b.send_keys(Variables.username)

        next_b = driver.find_element_by_xpath(next_button.locator)
        next_b.click()

        time.sleep(5)

        sign_in_p_b = driver.find_element_by_xpath(sign_in_password.locator)
        sign_in_p_b.click()
        sign_in_p_b.send_keys(Variables.password)

        next_b2 = driver.find_element_by_xpath(next_button.locator)
        next_b2.click()

        time.sleep(5)

        driver.quit()
        return True

    except NoSuchElementException:
        print("Element not found")
        return False

