import re

from lib.adb import ADBInterface, AdbProxy
from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class H4(AdbProxy):
    def __init__(self, interface=None, dut_index=0):
        if interface is None:
            self.interface = ADBInterface()
        else:
            self.interface = interface
        self.device = self.interface.get_dut(dut_index)
        super().__init__(self.device)

    def go_to_default_ui(self):
        DEFAULT_UI = "set_home default"
        # SETENFORCE = "setenforce 0"
        try:
            self.root()
            # self.run_command(SETENFORCE)
            # self.run_command(DEFAULT_UI)
            Utils.time_delay_s(5)
        except Exception as e:
            logger.debug(f"Exception occurred while switching to Ironman UI | ERROR: {e}")

    def go_to_ironman_ui(self):
        IRONMAN_UI = "set_home ironman"
        try:
            self.root()
            self.run_command(IRONMAN_UI)
            Utils.time_delay_s(5)
        except Exception as e:
            logger.debug(f"Exception occurred while switching to Ironman UI | ERROR: {e}")
    
    def click(self, tap_x, tap_y):
        """
        This method is used to click on the DUT screen based on the coordinates value.
        """
        cmd = "input tap {0} {1}".format(tap_x, tap_y)
        self.run_command(cmd)
        Utils.time_delay_s(2)
    
    def long_press(self, tap_x, tap_y):
        """
        This method is used to long press the DUT screen based on the coordinates value.
        """
        cmd = f"input swipe {tap_x} {tap_y} {tap_x} {tap_y} 1000"
        self.run_command(cmd)
        Utils.time_delay_s(2)
    
    def go_to_notification_screen(self):
        cmd = "input keyevent 83"
        self.run_command(cmd)
        Utils.time_delay_s(1)
    
    def go_back_to_prev_screen(self):
        cmd = "input keyevent 4"
        self.run_command(cmd)
        # Utils.time_delay_s(1)
    
    def grant_audio_call_permission(self):
        self.run_command("pm grant com.android.dialer android.permission.CALL_PHONE")
        self.run_command("pm grant com.android.dialer android.permission.READ_PHONE_STATE")
        self.run_command("pm grant com.android.dialer android.permission.READ_CONTACTS")
        self.run_command("pm grant com.android.dialer android.permission.WRITE_CONTACTS")
    
    def grant_music_app_permission(self):
        self.run_command("pm grant com.android.music android.permission.READ_PHONE_STATE")

    def get_reboot_reason(self):
        """
        [persist.sys.boot.reason]: []
        [persist.sys.boot.reason.history]: [reboot,ota,1690826815
        [ro.boot.bootreason]: [reboot,ota]
        [sys.boot.reason]: [reboot,ota]
        [sys.boot.reason.last]: [reboot,]
        """
        self.run_command("getprop | grep reason")
