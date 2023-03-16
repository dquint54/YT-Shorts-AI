import json
import logging
import os
import random
import shutil
import time
import openai
import tkinter as tk
import threading
import sys

from tkinter import ttk
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from TestObjects import TestObjects
from tkinter.scrolledtext import ScrolledText

VIDEO_COUNT = 10
MAX_RETRIES = 5
SLEEP_LOWER = 7
SLEEP_UPPER = 15
TIMEOUT = 10
exit_app = False

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))


CONFIG_FILE = config_file_path = 'C:\\Users\\Q\\PycharmProjects\\YT-Shorts-AI\\config.json'
LOG_FILE = "upload_log.log"

# Create logging file
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""Clear Log file"""


def clear_log_file(log_file):
    with open(log_file, "w") as file:
        file.write("")


"""Load json file into main"""


def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


"""Updating Log File For GUI"""


def update_log_content(log_file, text_area):
    while not exit_app:
        with open(log_file, "r") as file:
            log_content = file.readlines()

        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, "".join(log_content))
        text_area.config(state=tk.DISABLED)
        time.sleep(1)


"""GUI for the logging"""


def show_log_file(log_file):
    def on_closing():
        global exit_app
        exit_app = True
        root.destroy()

    root = tk.Tk()
    root.title("Log File")

    style = ttk.Style()
    style.theme_use('clam')

    frame = ttk.Frame(root, padding="5")
    frame.pack(fill=tk.BOTH, expand=True)

    text_area = ScrolledText(frame, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH)

    text_area.configure(bg='#1e1e1e', fg='#ffffff', font=('Consolas', 11))

    root.protocol("WM_DELETE_WINDOW", on_closing)

    log_updater_thread = threading.Thread(target=update_log_content, args=(log_file, text_area))
    log_updater_thread.start()

    root.mainloop()
    log_updater_thread.join()


"""Create WebDriver class using ChromeDriverManager"""


def get_web_driver():
    options = Options()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.set_window_position(-2000, 0)



    return driver


"""Creating a random time for the driver to sleep"""


def random_sleep():
    time.sleep(random.randint(SLEEP_LOWER, SLEEP_UPPER))


"""Retries to find the element with the backup of the xpath saved in config.json file"""


def find_element_on_page(driver, primary, backup):
    try:
        return driver.find_element(*primary.locator)
    except NoSuchElementException:
        logging.error("Failed to find element using the primary locator: %s", primary.locator)
        logging.info("Trying to find element using the backup locator: %s", backup.locator)
        try:
            element = driver.find_element(*backup.locator)
            logging.info("Successfully found element using the backup locator: %s", backup.locator)
            return element
        except NoSuchElementException:
            logging.error("Failed to find element using both primary and backup locators.")
            raise

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
    logging.info("Starting Logining in process..")

    driver.get('https://www.youtube.com')

    random_sleep()

    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located(test_objects["login_button"].locator))

    logging.info("Clicking Login button...")
    login_button = driver.find_element(*test_objects["login_button"].locator)
    login_button.click()
    random_sleep()

    logging.info("Entering Email...")
    sign_in_email = driver.find_element(*test_objects["sign_in_email"].locator)
    sign_in_email.click()
    sign_in_email.send_keys(username)
    random_sleep()

    logging.info("Clicking next button...")
    next_button = driver.find_element(*test_objects["next_button"].locator)
    next_button.click()
    random_sleep()

    max_retries = 3
    retries = 0

    while retries < max_retries:
        logging.info("Entering password...")
        sign_in_password = driver.find_element(*test_objects["sign_in_password"].locator)
        sign_in_password.click()
        sign_in_password.send_keys(password)
        random_sleep()

        logging.info("Clicking next button after entering password...")
        current_url = driver.current_url
        next_button2 = driver.find_element(*test_objects["next_button"].locator)
        next_button2.click()
        random_sleep()

        new_url = driver.current_url

        if current_url != new_url:
            break
        else:
            logging.warning("URL didn't change after clicking next button, waiting and refreshing...")
            time.sleep(5)
            driver.refresh()
            random_sleep()

        retries += 1

    if retries == max_retries:
        logging.error("Unable to proceed after entering the password.")
        return False

    logging.info("Finished Logining in..")

    return True


"""Uploading video to Youtube 10 times"""


def upload_videos(driver, test_objects, video_number, video_dir, used_videos_dir, api_key):
    count = 1

    while count <= VIDEO_COUNT:

        video_files = os.listdir(video_dir)
        video_path = os.path.join(video_dir, video_files[0])

        logging.info(f"Starting to upload video {count}")

        logging.info("Clicking create button...")
        create_button = find_element_on_page(driver, test_objects["create_button"], test_objects["create_button_BU"])
        create_button.click()
        random_sleep()

        logging.info("Clicking upload button...")
        upload_button = find_element_on_page(driver, test_objects["upload_video"], test_objects["upload_video_BU"])
        upload_button.click()
        random_sleep()

        logging.info("Selecting video file...")
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

        logging.info("Entering video title...")
        title_box = find_element_on_page(driver, test_objects["title_box"], test_objects["title_box_BU"])
        title_box.clear()
        title_box.send_keys(title)

        with open("video_number.txt", "w") as f:
            f.write(str(video_number))

        logging.info("Entering video description...")
        description_box = find_element_on_page(driver, test_objects["description_box"],
                                               test_objects["description_box_BU"])
        prompt = "Generate a random and unique text for a youtube description about cooking in 20 words or less and end the text with telling the viewer to like comment and subscribe!"
        generated_description = generate_description(api_key, prompt)
        description_box.send_keys(generated_description)

        random_sleep()

        logging.info("Clicking 'No, it's not made for kids' button...")
        no_kids_button = find_element_on_page(driver, test_objects["no_kids"], test_objects["no_kids_BU"])
        no_kids_button.click()
        random_sleep()

        logging.info("Clicking next button...")
        youtube_next_button = find_element_on_page(driver, test_objects["youtube_next_button"],
                                                   test_objects["youtube_next_button_BU"])
        youtube_next_button.click()
        random_sleep()

        logging.info("Clicking next button again...")
        youtube_next_button1 = find_element_on_page(driver, test_objects["youtube_next_button"],
                                                    test_objects["youtube_next_button_BU"])
        youtube_next_button1.click()
        random_sleep()

        logging.info("Clicking next button one more time...")
        youtube_next_button2 = find_element_on_page(driver, test_objects["youtube_next_button"],
                                                    test_objects["youtube_next_button_BU"])
        youtube_next_button2.click()
        random_sleep()

        logging.info("Clicking public button...")
        public_button = find_element_on_page(driver, test_objects["public_button"], test_objects["public_button_BU"])
        public_button.click()
        random_sleep()

        logging.info("Clicking save button...")
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
    clear_log_file(LOG_FILE)

    log_thread = threading.Thread(target=show_log_file, args=(LOG_FILE,))
    log_thread.start()

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
        video_number_file = "video_number.txt"

        if not os.path.exists(video_number_file):
            with open(video_number_file, "w") as f:
                f.write("1")

        with open(video_number_file, "r") as f:
            video_number = int(f.read())

        upload_videos(driver, test_objects, video_number, video_dir, used_videos_dir, api_key)
    else:
        print("Login failed.")

    driver.quit()
    log_thread.join()


if __name__ == '__main__':
    main()
