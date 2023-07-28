import logging
import os
import sys
from datetime import datetime

from lib.config import Config
from lib.global_constants import (
    GlobalConstants as Global,
)


class Logger:
    """
    Description of available log levels:

    DEBUG: Used when logging detailed information for diagnosing problems.
    INFO: Used when general information needs to be logged.
    ERROR: Used when the application is not able to perform some function.
    EXCEPTION: Used when logging exceptions. Logs the message with level ERROR.
        Traceback info will also be added to the log message. This method
        should only be called from an exception handler.
    """

    def __init__(self, logger_name="Main", log_dir=Global.LOG_DIR):
        try:
            # if "%s." % Global.PROJECT_NAME in logger_name:
            #     logger_name = logger_name.split("%s." % Global.PROJECT_NAME)[1]
            logger = logging.getLogger(logger_name)
            log_levels = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "ERROR": logging.ERROR,
            }
            log_level = log_levels[Config.LOG_LEVEL]
            logger.setLevel(log_level)
            log_format = (
                "%(asctime)s - %(name)s - %(funcName)s() - "
                "%(levelname)s - %(message)s"
            )
            formatter = logging.Formatter(log_format)
            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)
            logger.handlers.clear()
            logger.addHandler(sh)
            if not Config.LOGGING:
                # Disable logging if global logging is set to False
                logging.disable()
            else:
                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)
                self._file_name = self.get_log_filename(log_dir)
                fh = logging.FileHandler(self._file_name)
                fh.setFormatter(formatter)
                logger.addHandler(fh)
            self._logger = logger
        except Exception as e:
            print("Exception in logger class. ERROR: %s" % e)

    @property
    def logger(self):
        return self._logger

    @property
    def log_file(self):
        return self._file_name

    @staticmethod
    def get_log_filename(log_dir):
        """
        Generates and returns log filename based on current datetime.
        :return:
        """
        cur_time = datetime.now().strftime("%Y_%m_%d_%H_%M")
        # cur_dir = os.mkdir(os.path.join(log_dir, cur_time))
        return os.path.join(log_dir, "%s_%s.log" % (Config.LOG_FILE_PREFIX, cur_time))
