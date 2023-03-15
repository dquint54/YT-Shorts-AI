from selenium.webdriver.common.by import By


class TestObjects:
    def __init__(self, locator_type, locator_value):
        self.locator = (locator_type, locator_value)


test_objects = {
    # Start YouTube Test Objects
    "login_button": TestObjects(By.XPATH, "(//*[@aria-label='Sign in'])[1]"),
    "sign_in_email": TestObjects(By.XPATH, "//input[@type= 'email']"),
    "next_button": TestObjects(By.XPATH,
                               "//button[@data-idom-class= 'nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']"),
    "sign_in_password": TestObjects(By.XPATH, "//input[@type ='password']"),
    "create_button": TestObjects(By.XPATH, "//button[@aria-label='Create']"),
    "upload_video": TestObjects(By.XPATH, "//a[@href='/upload']"),
    "select_button": TestObjects(By.XPATH, "//input[@type='file' and @name='Filedata']"),
    "title_box": TestObjects(By.XPATH, "//div[@aria-label='Add a title that describes your video']"),
    "description_box": TestObjects(By.XPATH, "//div[@aria-label='Tell viewers about your video']"),
    "no_kids": TestObjects(By.XPATH, "(//ytcp-ve[@class='style-scope ytkc-made-for-kids-select'])[2]"),
    "public_button": TestObjects(By.XPATH, "//*[@name='PUBLIC']"),
    "close_button": TestObjects(By.XPATH, "//*[@id='close-icon-button']"),
    "youtube_next_button": TestObjects(By.XPATH, "//ytcp-button[@id='next-button']"),
    "save_button": TestObjects(By.XPATH, "//ytcp-button[@id='done-button']"),

    # Back Up TestObjects
    "create_button_BU": TestObjects(By.XPATH,
                                    "//a[@class='yt-simple-endpoint style-scope ytd-topbar-menu-button-renderer']"),
    "upload_video_BU": TestObjects(By.XPATH, "//yt-formatted-string[@id='label' and contains(text(),'Upload video')]"),
    "select_button_BU": TestObjects(By.XPATH, "//input[@type='file' and @name='Filedata']"),
    "title_box_BU": TestObjects(By.XPATH,
                                "//div[@id='textbox' and @aria-label='Add a title that describes your video']"),
    "description_box_BU": TestObjects(By.XPATH, "//div[@id='textbox' and @aria-label='Tell viewers about your video']"),
    "no_kids_BU": TestObjects(By.XPATH, "(//div[@id='radioContainer']"),
    "public_button_BU": TestObjects(By.XPATH, "//div[@id='offRadio']"),
    "close_button_BU": TestObjects(By.XPATH, "//*[@id='close-icon-button']"),
    "youtube_next_button_BU": TestObjects(By.XPATH, "//ytcp-button[@id='next-button']"),
    "save_button_BU": TestObjects(By.XPATH, "//div[@class='label style-scope ytcp-button' and text()='Save']"),

    # End YouTube
}


"""Creating a Dictionary to correspond each backup to its orignal testobject"""


backup_test_objects = {
    "login_button": "login_button_BU",
    "upload_video": "upload_video_BU",
    "select_button": "select_button_BU",
    "title_box": "title_box_BU",
    "description_box": "description_box_BU",
    "no_kids": "no_kids_BU",
    "public_button": "public_button_BU",
    "close_button": "close_button_BU",
    "youtube_next_button": "youtube_next_button_BU",
    "save_button": "save_button_BU",
}
