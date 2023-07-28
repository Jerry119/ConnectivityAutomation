import pytest

from lib.config import Config
from lib.global_constants import GlobalConstants as Global
from lib.logger.logger import Logger
from lib.settings_app import SettingsApp
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


@pytest.mark.usefixtures("wifi")
@pytest.mark.wifi
class TestWiFiIntegration:
    @pytest.mark.module
    def test_wifi_scan(self, request, test, dut, summary):
        pass