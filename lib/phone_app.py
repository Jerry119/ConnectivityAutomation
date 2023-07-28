from lib.appium_utils import AppiumUtils
from lib.logger.logger import Logger

logger = Logger(logger_name=__name__).logger


class PhoneApp(AppiumUtils):
    def __init__(self, dut, app_conf):
        super().__init__(dut, app_conf)

    def launch_app(self):
        resp = self.launch_application()
        if resp:
            logger.info("Phone app launched")
        else:
            logger.error("Exception occurred while launching Phone app")
    
    def go_to_dial_screen(self):
        self.wait_until_available(self.app_elements_info["keypad_icon"])
        self.tap_on_element("keypad_icon")

    def make_a_call_to(self, num):
        self.wait_until_available(self.app_elements_info["number_input"])
        self.send_text("number_input", num)
        # self.tap_on_element("dial_button")