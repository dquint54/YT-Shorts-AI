import json


class TestObjects:
    def __init__(self, locator_type, locator):
        self.locator_type = locator_type
        self.locator = locator


class TestObjectsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TestObjects):
            return {'locator_type': obj.locator_type, 'locator': obj.locator}
        return json.JSONEncoder.default(self, obj)


test_objects = {

    # Start YouTube Test Objects

    "login_button": TestObjects("xpath", "(//*[@aria-label='Sign in'])[1]"),
    "sign_in_email": TestObjects("xpath", "//input[@type= 'email']"),
    "next_button": TestObjects("xpath",
                               "//button[@data-idom-class= 'nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']"),
    "sign_in_password": TestObjects("xpath", "//input[@type ='password']"),
    "create_button": TestObjects("xpath", "//button[@aria-label='Create']"),
    "upload_video": TestObjects("xpath", "//a[@href='/upload']"),
    "select_button": TestObjects("xpath", "//input[@type='file' and @name='Filedata']"),
    "title_box": TestObjects("xpath", "//div[@aria-label='Add a title that describes your video']"),
    "description_box": TestObjects("xpath", "//div[@aria-label='Tell viewers about your video']"),
    "no_kids": TestObjects("xpath", "(//ytcp-ve[@class='style-scope ytkc-made-for-kids-select'])[2]"),
    "public_button": TestObjects("xpath", "//*[@name='PUBLIC']"),
    "close_button": TestObjects("xpath", "//*[@id='close-icon-button']"),
    "youtube_next_button": TestObjects("xpath", "//ytcp-button[@id='next-button']"),
    "save_button": TestObjects("xpath", "//ytcp-button[@id='done-button']")

    # End YouTube

}

json_str = json.dumps(test_objects, cls=TestObjectsEncoder)
