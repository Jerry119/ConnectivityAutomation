from lib.battery import Battery
from lib.config import Config
from lib.logger.logger import Logger

logger = Logger(logger_name=__name__).logger


class BatteryAPI:
    def __init__(self, dut):
        self.dut = dut
        self.battery = Battery(self.dut)

    def get_battery_level(self):
        level = self.battery.get_level()
        return level

    def drain_battery_to_level(self, target_level):
        self.battery.wait_to_drain(target_level)

    def charge_battery_to_level(self, target_level):
        self.battery.wait_to_charge(target_level)

    def set_battery_level(self, target_level):
        target_level = int(target_level)
        current_level = int(self.get_battery_level())
        if current_level > target_level:
            self.drain_battery_to_level(target_level)
        elif current_level < target_level:
            self.charge_battery_to_level(target_level)
        current_level = self.get_battery_level()
        logger.info("Current battery level set to: %s" % current_level)

    def disable_charging(self):
        self.battery.disable_charging()

    def enable_charging(self):
        self.battery.enable_charging()

    def check_battery_level(self, battery_level, check_flag=False):
        """
        Method to check & set battery level
        """
        self.set_battery_level(battery_level)

    def enable_battery_charging(self, check_flag=False):
        """
        Method to enable charging
        """
        self.enable_charging()
