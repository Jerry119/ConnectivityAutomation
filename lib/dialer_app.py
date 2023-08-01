from lib.appium_utils import AppiumUtils
from lib.config import Config
from lib.logger.logger import Logger

logger = Logger(logger_name=__name__).logger


class DialerApp(AppiumUtils):
    # coordinate combinations for digits 0 - 9
    col_idx = [230, 402, 575]
    row_idx = [160, 290, 417, 545]
    call_icon = (402, 677)
    end_call_icon = (406, 570)

    # row_idx[n%3-1], col_idx[(n-1)/3]
    # one = (230, 160)
    # two = (402, 160)
    # three = (575, 160)
    # four = (230, 290)
    # five = (402, 290)
    # six = (575, 290)
    # 7 = (230, 417)
    # 8 = (402, 417)
    # 9 = (575, 417)

    def __init__(self, dut):
        super().__init__(dut, Config.DIALER_APP_CONFIG)

    def launch_app(self):
        resp = self.launch_application()
        if resp:
            logger.info("Dialer app launched")
        else:
            logger.error("Exception occurred while launching Dialer app")
    
    def _get_digit_coord(self, n):
        if n == 0:
            return self.col_idx[1], self.row_idx[-1]
        return self.col_idx[n%3-1], self.row_idx[(n-1)//3]
    
    def call_number_from_dut(self, number):
        try:
            number = number.replace("+1", "")
            for n in number:
                x, y = self._get_digit_coord(int(n))
                logger.debug(f"Coordinate for digit \"{n}\" is ({x}, {y})")
                self.dut.click(x, y)
            self.dut.click(self.call_icon[0], self.call_icon[1])
        except Exception as e:
            logger.exception(f"Exception occurred while calling {number} from DUT | ERROR: {e}")

    def end_ongoing_call(self):
        self.dut.click(self.end_call_icon[0], self.end_call_icon[1])