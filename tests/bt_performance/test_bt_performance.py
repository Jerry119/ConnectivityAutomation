import pytest

from lib.config import Config
from lib.logger.logger import Logger
from lib.global_constants import GlobalConstants as Global
from lib.settings_app import SettingsApp
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("bluetooth")
@pytest.mark.bluetooth
@pytest.mark.performance
class TestBluetoothPerformance:
    @pytest.mark.aosp
    def test_bt_on_off_10_times(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Turn on/off BT on dut 10 times, make sure the functionality doesn't crash
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn on/off BT on dut 10 times"
        test.expected_result = "BT functionality does not break"
        test.expected_resp = "dut can connect to BT headset after on/off 10 times"
        try:
            dut.clear_device_logs()
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            settings.forget_bluetooth_devices()
            settings.go_to_notification()
            attempt = 0
            while attempt < 20:
                settings.tap_on_bt_icon()
                attempt += 1
            settings.dismiss_notification()
            settings.initiate_bluetooth_scan(15)
            settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
            test.status = self.bluetooth.is_bluetooth_connected()
            if test.status:
                test.actual_resp = f"dut is able to connect to BT headset after on/off 10 times"
            else:
                test.actual_resp = f"dut failed to connect to BT headset after on/off 10 times"
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status
    
    @pytest.mark.aosp
    def test_latency_to_auto_reassociate_bt(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Auto re-associate with BT headset when dut back in range
        Test Procedures:
            1. Pair with BT test device
            2. Disable BT on dut
            3. Enable BT on dut 
            4. Wait for re-association
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Auto re-associate with BT headset"
        test.expected_result = "DUT can auto re-associate with BT headset in less than 3s when back in range"
        test.expected_resp = "0-3"
        start_log_text = "D BluetoothManagerService: Sending BLE State Change: OFF > BLE_TURNING_ON"
        end_log_text = "D BluetoothA2dp: Proxy object connected"
        wait_time = 10
        try:
            dut.clear_device_logs()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            if self.bluetooth.is_bluetooth_connected():
                pass
            elif self.bluetooth.check_device_is_bonded(Config.TEST_BT_DEVICE):
                settings.pair_saved_bluetooth_device(Config.TEST_BT_DEVICE)
            else:
                settings.initiate_bluetooth_scan(3)
                settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
            self.bluetooth.disable_bt()
            self.bluetooth.enable_bt()
            Utils.time_delay_s(wait_time)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            test.actual_resp = dut.get_latency_between_two_logs(start_log_text, end_log_text)
            if test.actual_resp is None:
                test.additional_info = f"DUT has not been re-associated with BT headset in {wait_time}s"
                test.status, test.actual_resp = False, f">{wait_time}s"
            else:
                test.status = Utils.kpi_validation(test.expected_resp, test.actual_resp)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

