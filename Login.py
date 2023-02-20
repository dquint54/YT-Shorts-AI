from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from TestObjects import TestObjects, test_objects
import time
import Variables



def login(username, password):

    # Create a Chrome web driver instance

    driver = webdriver.Chrome(Variables.chromedriver_path)

    # Navigate to the login page
    driver.get('https://www.youtube.com')
    driver.maximize_window()
    time.sleep(5)

    login_button = test_objects.get("login_button")
    sign_in_email = test_objects.get("sign_in_email")
    next_button = test_objects.get("next_button")



    login_b = driver.find_element_by_xpath(login_button.locator)
    login_b.click()

    sign_in_b = driver.find_element_by_xpath(sign_in_email.locator)
    sign_in_b.click()
    sign_in_b.send_keys(Variables.username)

    next_b = driver.find_element_by_xpath(next_button.locator)
    next_b.click()

    time.sleep(5)







    driver.quit()








