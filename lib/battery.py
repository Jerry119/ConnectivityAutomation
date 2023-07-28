from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


class Battery:
    def __init__(self, dut):
        self.dut = dut

    def get_level(self):
        """
        Get battery level of the connected dut.
        """
        return int(self.dut.run_command("dumpsys battery | grep level | awk -F ' ' '{print $2}'"))

    # def check_level(self):
    #     """
    #     Check battery level using the dumpsys method. Returns the battery level of DUT
    #     """
    #     result = self.dut.run_command("dumpsys battery")
    #     level_line = [line for line in result.splitlines() if "level" in line][0]
    #     level = int(level_line.split(": ")[-1])
    #     return level

    def wait_to_charge(self, target_level):
        """
        Wait for battery to reach the target level. The method exits when the target
        battery level is achieved.
        """
        self.enable_charging()
        while True:
            current_level = self.get_level()
            if current_level >= target_level:
                break
            else:
                logger.info("Battery level is %s, waiting..." % current_level)
                Utils.time_delay_s(60)

    def wait_to_drain(self, target_level):
        """
        Wait for battery to drain until the target level is reached.
        """
        self.disable_charging()
        while True:
            current_level = self.get_level()
            if current_level <= target_level:
                logger.info("Battery level is %s, waiting... !" % current_level)
                break
            Utils.time_delay_s(60)

    def enable_charging(self):
        """
        Enable charging when the DUT is connected to the charging pin.
        """
        pass

    def disable_charging(self):
        """
        Disable charging when the DUT is connected to the charging pin.
        """
        pass

    # def get_board_name(self):
    #     """
    #     Identify whether the device is of kind P1 or EVT.
    #     """
    #     pass
