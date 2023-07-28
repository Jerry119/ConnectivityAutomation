from typing import Optional

from lib.server import (
    AppiumException,
    AppiumServer,
)
from lib.logger.logger import Logger

logger = Logger(logger_name=__name__).logger


class AppiumServerAPI:
    def __init__(self):
        self.appium_server = None

    def start_appium_server(self, appium_server_port: Optional[int]) -> AppiumServer:
        if appium_server_port is not None:
            # Reuse running appium server at given port
            logger.debug(f"Using appium server at port {appium_server_port}")
            return AppiumServer(appium_server_port)
        else:
            # Find an open port to start appium server
            # for appium_port in range(4723, 4733):
            attempt = 0
            appium_port = 4723
            while attempt < 3:
                self.appium_server = AppiumServer(appium_port)
                try:
                    self.appium_server.start_new_server()
                    logger.debug(f"Started new appium server at port {appium_port}")
                    return self.appium_server
                except AppiumException:
                    # Unable to start server, likely because port is taken
                    logger.warning(
                        f"Tried to start new appium server at port {appium_port} but it was taken, trying it again"
                    )
                    self.stop_appium_server()
                    attempt += 1
            # All ports to try are exhausted
            raise Exception(
                "Could not start appium server, "
                # "try using the --appium-server argument to manually specify an existing appium server"
            )

    def stop_appium_server(self) -> None:
        try:
            self.appium_server.stop_server()
        except Exception as e:
            logger.exception(f"Exception occurred | ERROR: {e}")
