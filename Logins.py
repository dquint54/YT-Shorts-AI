import shutil
import time
import random


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from Variables import video_dir, used_videos_dir

from TestObjects import test_objects, backup_test_objects

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

    """End Initializing Test objects"""

    r_int = random.randint(7, 15)
    timeout = 10

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

    max_retries = 5
    retries = 0

    while retries < max_retries:

        try:

            driver.get('https://www.youtube.com')
            driver.maximize_window()
            time.sleep(r_int)

            WebDriverWait(driver, timeout).until(EC.presence_of_element_located(login_button.locator))

            login_b = driver.find_element(*login_button.locator)
            login_b.click()

            time.sleep(r_int)

            sign_in_b = driver.find_element(*sign_in_email.locator)
            sign_in_b.click()
            sign_in_b.send_keys(username)
            time.sleep(r_int)

            next_b = driver.find_element(*next_button.locator)
            next_b.click()

            time.sleep(r_int)

            sign_in_p_b = driver.find_element(*sign_in_password.locator)
            sign_in_p_b.click()
            sign_in_p_b.send_keys(password)

            time.sleep(r_int)

            next_b2 = driver.find_element(*next_button.locator)
            next_b2.click()

            time.sleep(r_int)

            count = 1
            while count <= 10:

                uploading_video = f"Starting to upload video {count}"
                print(uploading_video)

                create_b = driver.find_element(*create_button.locator)
                create_b.click()

                time.sleep(r_int)

                upload_b = driver.find_element(*upload_button.locator)
                upload_b.click()

                time.sleep(r_int)

                file_upload = driver.find_element(*file_input.locator)

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

                time.sleep(r_int)

                title_b = driver.find_element(*title_box.locator)
                title_b.clear()
                title_b.send_keys(title)

                with open("video_number.txt", "w") as f:
                    f.write(str(video_number))

                description_box_b = driver.find_element(*descript_box.locator)
                description_box_b.send_keys(
                    "Get ready to spice up your kitchen with these hilarious and interesting cooking "
                    "quotes! Don't forget to like, comment, and subscribe for more foodie content.")

                time.sleep(r_int)

                no_kids_b = driver.find_element(*no_kids.locator)
                no_kids_b.click()

                time.sleep(r_int)

                youtube_b = driver.find_element(*youtube_next_button.locator)
                youtube_b.click()

                time.sleep(r_int)

                youtube_b1 = driver.find_element(*youtube_next_button.locator)
                youtube_b1.click()

                time.sleep(r_int)

                youtube_b2 = driver.find_element(*youtube_next_button.locator)
                youtube_b2.click()

                time.sleep(r_int)

                public_b = driver.find_element(*public_button.locator)
                public_b.click()

                time.sleep(r_int)

                save_b = driver.find_element(*save_button.locator)
                save_b.click()

                time.sleep(r_int)

                close_b = driver.find_element(*close_button.locator)
                close_b.click()

                time.sleep(r_int)

                finishing_video = f"Video number {count} is completed."
                print(finishing_video)

                driver.get('https://www.youtube.com')

                time.sleep(r_int)

                count += 1

            driver.quit()
            return True
        except NoSuchElementException as e:
            print("Element not found: ", e.msg)

            retries += 1

            """Figure out which test object threw the exception"""
            for var_name, test_obj in test_objects.items():
                try:
                    driver.find_element(*test_obj.locator)
                except NoSuchElementException:

                    # Update the XPath for the variable that caused the exception
                    # with the XPath of the corresponding backup variable

                    backup_var_name = backup_test_objects.get(var_name)

                    if backup_var_name:

                        backup_test_obj = test_objects.get(backup_var_name)
                        test_obj.locator = backup_test_obj.locator
                        print(f"Using backup variable '{backup_var_name}'")

                    else:
                        print(f"No backup variable found for '{var_name}'")
                    break
        continue

    return False

