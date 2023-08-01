import os
import re
import shlex
import subprocess

from lib.global_constants import GlobalConstants as Global
from lib.logger.logger import Logger
from lib.utils import Utils

from ppadb.client import Client as AdbClient

logger = Logger(logger_name=__name__).logger

# This class creates an object which holds a connection to the ADB server open,
# allowing for stateful communication to the Android device for scripted test purposes

DUTS = ["atoll", "sdk_gphone64_arm64"]
ROOT_USER_ID = '0'


class ADBInterface:
    __client = None
    __devices = []
    duts = []

    def __init__(self, client=None):

        if client is None:
            try:
                self.__devices = self._find_adb_devices()
            except Exception:
                command = "adb start-server"
                subprocess.run(shlex.split(command))
                Utils.time_delay_s(10)
                self.__devices = self._find_adb_devices()
        else:
            self.__client = client

        for device in self.__devices:
            self._update_device_list(device)

    def _find_adb_devices(self):
        self.__client = AdbClient(
            host="127.0.0.1", port=5037
        )
        devices = self.__client.devices()
        if len(devices) == 0:
            raise Exception("No Device Connected")
        return devices

    @classmethod
    def _update_device_list(cls, device):
        response = device.shell("getprop ro.product.name").strip()
        if response in DUTS:
            cls.duts.append(device)

    def get_dut(self, dut_index):
        return self.duts[dut_index]

class AdbProxy:
    def __init__(self, device):
        self.test_id = None
        self.device = device
        self.id = self.device.serial
        self.log_file_path = None
        self.root()
        self.build_branch = self.get_prop("ro.build.branch")
        self.build_version = self.get_prop("ro.build.version.incremental")
        self.build_flavor = self.get_prop("ro.build.flavor")
        self.type = self.get_prop("ro.product.name")

    def run_command(self, command, timeout=Global.ADB_SHELL_DEFAULT_RUN_WAIT):
        try:
            logger.debug("Device: %s | cmd: %s" % (self.id, command))
            resp = self.device.shell(command, timeout=timeout).strip()
            if (
                "logcat" not in command
            ):  # To avoid printing logcat response to console
                logger.debug("Response: %s" % resp)
            Utils.time_delay_s(1)
            return resp
        except Exception as e:
            logger.exception(
                "Exception occurred while running the command: %s | "
                "ERROR: %s" % (command, e)
            )
            return None
        
    def wait_for_device(self):
        try:
            logger.info("waitting for device to come online.")
            subprocess.run("adb wait-for-device", shell=True, timeout=30)
        except Exception as e:
            logger.exception(f"DUT did not come back after reboot. ERROR | {e}")

    def _get_user_id(self):
        """Returns the adb user. Either 2000 (shell) or 0 (root)."""
        return self.device.shell('id -u')
    
    def is_root(self, user_id=None):
        """Checks if the user is root.

        Args:
            user_id: if supplied, the id to check against.
        Returns:
            True if the user is root. False otherwise.
        """
        if not user_id:
            user_id = self._get_user_id()
        return user_id == ROOT_USER_ID

    def collect_adb_logcat(self, test_id):
        self.test_id = test_id
        self.device.shell("logcat -v threadtime -b all -d", handler=self.dump_logcat)

    def dump_logcat(self, connection):
        try:
            logger.debug("Collecting ADB logs...")
            self.log_file_path = os.path.join(Global.LOG_DIR, "%s_adb_logcat_%s_%s.log" % (self.test_id, self.id, Utils.get_current_time_with_format("%Y_%m_%d_%H_%M_%S")))
            while True:
                data = connection.read(1024)
                if not data:
                    break
                data_val = data.decode(encoding="utf-8", errors="ignore")
                with open(self.log_file_path, "a", encoding="utf-8") as f:
                    f.write(data_val)
            connection.close()
            logger.debug("Collected adb logcat")
        except Exception as e:
            logger.error(
                "Exception occurred while collecting adb logcat of {0} | Error {1}".format(
                    self.id, e
                )
            )

    def get_id(self):
        return self.id

    def get_prop(self, prop):
        return self.run_command("getprop {}".format(prop))

    def root(self):
        try:
            if not self.is_root():
                self.device.root()
                Utils.time_delay_s(3)
        except RuntimeError:
            pass
        except Exception as e:
            logger.debug(f"Exception occurred while running adb as root | ERROR: {e}")

    def remount(self):
        try:
            self.device.remount()
            Utils.time_delay_s(3)
        except Exception as e:
            logger.debug(f"Exception occurred while remounting device | ERROR: {e}")

    def reboot(self):
        try:
            self.device.reboot()
            Utils.time_delay_s(50)
            self.device.root()
        except Exception as e:
            logger.debug(f"Exception occurred while rebooting device | ERROR: {e}")

    def clear_device_logs(self, retry=3):
        """
        Clears adb logs from device
        """
        try:
            if retry == 0:
                return False
            resp = self.run_command("logcat -c")
            if resp is None:
                Utils.time_delay_s(10)
                logger.info("Retrying clear device logs")
                return self.clear_device_logs(retry - 1)
            return True
        except Exception as e:
            logger.exception(
                f"Exception occurred while clearing device logs | ERROR: {e}"
            )
            return False
    
    def get_latency_between_two_logs(self, start_str, end_str):
        result = None
        with open(self.log_file_path, "r") as f:
            lines = f.readlines()
        ss = list(filter(re.compile(f".*{start_str}.*").match, lines))
        if len(ss) <= 0:
            logger.warning(f"Failed to find text \"{start_str}\" in the log")
            return result
        es = list(filter(re.compile(f".*{end_str}.*").match, lines))
        if len(es) <= 0:
            logger.warning(f"Failed to find text \"{end_str}\" in the log")
            return result
        result = Utils.get_time_diff_from_log_lines(ss, es)
        return result
    
    def check_existence_in_log(self, test_str):
        with open(self.log_file_path, "r") as f:
            content = f.readlines()
        keyword = list(filter(re.compile(f".*{test_str}.*").match, content))
        if len(keyword) > 0:
            return keyword[-1]
        return None

    def push_file(self, src_path, dest_path):
        try:
            self.device.push(src_path, dest_path)
        except Exception as e:
            logger.exception(
                "Exception occurred while pushing the file to device "
                "device logs | ERROR: %s" % e
            )
    
    def sync_device_time(self):
        """
        Sync the device time with system time
        """
        try:
            self.root()
            cur_time = Utils.get_current_time_with_format("%m%d%H%M%Y.%S")
            self.run_command("date %s" % cur_time)
        except Exception as e:
            logger.exception("Exception while syncing device time | ERROR: %s" % e)