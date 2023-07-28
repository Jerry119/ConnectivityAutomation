import pytest
import threading

from lib.config import Config
from lib.logger.logger import Logger
from lib.global_constants import GlobalConstants as Global
from lib.settings_app import SettingsApp
from lib.utils import Utils
from lib.wifi_iperf import WiFiIperf

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("bluetooth")
@pytest.mark.usefixtures("wifi")
@pytest.mark.coex
class TestCoEx:
    def test_tcp_throughput_baseline(self, request, test, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        iperf_run_time = 60
        test.objective = "Measure baseline TCP throughput using iperf3"
        # test.expected_result = f"Measure baseline TCP throughput using iperf3"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            iperf_server = WiFiIperf(dut)
            iperf_server.start_iperf3_server()
            cmd = f"iperf3 -c %s -p %s -t {iperf_run_time}"
            iperf_server.run_iperf3_client(cmd)
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
    def test_tcp_throughput_with_bt_scan_10(self, request, test, appium_server, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        bt_scan_time = 10
        iperf_run_time = 60
        time_for_one_cycle = 30
        test.objective = f"Measure network throughput using iperf3 while BT is scanning for {bt_scan_time}"
        # test.expected_result = f"Measure network TCP throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            iperf_server = WiFiIperf(dut)
            iperf_server.start_iperf3_server()
            cmd = f"iperf3 -c %s -p %s -t {iperf_run_time}"
            iperf_client_thread = threading.Thread(target=iperf_server.run_iperf3_client, args=(cmd,))
            iperf_client_thread.start()
            cnt = 0
            # now = time.time()
            while cnt < iperf_run_time / time_for_one_cycle:
                settings.initiate_bluetooth_scan(bt_scan_time)
                settings.go_back_to_prev_screen()
                Utils.time_delay_s(time_for_one_cycle-bt_scan_time)
                cnt += 1
            # duration = time.time() - now
            # logger.debug(f"duration: {duration}")
            iperf_client_thread.join()
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
    def test_tcp_throughput_with_bt_scan_12(self, request, test, appium_server, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        bt_scan_time = 12.5
        iperf_run_time = 60
        time_for_one_cycle = 30
        test.objective = f"Measure network throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        # test.expected_result = f"Measure network TCP throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            iperf_server = WiFiIperf(dut)
            iperf_server.start_iperf3_server()
            cmd = f"iperf3 -c %s -p %s -t {iperf_run_time}"
            iperf_client_thread = threading.Thread(target=iperf_server.run_iperf3_client, args=(cmd,))
            iperf_client_thread.start()
            cnt = 0
            while cnt < iperf_run_time / time_for_one_cycle:
                settings.initiate_bluetooth_scan(bt_scan_time)
                settings.go_back_to_prev_screen()
                Utils.time_delay_s(time_for_one_cycle-bt_scan_time)
                cnt += 1
            iperf_client_thread.join()
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
    def test_udp_throughput_with_bt_scan_10(self, request, test, appium_server, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        bt_scan_time = 10
        iperf_run_time = 60
        time_for_one_cycle = 30
        test.objective = f"Measure network UDP throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        # test.expected_result = f"Measure network UDP throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            iperf_server = WiFiIperf(dut)
            iperf_server.start_iperf3_server()
            cmd = f"iperf3 -c %s -u -p %s -t {iperf_run_time}"
            iperf_client_thread = threading.Thread(target=iperf_server.run_iperf3_client, args=(cmd,))
            iperf_client_thread.start()
            cnt = 0
            while cnt < iperf_run_time / time_for_one_cycle:
                settings.initiate_bluetooth_scan(bt_scan_time)
                settings.go_back_to_prev_screen()
                Utils.time_delay_s(iperf_run_time-bt_scan_time)
                cnt += 1
            iperf_client_thread.join()
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
    def test_udp_throughput_with_bt_scan_12(self, request, test, appium_server, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        bt_scan_time = 12.5
        iperf_run_time = 60
        time_for_one_cycle = 30
        test.objective = f"Measure network UDP throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        # test.expected_result = f"Measure network UDP throughput using iperf3 while BT is scanning for {bt_scan_time}s"
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            iperf_server = WiFiIperf(dut)
            iperf_server.start_iperf3_server()
            cmd = f"iperf3 -c %s -u -p %s -t {iperf_run_time}"
            iperf_client_thread = threading.Thread(target=iperf_server.run_iperf3_client, args=(cmd,))
            iperf_client_thread.start()
            cnt = 0
            while cnt < iperf_run_time / time_for_one_cycle:
                settings.initiate_bluetooth_scan(bt_scan_time)
                settings.go_back_to_prev_screen()
                Utils.time_delay_s(iperf_run_time-bt_scan_time)
                cnt += 1
            iperf_client_thread.join()
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