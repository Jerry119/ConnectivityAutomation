from lib.global_constants import GlobalConstants as Global


class Config:
    # Test Config
    TEST_ITERATION_COUNT = 1

    # Logger Config
    LOGGING = True  # True or False
    LOG_FILE_PREFIX = "Connectivity_Validation"
    LOG_LEVEL = "DEBUG"  # DEBUG, INFO, ERROR

    # Database Config
    UPLOAD_TO_DRIVE = False  # True or False
    SHEET_NAME = "WiFi/BT Integration & Validation"
    TAB_NAME = "summary"

    SSID = "hdevice"
    PASSWORD = "Figure-Crepe9-Confound"

    TEST_BT_DEVICE = "Jerry’s AirPods"

    TWILIO_ACCOUNT_SID = "ACe2391540b23d67f909bf13ddfbc72bc8"
    TWILIO_AUTH_TOKEN = "147f2f16257feb69e4b4374f5ffa49c7"
    TWILIO_NUM = "+18882946399"
    DUT_NUM = "+14155950760"
    # DUT_NUM = "+14155796161"

    SETTING_APP_CONFIG = {
        "app_package": Global.APP_PACKAGE_SETTINGS,
        "app_activity": Global.APP_ACTIVITY_SETTINGS,
        "no_reset": "true"
    }

    PHONE_APP_CONFIG = {
        "app_package": Global.PHONE_PACKAGE_SETTINGS,
        "app_activity": Global.PHONE_ACTIVITY_SETTINGS,
        "no_reset": "true"
    }

    MUSIC_APP_CONFIG = {
        "app_package": Global.MUSIC_PACKAGE_SETTINGS,
        "app_activity": Global.MUSIC_ACTIVITY_SETTINGS,
        "no_reset": "true"
    }

    DIALER_APP_CONFIG = {
        "app_package": Global.DIALER_PACKAGE_SETTINGS,
        "app_activity": Global.DIALER_ACTIVITY_SETTINGS,
        "no_reset": "true"
    }

    SCOPES = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    ### For google drive api, specific to each account ###
    CRED_KEYS = {
        "type": "service_account",
        "project_id": "connectivity-automation",
        "private_key_id": "77981267d5998a68952afc91f833ebabf59f1234",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7xueaRizg3jrN\ncJL3CoZhRp2ixrIM06aoPA7DwqMv/7apBKEjC09KILGhHic/CXj6kQFYV1Vs8Ml8\nEVRnDuk0YXNadVTjJsuWZD97KMn3eQZX+Grxq0iRI+DshjnV5tjDIW/Mmt7bgdFr\naGP++v9I1MJC9dtxyo/da1CwzzxhXsNlhBmT2hmnV0MoIwBZuTcJ0LU/TTqzz8C0\njFyTWNjjKzEfNUwr0YbGlj4ZUAz5dPsE6bpD5hFk1FTnKofl1O2kkRX6OoqkZJIE\nerSu0h/K/VdYGOCxwH0/QXIpNcFeoxHWvYMI8WHmTRX8mtWh1BLNebqzmHV+p2S4\nfO54gjDZAgMBAAECggEAJXnmXdItIUkBC+Dwl+jsFmyBSAwnW2t/arqnyLanGoyK\n0FNJ9KRMdBMv2GPb+dcCY+G+VrsBY99vmvkbcwEVFnzviIl7wmULA04pJEOpAWDQ\nXQzJjUd90WfLe3EziEcNEm6xMTDkkwMnAGyCbpB6FDdQOQx3+k8u5MZHAa6ukpD+\n73TNnlWE6QtKuE2x4M1UETESY15xvLWOM8qtuLzw+IhPM1nngfxtesWiQ56xcVpR\nBYH++qoaEmrUd+gzJw/MJmhP8fXmlhp69HS8/OjjX2m+MM2Y6b28T5FaLyDnuEBf\nwIqO7vG93pasTk0V+ZIUG/EhjVnaL2oJrIpGvOez/QKBgQDyolWAcQGYmm82tpQn\nK2iL9cz7IidnIWuB/yIR0M8heu5WeohyUKzEQzNjSYL+wCJyXEj6KSFtBqsQWGrD\nxpMXWt5YAGVevdiyF3NkkGrhN53xQe0WJMxynozivfdgtKfYXod6XwA/re+ElRIT\n2JS0SGTbu33N3NRSI5Sdq65JFQKBgQDGHvddJj+j34Jy5wM+7WFSaSBp2CitUd2w\nAqyO+IZYjkQXW6xwFvyqsJ2JV5qT2PuWLABYrAMbbOVof1Uo6z1y4GA2t3OaWz6b\ndWO0bvILlEaN/5a+j5U1Rk2G64h2JDaJwG0y3c4QWWIOlsdguq4KtMtABzr+CdE2\nJJVX7P2xtQKBgQCR7nMQemdkWlZTiQKYgHIz49Wyofsi+yXHHSVno7hAwchBuRcB\n8mXG8UgiCl/ASt0s/TZjR4O0KFOQ1Cz6rR9g56VdNnfBwNtpWdNsg7PU23eiWG15\naQ6STawc3/a+ckmVSF2hiywCIOIzUtl5mETwHa6TvjPPMmd9M6s6Hb0IdQKBgAhB\nhBdan65Jgxscq1L0+2g+vz4J5vAKCE3sXpp6msaX7xh2FoJ5QsAuKfJuNx/QG/PP\nE5ieWmbLK+gl3judSes+lGPTUzrscHhz9NqxAN8gp6wFKZf5TcNxkYt8xyv9KFSn\nMyW6fnrJ7r8i414RiW0iyZF6e6fYauJxtdN7Kbs9AoGBAMfAKNUqRo8ybwWwXLoZ\nDrxeuUOfwJqCqYzYxqgDEsmpVZ6a7irG1IR7pq7zVhm/ORKVUkajOn7RXRFfulBZ\nNgj693MK249wvhjWDcUvIH1GnyFQFWzITKS36WV+tCud90P9FLW8yVoKI3aO5ulZ\n4zL5KbV+HWrefBsjPF0RohWo\n-----END PRIVATE KEY-----\n",
        "client_email": "automation-service@connectivity-automation.iam.gserviceaccount.com",
        "client_id": "103678698258136611341",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/automation-service%40connectivity-automation.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    WIFI_SANITY_TEST = [
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_enable_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_disable_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_scan_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_connect_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_disconnect_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_reconnect_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_forget_wifi",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_enable_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_disable_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_scan_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_connect_new_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_disconnect_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_connect_saved_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_forget_wifi_from_settings",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_enable_wifi_from_ironman",
        "tests/wifi_sanity/test_wifi_sanity.py::TestWiFiSanity::test_disable_wifi_from_ironman"
    ]

    WIFI_PERFORMANCE_TEST = [
        "tests/wifi_performance/test_wifi_performance.py::TestWiFiPerformance::test_throughput_with_iperf3",
        "tests/wifi_performance/test_wifi_performance.py::TestWiFiPerformance::test_latency_to_establish_new_connection",
        "tests/wifi_performance/test_wifi_performance.py::TestWiFiPerformance::test_latency_to_auto_reassociate_connection",
        "tests/wifi_performance/test_wifi_performance.py::TestWiFiPerformance::test_latency_to_disconnect_from_network"
    ]

    BT_SANITY_TEST = [
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_enable_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_disable_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_enable_bluetooth_from_settings",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_disable_bluetooth_from_settings",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_scan_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_pair_new_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_audio_route_to_bt",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_disconnect_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_pair_saved_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_auto_reconnect_bluetooth",
        "tests/bt_sanity/test_bt_sanity.py::TestBluetoothSanity::test_forget_bluetooth"
    ]
    
    BT_PERFORMANCE_TEST = [
        "tests/bt_performance/test_bt_performance.py::TestBluetoothPerformance::test_bt_on_off_10_times",
        "tests/bt_performance/test_bt_performance.py::TestBluetoothPerformance::test_latency_to_auto_reassociate_bt"
    ]

    COEX_TEST = [
        "tests/coex/test_coex.py::TestCoEx::test_tcp_throughput_baseline",
        "tests/coex/test_coex.py::TestCoEx::test_tcp_throughput_with_bt_scan_10",
        "tests/coex/test_coex.py::TestCoEx::test_tcp_throughput_with_bt_scan_12",
        "tests/coex/test_coex.py::TestCoEx::test_udp_throughput_with_bt_scan_10",
        "tests/coex/test_coex.py::TestCoEx::test_udp_throughput_with_bt_scan_12"
    ]

    CALL_TEST = [
        "tests/call_sanity/test_call_sanity.py::TestCallSanity::test_accept_call_on_dut",
        "tests/call_sanity/test_call_sanity.py::TestCallSanity::test_make_a_call_from_dut"
    ]

    OTA_TEST = [
        "tests/ota/test_ota.py::TestOTA::test_ota_normal_condition"
    ]