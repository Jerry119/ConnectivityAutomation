import pytest
import threading

from lib.config import Config
from lib.global_constants import GlobalConstants as Global
from lib.logger.logger import Logger
from lib.settings_app import SettingsApp
from lib.utils import Utils
from lib.wifi_iperf import WiFiIperf

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("wifi")
@pytest.mark.wifi
@pytest.mark.performance
@pytest.mark.repeat(Config.TEST_ITERATION_COUNT)
class TestWiFiPerformance:
    @pytest.mark.module
    def test_throughput_with_iperf3(self, request, test, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Measure network throughput using iperf3"
        test.expected_result = "Measure network throughput using iperf3"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            iperf_server = WiFiIperf(dut)
            iperf_server.start_iperf3_server()
            read_rssi_thread = threading.Thread(target=iperf_server.read_rssi_values)
            read_rssi_thread.start()
            iperf_server.run_iperf3_client("iperf3 -c %s -p %s -n 50M")
            iperf_server.stop_rssi_reading()
            resp = iperf_server.stop_iperf3_server()
            ssid = self.wifi.get_current_network_ssid()
            test.actual_resp = f"SSID: {ssid}\n" + iperf_server.parse_iperf_result(resp)
            test.status = True
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_latency_to_establish_new_connection(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Time to establish a new WiFI connection

        Test Procedure:
            1. Turn ON H4 and connect H4 using debug cable with hostPC
            2. Remove saved network if any
            3. Establish wifi connection using command
            4. Verify the time to establish network connection using device log.
        Expected Result:
            Time for Wi-Fi connection to be established is less than 1s
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Latency to establish a new connection"
        test.expected_result = "Less than 1s"
        start_log_text = "I WifiHAL : event received NL80211_CMD_VENDOR"
        end_log_text = "I wpa_supplicant: wlan0: CTRL-EVENT-CONNECTED"
        test.expected_resp = "0-1"
        wait_time = 10
        try:
            dut.clear_device_logs()
            self.wifi.remove_saved_network(Config.SSID)
            self.wifi.enable_wifi()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.select_ssid(Config.SSID)
            settings.enter_wifi_password(Config.PASSWORD)
            Utils.time_delay_s(wait_time)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            test.actual_resp = dut.get_latency_between_two_logs(start_log_text, end_log_text)
            if test.actual_resp is None:
                test.additional_info = f"DUT has not been connected to the network in {wait_time}s"
                test.status, test.actual_resp = False, f">{wait_time}s"
            else:
                test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_latency_to_auto_reassociate_connection(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Time for Wi-Fi connection to be establlish from disable state

        Test Procedure:
            1. Turn ON H4 and connect H4 using debug cable with hostPC, make sure wifi network has been connected before
            2. Disable DUT wifi
            3. Enable DUT wifi
            4. Verify the time to re-establish network connection using device log.
        Expected Result:
            Time for Wi-Fi connection to be established is less than 1s
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Latency from wake to wifi connection established"
        test.expected_result = "Less than 1s"
        start_log_text = "isWifiEnabled: Wifi is now enabled"
        end_log_text = "I wpa_supplicant: wlan0: CTRL-EVENT-CONNECTED"
        test.expected_resp = "0-1"
        wait_time = 10
        try:
            dut.clear_device_logs()
            if not self.wifi.saved_network_exist():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.wifi.disable_wifi()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.switch_wifi_toggle()
            Utils.time_delay_s(wait_time)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            test.actual_resp = dut.get_latency_between_two_logs(start_log_text, end_log_text)
            if test.actual_resp is None:
                test.additional_info = f"DUT has not been reconnected to the network in {wait_time}s"
                test.status, test.actual_resp = False, f">{wait_time}s"
            else:
                test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_latency_to_disconnect_from_network(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Time for disconnecting WiFi from idle state
        Expected Result:
            Time for Wi-Fi disconnection is less than 1s
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Latency to disconnect from a wifi network"
        test.expected_result = "Less than 1s"
        start_log_text = "I WifiHAL : event received NL80211_CMD_VENDOR"
        end_log_text = "I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED"
        test.expected_resp = "0-1"
        wait_time = 5
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            current_ssid = self.wifi.get_current_network_ssid()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_wifi_setting_page()
            settings.select_ssid(current_ssid)
            settings.disconnect_wifi()
            Utils.time_delay_s(wait_time)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            test.actual_resp = dut.get_latency_between_two_logs(start_log_text, end_log_text)
            if test.actual_resp is None:
                test.additional_info = f"DUT has not been disconnected from the network in {wait_time}s"
                test.status, test.actual_resp = False, f">{wait_time}s"
            else:
                test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    