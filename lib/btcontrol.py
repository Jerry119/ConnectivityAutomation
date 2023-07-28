from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class BTControl():
    def __init__(self, device):
        self.device = device

    def enable_bt(self):
        try:
            cmd = "ats bt -enable"
            if self.get_current_bt_status() == "on":
                return
            self.device.run_command(cmd)
            Utils.time_delay_s(1)
        except Exception as e:
            logger.exception(f"Exception occurred while enabling BT | ERROR: {e}")
    
    def disable_bt(self):
        try:
            cmd = "ats bt -disable"
            if self.get_current_bt_status() == "off":
                return
            self.device.run_command(cmd)
            Utils.time_delay_s(1)
        except Exception as e:
            logger.exception(f"Exception occurred while disabling BT | ERROR: {e}")
    
    def get_current_bt_status(self):
        """
        Get current BT enabled / disabled status of the device
        """
        try:
            bt_cmd = "settings get global bluetooth_on"
            bt_status = str(self.device.run_command(bt_cmd)).strip()
            bt_status_str = {"0": "off", "1": "on"}
            return bt_status_str.get(bt_status, None)
        except Exception as e:
            logger.exception(
                "Exception occurred while getting current bluetooth "
                "status | ERROR: %s" % e
            )
            return None

    def get_current_bt_profile(self):
        bt_name = None
        try:
            cmd = "dumpsys bluetooth_manager | grep -E 'mDevice:.+state=Connected$'"
            resp = self.device.run_command(cmd)
            bt_name = resp.split("(")[1].split(")")[0]
            return bt_name
        except Exception as e:
            logger.exception(f"Exception occurred while getting current bluetooth profile | ERROR: {e}")
            return None
    
    def is_bluetooth_connected(self):
        try:
            cmd = "dumpsys bluetooth_manager | sed -n '/ConnectionState:*/p'"
            connected_state = self.device.run_command(cmd)
            if "STATE_DISCONNECTED" in connected_state:
                logger.info("The bluetooth is not connected")
                return False
            elif "STATE_CONNECTED" in connected_state:
                logger.info("The bluetooth is connected")
                return True
        except Exception as e:
            logger.exception(f"Exception occurred while getting bluetooth connection status | {e}")
            return False

    def has_prev_bonded_bt_devices(self):
        try:
            cmd = "dumpsys bluetooth_manager | sed -n '/Bonded devices:/,/mSnoopLogSettingAtEnable/p'"
            resp = self.device.run_command(cmd).split("\n")
            return len(resp) > 2
        except Exception as e:
            logger.exception(f"Exception occurred while checking bonded BT devices | {e}")
            return False

    def check_device_is_bonded(self, bt_name):
        try:
            cmd = "dumpsys bluetooth_manager | sed -n '/Bonded devices:/,/mSnoopLogSettingAtEnable/p'"
            resp = self.device.run_command(cmd)
            return bt_name in resp
        except Exception as e:
            logger.exception(f"Exception occurred while checking bonded BT devices | {e}")
            return False