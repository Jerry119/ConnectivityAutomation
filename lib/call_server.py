# from flask import Flask, request
# from pyngrok import ngrok
# import subprocess

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from lib.config import Config
from lib.global_constants import GlobalConstants as Global
from lib.logger.logger import Logger
from lib.utils import Utils

logger = Logger(logger_name=__name__).logger

# app = Flask(__name__)


class CallServer:
    def __init__(self):
        self.account_sid = Config.TWILIO_ACCOUNT_SID
        self.auth_token = Config.TWILIO_AUTH_TOKEN
        self.client = Client(self.account_sid, self.auth_token)
        # self._ngrok_server = None
    
    # @app.route('/voice', methods=['POST'])
    # def voice():
    #     resp = VoiceResponse()
    #     # Read a message aloud to the caller
    #     resp.say("Hello world! This is a test")
    #     return str(resp)

    def make_call_to_dut(self, voice_msg=Global.VOICE_MSG):
        try:
            call = self.client.calls.create(
                twiml=f"<Response><Say>{voice_msg}</Say></Response>",
                to=Config.DUT_NUM,
                from_=Config.TWILIO_NUM
            )
            Utils.time_delay_s(7)
            logger.info(call.sid)
            return True
        except Exception as e:
            logger.exception(f"Exception occurred while making a voice call to dut | ERROR: {e}")
            return False
    
    # def start_ngrok(self):
    #     url = ngrok.connect(5000).public_url
    #     print(' * Tunnel URL:', url)
    #     client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
    #     client.incoming_phone_numbers.list(phone_number=Config.TWILIO_NUM)[0].update(voice_url=url + '/voice')
    #     app.run()
    
    # def stop_ngrok(self):
    #     resp = subprocess.check_output("ps | grep -E 'ngrok*.' | awk -F ' ' '{print $1}'", shell=True).split("\n")
    #     pid = resp[-1]
    #     subprocess.run(f"kill -9 {pid}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)