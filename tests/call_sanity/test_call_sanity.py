import pytest
import threading

from lib.config import Config
from lib.call_server import CallServer
from lib.global_constants import GlobalConstants as Global
from lib.ironman import Ironman
from lib.logger.logger import Logger
from lib.phone_app import PhoneApp
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger


@pytest.mark.call
class TestCallSanity:
    @pytest.mark.aosp
    def test_accept_call_on_dut(self, request, test, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Accept an incoming call on H4"
        test.expected_result = "DUT is able to accept calls"
        start_log_text = "I Telecom : CallsManager: setCallState RINGING -> ANSWERED"
        end_log_text = "I Telecom : CallsManager: setCallState DISCONNECTING -> DISCONNECTED"
        try:
            dut.clear_device_logs()
            dut.grant_audio_call_permission()
            callserver = CallServer()
            ironman = Ironman(dut)
            callserver.make_call_to_dut()
            ironman.accept_incoming_call()
            Utils.time_delay_s(5)
            ironman.end_ongoing_call()
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            duration = dut.get_latency_between_two_logs(start_log_text, end_log_text)
            test.status = duration is not None and duration > 0
            test.actual_resp = f"Call duration: {duration}s"
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status

    @pytest.mark.aosp
    def test_make_a_call_from_dut(self, request, test, appium_server, dut, summary):
        test.start_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
        test.id = request.node.originalname.replace("test_", "").upper()
        test.objective = "Initiate a voice call from H4"
        test.expected_result = "DUT is able to make a voice call"
        try:
            dut.clear_device_logs()
            phone = PhoneApp(dut, Config.PHONE_APP_CONFIG)
            # callserver = CallServer()
            # callserver.start_ngrok()
            # ngrok_thread = threading.Thread(target=callserver.start_ngrok)
            # ngrok_thread.start()
            phone.launch_app()
            dut.grant_audio_call_permission()
            phone.go_to_dial_screen()
            phone.make_a_call_to(Config.TWILIO_NUM)
            # callserver.stop_ngrok()
            test.status = True
        except Exception as e:
            logger.exception(f"Exception occurred in {test.id} | ERROR: {e}")
        finally:
            Utils.collect_data(test, dut)
            test.end_time = Utils.get_current_time_with_format(Global.TIME_FORMAT)
            Utils.write_csv(test, dut)
            summary[test.id] = Utils.get_pass_fail_str(test.status)
            assert test.status