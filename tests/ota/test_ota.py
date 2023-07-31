import pytest

from lib.battery_api import BatteryAPI
from lib.config import Config
from lib.global_constants import GlobalConstants as Global
from lib.logger.logger import Logger
from lib.settings_app import SettingsApp
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("wifi")
@pytest.mark.ota
class TestOTA:
    @pytest.mark.aosp
    def test_ota_normal_condition(self, request, test, appium_server, dut, summary):
        """
        Test Objective:
            Device can only take the standard OTA update when battery > 80, under charging, and connected to wifi
        """
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Trigger OTA update from H4"
        test.expected_result = "DUT can only take the standard OTA update when battery > 80, under charging, and connected to wifi"
        test.expected_resp = f"Updated build should be later than the current build: \"{self.dut.build_version}\""
        min_battery = 80
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            battery = BatteryAPI(dut)
            battery.charge_battery_to_level(min_battery)
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.scroll_down()
            settings.go_to_software_update()
            settings.check_and_download_update()
            test.status = True
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status