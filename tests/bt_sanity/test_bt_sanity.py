import pytest

from lib.config import Config
from lib.logger.logger import Logger
from lib.global_constants import GlobalConstants as Global
from lib.music_app import MusicApp
from lib.settings_app import SettingsApp
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("bluetooth")
@pytest.mark.bluetooth
@pytest.mark.sanity
class TestBluetoothSanity:
    @pytest.mark.module
    def test_enable_bluetooth(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to turn on the BT
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Enable BT using the command"
        test.expected_result = "Bluetooth can be enabled by command"
        test.expected_resp = "on"
        try:
            dut.clear_device_logs()
            self.bluetooth.disable_bt()
            self.bluetooth.enable_bt()
            Utils.time_delay_s(3)
            test.actual_resp = self.bluetooth.get_current_bt_status()
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
    def test_disable_bluetooth(self, request, test, dut, summary):
        """
        Test Objective:
            Device is able to turn off the BT
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Disable BT using the command"
        test.expected_result = "Bluetooth can be disabled by command"
        test.expected_resp = "off"
        try:
            dut.clear_device_logs()
            self.bluetooth.enable_bt()
            self.bluetooth.disable_bt()
            Utils.time_delay_s(3)
            test.actual_resp = self.bluetooth.get_current_bt_status()
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
    def test_enable_bluetooth_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to turn on BT from UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn on BT from UI"
        test.expected_result = "DUT can turn on BT from UI"
        test.expected_resp = "on"
        try:
            dut.clear_device_logs()
            self.bluetooth.disable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_notification()
            settings.tap_on_bt_icon()
            settings.dismiss_notification()
            test.actual_resp = self.bluetooth.get_current_bt_status()
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
    def test_disable_bluetooth_from_settings(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to turn off BT from UI
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Turn off BT from UI"
        test.expected_result = "DUT can turn off BT from UI"
        test.expected_resp = "off"
        try:
            dut.clear_device_logs()
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_notification()
            settings.tap_on_bt_icon()
            settings.dismiss_notification()
            test.actual_resp = self.bluetooth.get_current_bt_status()
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
    def test_scan_bluetooth(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to scan for BT devices
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Scan for BT devices"
        test.expected_result = "DUT can discover BT headset devices"
        test_str = "D BluetoothAdapterService: startDiscovery"
        test.expected_resp = "BT headsets in pairing mode should be displayed"
        try:
            dut.clear_device_logs()
            self.bluetooth.enable_bt()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            settings.initiate_bluetooth_scan(10)
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            resp = dut.check_existence_in_log(test_str)
            if resp is not None:
                test.status = True
                bt_list = settings.get_bt_scan_result()
                test.actual_resp = resp + f"bluetooth scan result: {bt_list}"
            else:
                test.status = False
                test.actual_resp = "No bt scan detected in the logcat."
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_pair_new_bluetooth(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to pair with a new BT headset devices, make sure headset is in pairing mode
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Pair with a new BT headset device"
        test.expected_result = "DUT can pair with a new BT headset"
        test_str = "D BluetoothA2dp: Proxy object connected"
        try:
            dut.clear_device_logs()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            if self.bluetooth.check_device_is_bonded(Config.TEST_BT_DEVICE):
                settings.forget_bluetooth_devices()
            settings.initiate_bluetooth_scan(3)
            settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
            test.status = self.bluetooth.is_bluetooth_connected()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            test.actual_resp = dut.check_existence_in_log(test_str)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_audio_route_to_bt(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to auto route the auido to bt HS
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Audio routing to bluetooth headset"
        test.expected_result = "DUT can auto route audio to BT HS"
        test_str = "V MediaRouter: Audio routes updated: AudioRoutesInfo{ type=SPEAKER, bluetoothName=%s }, a2dp=true" % Config.TEST_BT_DEVICE
        try:
            dut.clear_device_logs()
            if not self.bluetooth.is_bluetooth_connected():
                settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
                settings.launch_app()
                settings.go_to_bluetooth_setting_page()
                if not self.bluetooth.check_device_is_bonded(Config.TEST_BT_DEVICE):
                    settings.initiate_bluetooth_scan(3)
                    settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
                else:
                    settings.pair_saved_bluetooth_device(Config.TEST_BT_DEVICE)
            self.bluetooth.disable_bt()
            music = MusicApp(dut, Config.MUSIC_APP_CONFIG)
            music.launch_app()
            dut.grant_music_app_permission()
            music.play_music_from_fresh()
            Utils.time_delay_s(5)
            self.bluetooth.enable_bt()
            Utils.time_delay_s(10)
            music.pause_music()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            resp = dut.check_existence_in_log(test_str)
            if resp is not None:
                test.status = True
                test.actual_resp = resp
            else:
                test.status = False
                test.actual_resp = "Audio routing is not detected in logcat"
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status
    
    @pytest.mark.aosp
    def test_disconnect_bluetooth(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to disconnect from an existing bt connection
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Disconnect from BT headset device"
        test.expected_result = "DUT can disconnect from BT headset"
        try:
            dut.clear_device_logs()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            if self.bluetooth.is_bluetooth_connected():
                # bt_name = self.bluetooth.get_current_bt_profile()
                settings.disconnect_bluetooth_connection()
            else:
                if not self.bluetooth.check_device_is_bonded(Config.TEST_BT_DEVICE):
                    settings.initiate_bluetooth_scan(3)
                    settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
                else:
                    settings.pair_saved_bluetooth_device(Config.TEST_BT_DEVICE)
                settings.disconnect_bluetooth_connection()
            test.status = not self.bluetooth.is_bluetooth_connected()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_pair_saved_bluetooth(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to pair with an existing BT headset devices, make sure headset is in pairing mode
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Pair with a bonded BT headset device"
        test.expected_result = "DUT can pair with a bonded BT headset"
        try:
            dut.clear_device_logs()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            ### establish an existing connection ###
            if not self.bluetooth.check_device_is_bonded(Config.TEST_BT_DEVICE):
                settings.initiate_bluetooth_scan(3)
                settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
            if self.bluetooth.is_bluetooth_connected():
                settings.disconnect_bluetooth_connection()
                settings.go_back_to_prev_screen()
            settings.pair_saved_bluetooth_device(Config.TEST_BT_DEVICE)
            test.status = self.bluetooth.is_bluetooth_connected()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_auto_reconnect_bluetooth(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to auto connect to prev paired BT device
        Test Procedure:
            1. DUT is paired and connected to BT headset
            2. Headset goes out of range or turned off or BT is disabled on DUT
            3. Turn on BT on headset or DUT
            4. Verify DUT should get auto reconnected to the headset
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Auto connect BT headset device"
        test.expected_result = "DUT can auto reconnect to BT headset."
        try:
            dut.clear_device_logs()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            if not self.bluetooth.is_bluetooth_connected():
                ##### connect BT if not connected #####
                if not self.bluetooth.check_device_is_bonded(Config.TEST_BT_DEVICE):
                    settings.initiate_bluetooth_scan(3)
                    settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
                else:
                    settings.pair_saved_bluetooth_device(Config.TEST_BT_DEVICE)
            self.bluetooth.disable_bt()
            self.bluetooth.enable_bt()
            settings.wait_for_auto_reconnection()
            test.status = self.bluetooth.is_bluetooth_connected()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_forget_bluetooth(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device is able to forget a BT device
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Forget BT headset device"
        test.expected_result = "DUT can forget a BT headset."
        try:
            dut.clear_device_logs()
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.go_to_bluetooth_setting_page()
            if not self.bluetooth.has_prev_bonded_bt_devices():
                settings.initiate_bluetooth_scan(3)
                settings.pair_new_bluetooth_device(Config.TEST_BT_DEVICE)
            settings.forget_bluetooth_devices()
            test.status = not self.bluetooth.has_prev_bonded_bt_devices()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status