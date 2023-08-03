import re

from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class WiFiControl():
    def __init__(self, device):
        self.device = device

    def _forget_network_id(self, id):
        """
        Forget a wifi network using id
        """
        cmd = f"cmd wifi forget-network {id}"
        self.device.run_command(cmd)
    
    def _check_action(self, action):
        """
        Check whether the given action is valid or not
        """
        action = str(action).strip().lower()
        if action not in ["on", "off"]:
            logger.info("Invalid action. Given action is: %s" % action)
            return False
        return action
    
    def _get_saved_networks(self):
        """
        Get saved network Ids
        """
        output = self.device.run_command("cmd wifi list-networks")
        if "No networks" in output:
            return [], []
        ids, ssids = set(), set()
        lines = output.strip().split("\n")
        for line in lines:
            if "Network Id" in line:
                continue
            ids.add(int(re.split(r"\s{2,}", line)[0]))
            ssids.add(re.split(r"\s{2,}", line)[1])
        return ids, ssids
    
    def saved_network_exist(self):
        """
        Check if any saved network exists
        """
        ids, _ssids = self._get_saved_networks()
        return len(ids) > 0

    def enable_wifi(self):
        """
        Enable wifi using ats command
        """
        try:
            cmd = "ats wifi -enable"
            if self.get_current_wifi_status() == "on":
                return
            self.device.run_command(cmd)
            Utils.time_delay_s(1)
        except Exception as e:
            logger.exception(f"Exception occurred while enabling WiFi | ERROR: {e}")
    
    def disable_wifi(self):
        """
        Disable wifi using ats command
        """
        try:
            cmd = "ats wifi -disable"
            if self.get_current_wifi_status() == "off":
                return
            self.device.run_command(cmd)
            Utils.time_delay_s(1)
        except Exception as e:
            logger.exception(f"Exception occurred while disabling WiFi | ERROR: {e}")
    
    def scan_network(self):
        """
        Return the wifi scan list
        """
        try:
            self.enable_wifi()
            attempt = 0
            while attempt < 5:
                self.device.run_command("cmd wifi start-scan")
                output = self.device.run_command("cmd wifi list-scan-results")
                if "No scan results" in output:
                    attempt += 1
                else:
                    break
            if "No scan results" in output:
                return "No scan results"

            output = output.split("\n")
            ssids = set()
            for i in range(1, len(output)):
                items = re.split(r"\s{2,}", output[i].strip())
                if len(items) == 6:
                    ssids.add(items[4])
            return ssids
        except Exception as e:
            logger.exception(f"Exception occurred while scanning wifi networks | ERROR: {e}")
            return set()
    
    def connect_to_ssid(self, ssid, pwd):
        """
        Connect to wifi with ssid and pwd
        """
        try:
            self.enable_wifi()
            logger.debug(f"Connecting to \"{ssid}\"")
            cmd = f"cmd wifi connect-network {ssid} wpa2 {pwd}"
            self.device.run_command(cmd)
            Utils.time_delay_s(3)
        except Exception as e:
            logger.exception(f"Exception occurred while connecting to \"{ssid}\" | ERROR: {e}")

    def disconnect_wifi_network(self):
        """
        Disconnect wifi network 
        """
        try:
            cmd = "ats wifi -disconn"
            self.device.run_command(cmd)
            Utils.time_delay_s(1)
        except Exception as e:
            logger.exception(f"Exception occurred while disconnecting wifi | ERROR: {e}")
    
    def get_current_wifi_status(self):
        """
        Get current wi-fi enabled / disabled status of the device
        """
        try:
            wifi_cmd = "settings get global wifi_on"
            wifi_status = str(self.device.run_command(wifi_cmd)).strip()
            wifi_status_str = {"0": "off", "1": "on"}
            return wifi_status_str.get(wifi_status, None)
        except Exception as e:
            logger.exception(
                "Exception occurred while getting current wi-fi "
                "status | ERROR: %s" % e
            )
            return None
    
    def is_wifi_connected(self):
        """
        Check if wifi is connected
        """
        try: 
            cmd = "cmd wifi status"
            resp = self.device.run_command(cmd)
            return "Wifi is connected to " in resp
        except Exception as e:
            logger.exception(f"Exception occurred while getting wifi connection status | {e}")
            return False

    def remove_all_saved_networks(self):
        """
        Remove all the saved networks
        """
        if not self.saved_network_exist():
            return
        ids, _ssids = self._get_saved_networks()
        for i in ids:
            self._forget_network_id(i)
    
    def remove_saved_network(self, ssid):
        """
        Remove the wifi network ssid
        """
        if not self.check_ssid_in_saved_networks(ssid):
            return
        output = self.device.run_command("cmd wifi list-networks").split("\n")
        for line in output:
            if ssid in line:
                idx = int(re.split(r"\s{2,}", line)[0])
                self._forget_network_id(idx)
                break
        
    def get_current_network_ssid(self):
        """
        Return the current wifi SSID
        """
        try: 
            cmd = "cmd wifi status | sed -n '/Wifi is connected to/p'"
            resp = self.device.run_command(cmd)
            if resp is not None and resp != "":
                ssid = resp.split('"')[1]
            else:
                ssid = None
            return ssid
        except Exception as e:
            logger.exception(f"Exception occurred while getting current wifi ssid | {e}")
            return None

    def check_ssid_in_saved_networks(self, ssid):
        """
        Check if ssid is in saved networks
        """
        _ids, ssids = self._get_saved_networks()
        return ssid in ssids