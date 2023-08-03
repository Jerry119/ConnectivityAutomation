import os
import subprocess
import tempfile
import time
from types import TracebackType
from typing import Optional, TextIO, Type

from lib.logger.logger import Logger

logger = Logger(logger_name=__name__).logger


class AppiumException(Exception):
    pass

class AppiumServer:
    def __init__(self, port: int) -> None:
        self._port: int = port
        self._log_file: Optional[TextIO] = None
        # pyre-fixme[24]: Generic type `subprocess.Popen` expects 1 type parameter.
        self._server: Optional[subprocess.Popen] = None
    
    def start_new_server(self) -> None:
        server = self._server
        if server is not None:
            # Terminate previous server process
            server.terminate()

        log_file = self._log_file
        if log_file is not None:
            log_file.close()
        logger.debug(f"Starting new appium server at port {self._port}")
        with open(os.path.join(tempfile.gettempdir(), "appium_log"), "w") as log_file:
            self._log_file = log_file
            server = subprocess.Popen(
                ["appium", "-a", "127.0.0.1", "-p", str(self._port)], stdout=self._log_file, shell=True
            )
            time.sleep(2)

        server_returncode = server.poll()
        # logger.debug(server_returncode)
        if server_returncode is not None and server_returncode != 0:
            # Server process terminated with error
            raise AppiumException(
                f"Appium server terminated with returncode {server_returncode}"
            )
        self._server = server

    def stop_server(self) -> None:
        if self._server is None:
            # No running server to stop
            return

        log_file = self._log_file
        if log_file is not None:
            log_file.close()
            self._log_file = None

        logger.debug(f"Stopping appium server at port {self._port}")
        server = self._server
        if server is not None:
            server.terminate()
        self._server = None

    def restart_server(self) -> None:
        self.stop_server()
        self.start_new_server()

    def __enter__(self):
        self.start_new_server()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        self.stop_server()
        return False
