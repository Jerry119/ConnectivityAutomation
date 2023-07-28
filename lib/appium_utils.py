import re
import subprocess

from appium import webdriver
# from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.config import Config
from lib.global_constants import GlobalConstants as Global

from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class AppiumUtils:
    def __init__(self, dut, app_conf):
        self.driver = None
        self.dut = dut
        self.host = "http://localhost:4723/wd/hub"
        self.desired_caps = {
            "udid": dut.id,
            "platformName": "Android",
            "platformVersion": "12",
            "appPackage": app_conf.get("app_package", None),
            "appActivity": app_conf.get("app_activity", None),
            "automationName": "UiAutomator2",
            # "newCommandTimeout": 3600,
        }
        self.app_elements_info = self.get_app_elements_info()

    def launch_application(self, retry=3):
        """
        Launch an application using initialized desired capabilities
        """
        if retry == 0:
            logger.error("Appium Launch error!")
            return False
        try:
            implicit_wait = 12  # sec

            subprocess.call(f"adb -s {self.dut.id} forward --remove-all", shell=True)
            print(self.dut.id)
            self.driver = webdriver.Remote(self.host, self.desired_caps)
            self.driver.implicitly_wait(implicit_wait)
            if not self.driver:
                raise Exception("Application not launched")
            return True
        except Exception as e:
            logger.exception(
                "Exception occurred while initializing appium "
                "driver. Try restarting appium server | "
                "ERROR: %s" % e
            )
            return False

    def close_application(self, app_package=None):
        """
        Disconnect and close the application
        """
        try:
            if not self.driver:
                raise Exception("Application not launched")
            if app_package:
                self.driver.terminate_app(app_package)
                logger.info("Application terminated")
            self.driver.close_app()
            logger.info("Application closed")
            return True
        except Exception as e:
            logger.exception(
                "Exception occurred while disconnecting appium | ERROR: %s" % e
            )
            return False

    def press_keycode(self, keycode):
        try:
            if not self.driver:
                raise Exception("Application not launched")

            self.driver.press_keycode(keycode)
            logger.info("Volume Increase event raised")
            return True
        except Exception as e:
            logger.exception(
                "Exception occurred while increasing volume | ERROR: %s" % e
            )
            return False

    @staticmethod
    def get_app_elements_info():
        """
        Returns all data from UI elements dict
        """
        try:
            data = Utils.read_json_data(Global.UI_ELEMENTS_H4)["elements"]
            return data
        except Exception as e:
            logger.exception(
                "Exception occurred while getting app elements info | ERROR: %s" % e
            )

    def get_element_by_name(self, element_name):
        """
        Return the element info for a given element name
        """
        element = None
        element_name = str(element_name).lower()
        t1 = Utils().get_current_time()
        try:
            element_info = self.app_elements_info[element_name]
            if "id" in element_info:
                ele_id = element_info["id"]
                if "text" in element_info:
                    elements = self.driver.find_elements(by="id", value=ele_id)
                    for ele in elements:
                        if element_info["text"] in ele.text:
                            element = ele
                            break
                else:
                    element = self.driver.find_element(by="id", value=ele_id)
            elif "xpath" in element_info:
                ele_xpath = element_info["xpath"]
                element = self.driver.find_element(by="xpath", value=ele_xpath)
            else:
                raise ("Could not find element details for '%s'" % element_name)
        except Exception as e:
            t2 = Utils().get_current_time()
            delta = Utils().get_time_diff_s(t1, t2)
            logger.exception(
                "Could not find element '%s' in %s seconds | "
                "EXCEPTION: %s" % (element_name, delta, e)
            )
        return element
    
    def tap_on_element_at_pos(self, element_name, pos):
        try:
            element_name = str(element_name).lower()
            t1 = Utils().get_current_time()
            element_info = self.app_elements_info[element_name]
            ele = self.driver.find_elements(by="id", value=element_info["id"])[pos]
            if self.tap_on(ele):
                logger.debug(f"Tapped on: {element_name}")
                return True
            return False
        except Exception as e:
            t2 = Utils().get_current_time()
            delta = Utils().get_time_diff_s(t1, t2)
            logger.exception(f"Could not find element '{element_name}' in {delta} seconds | EXCEPTION: {e}")
            return False
        
    def get_titles_in_between(self, title1, title2):
        try:
            titles = []
            while True:
                elements = self.driver.find_elements(by="id", value="android:id/title")
                for ele in elements:
                    if ele.text not in titles:
                        titles.append(ele.text)
                logger.debug(titles)
                if len(list(filter(re.compile(f"{title2}.*").match, elements))) == 0:
                    self.scroll_down()
                else:
                    break
            start = titles.index(title1) + 1
            end = titles.index(title2)
            return titles[start:end]
        except Exception as e:
            logger.exception(f"Exception occurred while retriving titles between {title1} and {title2} | ERROR: {e}")
            return []

    def tap_on(self, ele):
        """
        Appium 'tap' functionality is implemented here
        """
        try:
            # actions = TouchAction(self.driver)
            # Utils.time_delay_s(2)
            # actions.tap(ele)
            # Utils.time_delay_s(2)
            # actions.perform()
            ele.click()
            Utils.time_delay_s(1)
            return True
        except Exception as e:
            logger.exception(
                "Exception occurred while tapping element: %s. | "
                "ERROR: %s" % (ele, e)
            )
            return False

    def tap_on_element(self, element):
        """
        Tap on a given element
        """
        ele = self.get_element_by_name(element)
        if ele is not None:
            if self.tap_on(ele):
                logger.debug("Tapped on: %s" % element)
                return True
            return False
        else:
            logger.exception("Could not find element for '%s'" % element)
            return False

    def wait_until_available(self, ele_info, t=5):
        if "id" in ele_info:
            WebDriverWait(self.driver, t).until(EC.presence_of_element_located((By.ID, ele_info["id"])))
        elif "xpath" in ele_info:
            WebDriverWait(self.driver, t).until(EC.presence_of_element_located((By.XPATH, ele_info["xpath"])))
    
    def wait_until_text_visible(self, ele_info, t=5):
        WebDriverWait(self.driver, t).until(EC.text_to_be_present_in_element((By.ID, ele_info["id"]), ele_info["text"]))

    def wait_until_title_visible(self, ele_info, t=5):
        t1 = Utils().get_current_time()
        delta = 0
        while delta < t:
            elements = self.driver.find_elements(by="id", value=ele_info["id"])
            for ele in elements:
                if ele_info["text"] in ele.text:
                    return
            t2 = Utils().get_current_time()
            delta = Utils().get_time_diff_s(t1, t2)
        raise Exception(f"Could not find element {ele_info['text']} in {delta}s")

    def scroll_down(self):
        device_size = self.driver.get_window_size()
        screen_width = device_size["width"]
        screen_height = device_size["height"]
        self.driver.swipe(
            screen_width / 2, screen_height, screen_width / 2, screen_height / 4, 100
        )
    
    def send_text(self, element, txt):
        try:
            ele = self.get_element_by_name(element)
            if ele is not None:
                ele.send_keys(txt)
                Utils.time_delay_s(1)
                self.driver.press_keycode(66)
                Utils.time_delay_s(1)
                return True
            else:
                logger.exception("Could not find element for '%s'" % element)
                return False
        except Exception as e:
            logger.exception(f"Exception occurred while sending \"{txt}\" | ERROR: {e}")
            return False