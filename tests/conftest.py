import pytest
from collections import defaultdict

from lib.adb import ADBInterface
from lib.btcontrol import BTControl
from lib.config import Config
from lib.data_interface import Data
from lib.h4 import H4
from lib.server_api import AppiumServerAPI
from lib.utils import Utils
from lib.wificontrol import WiFiControl


@pytest.fixture(scope="session")
def interface():
    return ADBInterface()


@pytest.fixture(scope="session")
def dut(interface):
    dut = H4(interface)
    yield dut

@pytest.fixture(scope="session")
def summary(request):
    summary = defaultdict(lambda: "Not Started")
    yield summary

@pytest.fixture(scope="session", autouse=True)
def upload_data(request, summary, dut):
    if Config.UPLOAD_TO_DRIVE:
        request.addfinalizer(lambda: Utils.upload_data_to_google_sheet(summary, dut))

@pytest.fixture(scope="session", autouse=True)
def archive_data(request, dut):
    Utils.init_results_dir_setup()
    request.addfinalizer(lambda: Utils.archive_test_results(dut))

@pytest.fixture(scope="class")
def wifi(request, dut):
    request.cls.wifi = WiFiControl(dut)
    yield

@pytest.fixture(scope="class")
def bluetooth(request, dut):
    request.cls.bluetooth = BTControl(dut)
    yield

@pytest.fixture(scope="function")
def test():
    _test_obj = Data()
    yield _test_obj

@pytest.fixture(scope="function")
def appium_server():
    _server = AppiumServerAPI()
    _server.start_appium_server(None)
    yield _server
    _server.stop_appium_server()