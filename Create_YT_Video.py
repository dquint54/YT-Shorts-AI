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
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--enable-javascript")

    driver = webdriver.Chrome(Variables.chromedriver_path, options=options)

    try:

        driver.quit()

    except NoSuchElementException:
        print("Element not found")


def main():
    create_video()


if __name__ == '__main__':
    main()
