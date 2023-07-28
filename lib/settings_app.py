from lib.appium_utils import AppiumUtils

from lib.logger.logger import Logger
from lib.utils import Utils
from lib.wificontrol import WiFiControl

logger = Logger(logger_name=__name__).logger


class SettingsApp(AppiumUtils):
    def __init__(self, dut, app_conf):
        super().__init__(dut, app_conf)
    
    def launch_app(self):
        resp = self.launch_application()
        if resp:
            logger.info("Settings app launched")
        else:
            logger.error("Exception occurred while launching Settings app")

    def switch_wifi_toggle(self):
        self.wait_until_available(self.app_elements_info["wifi_toggle"])
        self.tap_on_element("wifi_toggle")
    
    def go_to_wifi_setting_page(self):
        self.wait_until_available(self.app_elements_info["network_setting"])
        self.tap_on_element("network_setting")
        self.wait_until_available(self.app_elements_info["internet_setting"])
        self.tap_on_element("internet_setting")

    def get_wifi_scan_result(self):
        Utils.time_delay_s(3)
        start = "Wi-Fi"
        end = "Add network"
        return self.get_titles_in_between(start, end)

    def select_ssid(self, ssid):
        self.app_elements_info["wifi_ssid"]["text"] = ssid
        wifi = WiFiControl(self.dut)
        attempt = 0
        while attempt < 3:
            ssids = self.get_wifi_scan_result()
            if ssid in ssids and self.tap_on_element("wifi_ssid"):
                break
            wifi.disable_wifi()
            wifi.enable_wifi()
            attempt += 1
        else:
            logger.error(f"not able to find the ssid \"{ssid}\"")

    def enter_wifi_password(self, pwd):
        self.wait_until_available(self.app_elements_info["password_field"])
        self.send_text("password_field", pwd)

    def disconnect_wifi(self):
        self.app_elements_info["wifi_connection_button"]["text"] = "DISCONNECT"
        self.wait_until_available(self.app_elements_info["wifi_connection_button"])
        self.tap_on_element("wifi_connection_button")
    
    def connect_wifi(self):
        self.app_elements_info["wifi_connection_button"]["text"] = "CONNECT"
        self.wait_until_available(self.app_elements_info["wifi_connection_button"])
        self.tap_on_element("wifi_connection_button")
    
    def forget_wifi(self):
        self.wait_until_available(self.app_elements_info["wifi_forget_button"])
        self.tap_on_element("wifi_forget_button")

    def go_to_notification(self):
        self.dut.go_to_notification_screen()
    
    def dismiss_notification(self):
        self.dut.go_to_notification_screen()
    
    def go_back_to_prev_screen(self):
        self.dut.go_back_to_prev_screen()

    def tap_on_bt_icon(self):
        self.wait_until_available(self.app_elements_info["bluetooth_icon"])
        self.tap_on_element("bluetooth_icon")
    
    def go_to_bluetooth_setting_page(self):
        self.tap_on_element("bluetooth_setting")
    
    def initiate_bluetooth_scan(self, t):
        self.tap_on_element("pair_new_device")
        Utils.time_delay_s(t)
    
    def get_bt_scan_result(self):
        start = "Available devices"
        end = "Phone's Bluetooth address"
        return self.get_titles_in_between(start, end)
    
    def get_prev_connected_device(self):
        start = "Previously connected devices"
        end = "See all"
        return self.get_titles_in_between(start, end)
        
    def pair_new_bluetooth_device(self, name):
        self.app_elements_info["bt_name"]["text"] = name
        self.wait_until_title_visible(self.app_elements_info["bt_name"], 15)
        self.tap_on_element("bt_name")
        self.wait_until_available(self.app_elements_info["allow_access_to_contact"])
        self.tap_on_element("allow_access_to_contact")
        self.wait_until_available(self.app_elements_info["pair_button"])
        self.tap_on_element("pair_button")
        Utils.time_delay_s(5)
    
    def pair_saved_bluetooth_device(self, name):
        if self.get_element_by_name("bt_setting_button") is None:
            self.app_elements_info["bt_name"]["text"] = name
            self.tap_on_element("bt_name")
        else:
            idx = self.get_prev_connected_device().index(name)
            self.tap_on_element_at_pos("bt_setting_button", idx)
            self.wait_until_available(self.app_elements_info["bt_connection_button"])
            self.tap_on_element("bt_connection_button")
        Utils.time_delay_s(5)
    
    def disconnect_bluetooth_connection(self):
        self.wait_until_available(self.app_elements_info["bt_setting_button"])
        self.tap_on_element("bt_setting_button")
        self.wait_until_available(self.app_elements_info["bt_connection_button"])
        self.tap_on_element("bt_connection_button")

    def forget_bluetooth_devices(self):
        while True:
            try:
                if self.get_element_by_name("bt_setting_button") is None:
                    break
                self.wait_until_available(self.app_elements_info["bt_setting_button"])
                self.tap_on_element("bt_setting_button")
                self.wait_until_available(self.app_elements_info["bt_forget_button"])
                self.tap_on_element("bt_forget_button")
                self.wait_until_available(self.app_elements_info["forget_device_button"])
                self.tap_on_element("forget_device_button")
            except Exception as e:
                logger.exception(f"Exception occurred while forgetting BT device | ERROR: {e}")

    def wait_for_auto_reconnection(self):
        self.wait_until_text_visible(self.app_elements_info["media_device"], t=15)

    def go_to_software_update(self):
        self.tap_on_element("system_setting")
        self.tap_on_element("software_update")
        self.tap_on_element("check_for_update")