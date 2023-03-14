import shutil
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from Variables import video_dir, used_videos_dir

from TestObjects import test_objects

import os


def login(username, password):
    """Create a Chrome web driver instance"""
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    """Initializing Test Objects"""

    login_button = test_objects.get("login_button")
    sign_in_email = test_objects.get("sign_in_email")
    next_button = test_objects.get("next_button")
    sign_in_password = test_objects.get("sign_in_password")
    create_button = test_objects.get("create_button")
    upload_button = test_objects.get("upload_video")
    file_input = test_objects.get("select_button")
    title_box = test_objects.get('title_box')
    descript_box = test_objects.get("description_box")
    no_kids = test_objects.get("no_kids")
    youtube_next_button = test_objects.get("youtube_next_button")
    public_button = test_objects.get("public_button")
    save_button = test_objects.get("save_button")
    close_button = test_objects.get("close_button")

    video_files = os.listdir(video_dir)
    video_path = os.path.join(video_dir, video_files[0])

    if os.path.exists("video_number.txt"):
        # If the file exists, read the value of "i" from it
        with open("video_number.txt", "r") as f:
            video_number = int(f.read().strip())
    else:
        # If the file does not exist, set the value of "i" to 0
        video_number = 0

    # navigate to YouTube and identify test objects
    # Click on test objects then sleep until webpages are loaded properly
    try:

        driver.get('https://www.youtube.com')
        driver.maximize_window()
        time.sleep(15)

        login_b = driver.find_element(By.XPATH, login_button.locator)
        login_b.click()
        time.sleep(15)

        sign_in_b = driver.find_element(By.XPATH, sign_in_email.locator)
        sign_in_b.click()
        sign_in_b.send_keys(username)
        time.sleep(15)

        next_b = driver.find_element(By.XPATH, next_button.locator)
        next_b.click()

        time.sleep(15)

        sign_in_p_b = driver.find_element(By.XPATH, sign_in_password.locator)
        sign_in_p_b.click()
        sign_in_p_b.send_keys(password)

        time.sleep(15)

        next_b2 = driver.find_element(By.XPATH, next_button.locator)
        next_b2.click()

        time.sleep(15)

        create_b = driver.find_element(By.XPATH, create_button.locator)
        create_b.click()

        time.sleep(15)

        upload_b = driver.find_element(By.XPATH, upload_button.locator)
        upload_b.click()

        time.sleep(15)

        file_upload = driver.find_element(By.XPATH, file_input.locator)

        try:
            file_upload.send_keys(video_path)
            time.sleep(5)
            video_number += 1
            print("Upload successful")
            shutil.move(video_path, os.path.join(used_videos_dir, video_files[0]))
        except Exception as e:
            print(f"Upload unsuccessful: {e}")

        num_videos_uploaded = len(video_files)
        title = f"Quote of the Day Pt. {video_number}"

        time.sleep(15)

        title_b = driver.find_element(By.XPATH, title_box.locator)
        title_b.clear()
        title_b.send_keys(title)

        with open("video_number.txt", "w") as f:
            f.write(str(video_number))

        description_box_b = driver.find_element(By.XPATH, descript_box.locator)
        description_box_b.send_keys("Get ready to spice up your kitchen with these hilarious and interesting cooking "
                                    "quotes! Don't forget to like, comment, and subscribe for more foodie content.")

        time.sleep(15)

        no_kids_b = driver.find_element(By.XPATH, no_kids.locator)
        no_kids_b.click()

        time.sleep(15)

        youtube_b = driver.find_element(By.XPATH, youtube_next_button.locator)
        youtube_b.click()

        time.sleep(15)

        youtube_b1 = driver.find_element(By.XPATH, youtube_next_button.locator)
        youtube_b1.click()

        time.sleep(15)

        youtube_b2 = driver.find_element(By.XPATH, youtube_next_button.locator)
        youtube_b2.click()

        time.sleep(15)

        public_b = driver.find_element(By.XPATH, public_button.locator)
        public_b.click()

        time.sleep(15)

        save_b = driver.find_element(By.XPATH, save_button.locator)
        save_b.click()

        time.sleep(15)

        close_b = driver.find_element(By.XPATH, close_button.locator)
        close_b.click()

        time.sleep(15)

        driver.quit()
        return True

    except NoSuchElementException as e:
        print("Element not found: ", e.msg)
        return False
