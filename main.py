import json
import logging
import os
import random
import shutil
import time
import openai

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from TestObjects import TestObjects

VIDEO_COUNT = 10
MAX_RETRIES = 5
SLEEP_LOWER = 7
SLEEP_UPPER = 15
TIMEOUT = 10

CONFIG_FILE = "config.json"
LOG_FILE = "upload_log.log"

# Create logging file
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""Load json file into main"""


def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


"""Create WebDriver class using ChromeDriverManager"""


def get_web_driver():
    options = Options()
    options.add_argument("--incognito")
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


"""Creating a random time for the driver to sleep"""


def random_sleep():
    time.sleep(random.randint(SLEEP_LOWER, SLEEP_UPPER))


"""Retries to find the element with the backup of the xpath saved in config.json file"""


def find_element_on_page(driver, primary, backup):
    try:
        return driver.find_element(*primary.locator)
    except:
        return driver.find_element(*backup.locator)


"""Generating random description for Youtube video"""


def generate_description(api_key, prompt):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


"""Login into Youtube"""


def login(driver, username, password, test_objects):
    driver.get('https://www.youtube.com')
    driver.maximize_window()
    random_sleep()

    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(test_objects["login_button"].locator))

    login_button = driver.find_element(*test_objects["login_button"].locator)
    login_button.click()
    random_sleep()

    sign_in_email = driver.find_element(*test_objects["sign_in_email"].locator)
    sign_in_email.click()
    sign_in_email.send_keys(username)
    random_sleep()

    next_button = driver.find_element(*test_objects["next_button"].locator)
    next_button.click()
    random_sleep()

    sign_in_password = driver.find_element(*test_objects["sign_in_password"].locator)
    sign_in_password.click()
    sign_in_password.send_keys(password)
    random_sleep()

    next_button2 = driver.find_element(*test_objects["next_button"].locator)
    next_button2.click()
    random_sleep()

    logging.info("Finished Logining in..")

    return True


"""Uploading video to Youtube 10 times"""


def upload_videos(driver, test_objects, video_number, video_dir, used_videos_dir,api_key):
    count = 1

    while count <= VIDEO_COUNT:

        video_files = os.listdir(video_dir)
        video_path = os.path.join(video_dir, video_files[0])

        logging.info(f"Starting to upload video {count}")

        create_button = find_element_on_page(driver, test_objects["create_button"], test_objects["create_button_BU"])
        create_button.click()
        random_sleep()

        upload_button = find_element_on_page(driver, test_objects["upload_video"], test_objects["upload_video_BU"])
        upload_button.click()
        random_sleep()

        file_input = find_element_on_page(driver, test_objects["select_button"], test_objects["select_button_BU"])

        try:
            file_input.send_keys(video_path)
            time.sleep(5)
            video_number += 1
            logging.info("Upload successful")
            shutil.move(video_path, os.path.join(used_videos_dir, video_files[0]))
        except Exception as e:
            logging.error(f"Upload unsuccessful: {e}")

        title = f"Quote of the Day Pt. {video_number}"
        random_sleep()

        title_box = find_element_on_page(driver, test_objects["title_box"], test_objects["title_box_BU"])
        title_box.clear()
        title_box.send_keys(title)

        with open("video_number.txt", "w") as f:
            f.write(str(video_number))

        description_box = find_element_on_page(driver, test_objects["description_box"],
                                               test_objects["description_box_BU"])
        prompt = "Generate a random and unique text for a youtube description about cooking quotes in 20 words or less"
        generated_description = generate_description(api_key, prompt)
        description_box.send_keys(generated_description)

        random_sleep()

        no_kids_button = find_element_on_page(driver, test_objects["no_kids"], test_objects["no_kids_BU"])
        no_kids_button.click()
        random_sleep()

        youtube_next_button = find_element_on_page(driver, test_objects["youtube_next_button"],
                                                   test_objects["youtube_next_button_BU"])
        youtube_next_button.click()
        random_sleep()

        youtube_next_button1 = find_element_on_page(driver, test_objects["youtube_next_button"],
                                                    test_objects["youtube_next_button_BU"])
        youtube_next_button1.click()
        random_sleep()

        youtube_next_button2 = find_element_on_page(driver, test_objects["youtube_next_button"],
                                                    test_objects["youtube_next_button_BU"])
        youtube_next_button2.click()
        random_sleep()

        public_button = find_element_on_page(driver, test_objects["public_button"], test_objects["public_button_BU"])
        public_button.click()
        random_sleep()

        save_button = find_element_on_page(driver, test_objects["save_button"], test_objects["save_button_BU"])
        save_button.click()
        random_sleep()

        logging.info(f"Video number {count} is completed.")
        driver.get('https://www.youtube.com')
        random_sleep()

        count += 1

    driver.quit()


def main():
    config = load_config(CONFIG_FILE)

    username = config['username']
    password = config['password']
    video_dir = config['video_dir']
    used_videos_dir = config['used_videos_dir']
    api_key = config["api_key"]

    test_objects = {
        key: TestObjects(By.XPATH, value[1]) if value[0] == 'xpath' else TestObjects(By.CSS_SELECTOR, value[1])
        for key, value in config['test_objects'].items()
    }

    test_objects.update({
        key: TestObjects(By.XPATH, value[1]) if value[0] == 'xpath' else TestObjects(By.CSS_SELECTOR, value[1])
        for key, value in config['test_objects_backup'].items()
    })

    driver = get_web_driver()
    login_success = login(driver, username, password, test_objects)

    if login_success:
        print("Login successful.")
        with open("video_number.txt", "r") as f:
            video_number = int(f.read())
        upload_videos(driver, test_objects, video_number, video_dir, used_videos_dir, api_key)
    else:
        print("Login failed.")

    driver.quit()


if __name__ == '__main__':
    main()
