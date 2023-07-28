from lib.appium_utils import AppiumUtils
from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class MusicApp(AppiumUtils):
    def __init__(self, dut, app_conf):
        super().__init__(dut, app_conf)

    def launch_app(self):
        resp = self.launch_application()
        if resp:
            logger.info("Music app launched")
        else:
            logger.error("Exception occurred while launching Music app")
    
    def play_music_from_fresh(self):
        self.wait_until_available(self.app_elements_info["three_dot_icon"])
        self.tap_on_element("three_dot_icon")
        self.wait_until_title_visible(self.app_elements_info["play_text"])
        self.tap_on_element("play_text")

    def pause_music(self):
        self.wait_until_available(self.app_elements_info["play_icon"])
        self.tap_on_element("play_icon")
