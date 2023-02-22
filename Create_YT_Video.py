import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import Variables
from TestObjects import test_objects
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def create_video():
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(Variables.chromedriver_path, options=options)

    sign_up_button = test_objects.get("sign_up_button_inVideo")
    login_button = test_objects.get("sign_in_button_inVideo")
    sign_email = test_objects.get("sign_in_email_inVideo")
    sign_in_password = test_objects.get("sign_in_password_inVideo")
    continue_button = test_objects.get("continue_button_inVideo")

    try:

        driver.get('https://invideo.io/')
        driver.maximize_window()
        time.sleep(5)

        sign_up_b = driver.find_element_by_xpath(sign_up_button.locator)
        sign_up_b.click()



        """
        sign_email_b = driver.find_element_by_xpath(sign_email.locator)
        sign_email_b.click()

        sign_in_password_b = driver.find_element_by_xpath(sign_in_password.locator)
        sign_in_password_b.click()

        continue_button_b = driver.find_element_by_xpath(continue_button.locator)
        continue_button_b.click()
        """

        driver.quit()

    except NoSuchElementException:
        print("Element not found")


def main():
    create_video()


if __name__ == '__main__':
    main()
