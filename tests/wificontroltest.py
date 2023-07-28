import pytest

from lib.wificontrol import WiFiControl
from lib.cmd_execute import execute_shell_cmd


class TestWiFiControl:
    wifi = WiFiControl()
    
    def test_enable_wifi(self):
        self.wifi.enable_wifi()
        # assert "Wifi is enabled" in output_cmd("adb shell cmd wifi status")
        assert "Wifi is enabled" in execute_shell_cmd(self.wifi.device, "cmd wifi status")

    def test_disable_wifi(self):
        pass

    def test_connect_to_wifi(self):
        ssid, pwd = "hdevice", "Figure-Crepe9-Confound"
        self.wifi.connect_to_wifi(ssid, pwd)
        assert f"Wifi is connected to \"{ssid}\"" in execute_shell_cmd(self.wifi.device, "cmd wifi status")