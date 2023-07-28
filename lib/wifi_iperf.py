import re
import subprocess

from lib.global_constants import (
    GlobalConstants as Global,
)
from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class WiFiIperf:
    def __init__(self, device):
        super(WiFiIperf, self).__init__()
        self.device = device
        self._server = None
        self._port = None
        self.rssi_list = []
        self.rssi_flag = False
        self._ip = self.get_device_ip()

    def get_device_ip(self):
        """
        execute ifconfig commands in shell to get ip details
        """
        try:
            # ip = self.device.run_command("ifconfig wlan0 | grep 'inet addr:' | awk -F : '{print $2}' | awk -F ' ' '{print $1}'")
            ip = subprocess.check_output("ipconfig getifaddr en0", shell=True).decode("utf-8").strip()
            logger.info(f"Host IP addr: {ip}")
            return ip
        except Exception as e:
            logger.exception(f"Exception occurred while getting Host IP | ERROR: {e}")
            return None

    def start_iperf3_server(self):
        """
        execute iperf3 commands in shell
        by default , the device is DUT
        """
        if self._server is not None:
            self.stop_iperf3_server()

        server = None
        for port in range(5201, 5207):
            try:
                cmd = f"iperf3 -s -p {port}"
                # server = subprocess.Popen(f"adb -s {self.device.id} shell iperf3 -s -p {port}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                server = subprocess.Popen(f"iperf3 -s -p {port}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                logger.info(f"Successfully execute iperf3 on port {port} on host")
                self._port = port
                break
            except Exception as e:
                logger.exception(f"Exception occurred while starting iperf3 server on port {port} | ERROR: {e}")
                server = None
        self._server = server

    def run_iperf3_client(self, cmd):
        try:
            i = 0
            while i < 3:
                # result = subprocess.run(cmd % (self._ip, self._port), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                # resp = result.stdout.decode('utf-8').strip()
                resp = self.device.run_command(cmd % (self._ip, self._port))
                # logger.debug(f"iperf3 client output\n{resp}")
                if "Connection refused" in resp:
                    i += 1
                else:
                    break
        except Exception as e:
            logger.exception(f"Exception occurred while starting iperf3 client \"{cmd}\" | ERROR: {e}")

    def read_rssi(self):
        """
        get rssi level in shell
        """
        try:
            logger.info("Getting RSSI")
            resp = self.device.run_command("dumpsys connectivity | sed -n '/RSSI:/p'")
            rssi = int(re.findall(r"RSSI: -?\d+", resp)[0].split(" ")[1])
            return rssi
        except Exception as e:
            logger.exception(f"Exception occurred while executing read_rssi | ERROR: {e}")
            return None

    def read_rssi_values(self):
        """
        get rssi level in shell
        """
        try:
            while True:
                rssi = self.read_rssi()
                if rssi:
                    self.rssi_list.append(rssi)
                    Utils.time_delay_s(1)
                else:
                    break
                if self.rssi_flag:
                    break
        except Exception as e:
            logger.exception(f"Exception occurred while executing read_rssi_values in DUT | ERROR: {e}")

    def stop_rssi_reading(self):
        self.rssi_flag = True

    def stop_iperf3_server(self):
        """
        kill iperf3
        """
        try:
            # self.device.run_command("killall iperf3")
            subprocess.run("killall iperf3", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            resp = self._server.communicate()[0].decode("utf-8").strip()
            logger.debug(f"iperf3 server output\n{resp}")
            if self._server is not None:
                self._server.wait()
            return resp
        except Exception as e:
            logger.exception(f"Exception occurred while killing iperf | ERROR: {e}")
            return None

    def parse_iperf_result(self, resp):
        result = ""
        if resp is None:
            return result
        try:
            resp = resp.split("\n")
            ret = list(filter(re.compile(".+receiver$").match, resp))[0]
            bitrate = re.findall(r"\d+ Mbits/sec|\d+.\d+ Mbits/sec", ret)[0]
            transfer = re.findall(r"\d+ MBytes|\d+.\d+ MBytes|\d+ GBytes|\d+.\d+ GBytes", ret)[0]
            total_time = re.findall(r"\d+.\d{2}\s+sec", ret)[0]
            result = f"Total time: {total_time}\nTransfer: {transfer}\nBitrate: {bitrate}"
            if len(self.rssi_list) > 0:
                result += f"\nRSSIs: {self.rssi_list}"
            return result
        except Exception as e:
            logger.exception(f"Exception occurred while parsing iperf result | ERROR: {e}")
            return result