import pytest

from lib.config import Config
from lib.global_constants import GlobalConstants as Global
from lib.ironman import Ironman
from lib.logger.logger import Logger
from lib.settings_app import SettingsApp
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("wifi")
@pytest.mark.wifi
@pytest.mark.sanity
@pytest.mark.repeat(Config.TEST_ITERATION_COUNT)
class TestWiFiSanity:
    @pytest.mark.module
    def test_enable_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to turn on the wifi using command
        Test Procedure:
            1. Connect H4 using debug cable with hostPC
            2. Execute the following commands
                a. adb devices (H4 device will be listed)
                b. adb root
                c. adb shell ats wifi -disable
                d. adb shell ats wifi -enable
            3. Verify wifi is enabled by "adb shell settings get global wifi_on".
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Enable wifi using the command"
        test.expected_result = "Wifi can be enabled by the command"
        test.expected_resp = "on"
        try:
            dut.clear_device_logs()
            self.wifi.disable_wifi()
            self.wifi.enable_wifi()
            Utils.time_delay_s(3)
            test.actual_resp = self.wifi.get_current_wifi_status()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = summary[test.id] if summary[test.id] == "FAIL" else Utils.get_pass_fail_str(test.status)
            assert test.status
    
    @pytest.mark.module
    def test_disable_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to turn off the wifi using command
        Test Procedure:
            1. Connect H4 using debug cable with hostPC
            2. Execute the following commands
                a. adb devices (H4 device will be listed)
                b. adb root
                c. adb shell ats wifi -enable
                d. adb shell ats wifi -disable
            3. Verify wifi is disabled by "adb shell settings get global wifi_on"
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Disable wifi using the command"
        test.expected_result = "Wifi can be disabled by the command"
        test.expected_resp = "off"
        try:
            dut.clear_device_logs()
            self.wifi.enable_wifi()
            self.wifi.disable_wifi()
            Utils.time_delay_s(3)
            test.actual_resp = self.wifi.get_current_wifi_status()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.module
    def test_scan_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to scan for wifi networks using command,
            and only four networks should be detected
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Scan wifi using the command"
        test.expected_result = "DUT can detect the available networks"
        test.expected_resp = f"{Config.SSID} is in the network list"
        try:
            dut.clear_device_logs()
            ssids = self.wifi.scan_network()
            if isinstance(ssids, str):
                test.actual_resp = ssids
                test.status = False
            else:
                test.status = Config.SSID in ssids
                test.actual_resp = f"Scanned SSIDs: {ssids}"
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.module
    def test_connect_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to connect to a network using command
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Connect to a wifi network by command"
        test.expected_result = "Wifi gets connected without any issue"
        test.expected_resp = f"Wifi is connected to \"{Config.SSID}\""
        try:
            dut.clear_device_logs()
            self.wifi.enable_wifi()
            self.wifi.remove_all_saved_networks()
            self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            Utils.time_delay_s(2)
            test.actual_resp = dut.run_command("cmd wifi status | sed -n '/Wifi is connected to/p'")
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.module
    def test_disconnect_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to disconnect from a network using command
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Disconnect from a wifi network by command"
        test.expected_result = "Wifi gets connected without any issue"
        test.expected_resp = "Wifi is enabled\nWifi is not connected"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.wifi.disconnect_wifi_network()
            test.actual_resp = dut.run_command("cmd wifi status | sed -n '/Wifi is /p'")
            self.wifi.disable_wifi()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status
    
    @pytest.mark.module
    def test_reconnect_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to reconnect to a saved network using command
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Reconnect to a saved wifi network by command"
        test.expected_result = "Wifi gets reconnected without any issue"
        test.expected_resp = f"Wifi is connected to \"{Config.SSID}\""
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected() or self.wifi.get_current_network_ssid() != Config.SSID:
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.wifi.disconnect_wifi_network()
            self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            test.actual_resp = dut.run_command("cmd wifi status | sed -n '/Wifi is connected to/p'")
            self.wifi.disable_wifi()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.module
    def test_forget_wifi(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to forget a network using command
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Forget a wifi network by command"
        test.expected_result = "DUT can forget wifi by command"
        test.expected_resp = f"\"{Config.SSID}\" is not in saved networks"
        try:
            dut.clear_device_logs()
            if self.wifi.get_current_network_ssid() != Config.SSID:
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.wifi.remove_saved_network(Config.SSID)
            test.status = not self.wifi.check_ssid_in_saved_networks(Config.SSID)
            test.actual_resp = dut.run_command("cmd wifi list-networks")
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_enable_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Turn on the wifi from default UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn on wifi from Settings app"
        test.expected_result = "Wifi can be turned on from Settings app"
        test.expected_resp = "on"
        try:
            dut.clear_device_logs()
            self.wifi.disable_wifi()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.switch_wifi_toggle()
            test.actual_resp = self.wifi.get_current_wifi_status()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_disable_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Turn off the wifi from default UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn off wifi from Settings app"
        test.expected_result = "Wifi can be turned off from Settings app"
        test.expected_resp = "off"
        try:
            dut.clear_device_logs()
            self.wifi.enable_wifi()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.switch_wifi_toggle()
            test.actual_resp = self.wifi.get_current_wifi_status()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_scan_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to scan for wifi networks from UI
            and only four networks should be detected
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Scan wifi from settings UI"
        test.expected_result = "DUT can scan for the available networks"
        test.expected_resp = "With the wifi scan trim down, at most 4 APs should be displayed"
        try:
            dut.clear_device_logs()
            self.wifi.enable_wifi()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            Utils.time_delay_s(7)
            wifi_list = settings.get_wifi_scan_result()
            test.actual_resp = f"WiFi scan result: {wifi_list}"
            if self.wifi.is_wifi_connected():
                test.status = len(wifi_list) <= 5
            else:
                test.status = len(wifi_list) <= 4
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_connect_new_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Connect to a new wifi network from default UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Connect to a new network from setting UI"
        test.expected_result = "DUT can connect to wifi from setting UI"
        test.expected_resp = f"Wifi is connected to \"{Config.SSID}\""
        try:
            dut.clear_device_logs()
            self.wifi.remove_saved_network(Config.SSID)
            self.wifi.enable_wifi()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.select_ssid(Config.SSID)
            settings.enter_wifi_password(Config.PASSWORD)
            Utils.time_delay_s(3)
            test.actual_resp = dut.run_command("cmd wifi status | sed -n '/Wifi is connected to/p'")
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_disconnect_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Disconnect from a wifi network from default UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Disconnect from a wifi network from setting UI"
        test.expected_result = "DUT can disconnect wifi from setting UI"
        test.expected_resp = "Wifi is enabled\nWifi is not connected"
        try:
            dut.clear_device_logs()
            # if self.wifi.get_current_network_ssid() != Config.SSID:
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            current_ssid = self.wifi.get_current_network_ssid()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.select_ssid(current_ssid)
            settings.disconnect_wifi()
            test.actual_resp = dut.run_command("cmd wifi status | sed -n '/Wifi is /p'")
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_connect_saved_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Connect to a saved wifi network from default UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Connect to a saved network from setting UI"
        test.expected_result = "DUT can reconnect to a saved network from setting UI"
        test.expected_resp = f"Wifi is connected to \"{Config.SSID}\""
        wait_time = 10
        try:
            dut.clear_device_logs()
            self.wifi.enable_wifi()
            if not self.wifi.check_ssid_in_saved_networks(Config.SSID):
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            if self.wifi.is_wifi_connected():
                settings.select_ssid(Config.SSID)
                settings.disconnect_wifi()
                settings.connect_wifi()
            else:
                settings.select_ssid(Config.SSID)
            Utils.time_delay_s(wait_time)
            test.actual_resp = dut.run_command("cmd wifi status | sed -n '/Wifi is connected to/p'")
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_forget_wifi_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Forget a wifi network from default UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Forget a network from setting UI"
        test.expected_result = "DUT can forget a network from setting UI"
        test.expected_resp = f"\"{Config.SSID}\" is not in saved networks"
        try:
            dut.clear_device_logs()
            if self.wifi.get_current_network_ssid() != Config.SSID:
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.select_ssid(Config.SSID)
            settings.forget_wifi()
            test.actual_resp = dut.run_command("cmd wifi list-networks")
            test.status = not self.wifi.check_ssid_in_saved_networks(Config.SSID)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.ironman
    @pytest.mark.skip
    def test_enable_wifi_from_ironman(self, request, test, dut, summary):
        """
        Test Objective:
            Turn on wifi on H4 UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn on wifi from Ironman UI"
        test.expected_result = "Wifi can be turned on from Ironman UI"
        test.expected_resp = "on"
        try:
            dut.clear_device_logs()
            self.wifi.disable_wifi()
            ironman = Ironman(dut)
            ironman.switch_wifi_status()
            test.actual_resp = self.wifi.get_current_wifi_status()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status
    
    @pytest.mark.ironman
    @pytest.mark.skip
    def test_disable_wifi_from_ironman(self, request, test, dut, summary):
        """
        Test Objective:
            Turn off wifi on H4 UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn off wifi from Ironman UI"
        test.expected_result = "Wifi can be turned off from Ironman UI"
        test.expected_resp = "off"
        try:
            dut.clear_device_logs()
            self.wifi.enable_wifi()
            ironman = Ironman(dut)
            ironman.switch_wifi_status()
            test.actual_resp = self.wifi.get_current_wifi_status()
            test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status
    
