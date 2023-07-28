import pytest

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
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Initiate OTA update from H4"
        test.expected_result = "DUT can start OTA update under normal condition"
        # test.expected_resp = ""
        try:
            dut.clear_device_logs()
            if not self.wifi.is_wifi_connected():
                self.wifi.connect_to_ssid(Config.SSID, Config.PASSWORD)
            settings = SettingsApp(dut, Config.SETTING_APP_CONFIG)
            settings.launch_app()
            settings.scroll_down()
            settings.go_to_software_update()
            test.status = True
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status