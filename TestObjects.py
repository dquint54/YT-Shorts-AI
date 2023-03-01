class TestObjects:
    def __init__(self, locator_type, locator):
        self.locator_type = locator_type
        self.locator = locator


test_objects = {

    # Start YouTube Test Objects

    "search_button": TestObjects("xpath", "//form[@class='flex flex-auto items-center justify-center pl3 justify-start-hdkp pa0-hdkp ml3-hdkp static']"),
    "sign_in_email": TestObjects("xpath", "//input[@class='whsOnd zHQkBf'][@type='email']"),
    "next_button": TestObjects("xpath", "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ "
                                        "VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc "
                                        "lw1w4b']"),
    "sign_in_password": TestObjects("xpath", "//input[@type ='password']"),
    # End YouTube















}
