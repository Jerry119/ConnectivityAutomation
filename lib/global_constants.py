import os


class GlobalConstants:
    # Directory Names
    PROJECT_NAME = "Connectivity"
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TESTS_DIR = os.path.join(ROOT_DIR, "tests")
    LIB_DIR = os.path.join(ROOT_DIR, "lib")
    RESOURCE_DIR = os.path.join(ROOT_DIR, "resources")
    RESULTS_DIR = os.path.join(TESTS_DIR, "results")
    ARCHIVES_DIR = os.path.join(TESTS_DIR, "results_archive")
    LOG_DIR = os.path.join(RESULTS_DIR, "logs")
    OUTPUT_DIR = os.path.join(RESULTS_DIR, "reports")
    UI_DIR = os.path.join(LIB_DIR, "ui")
    ANDROID_MUSIC_DIR = "/sdcard/music/"

    # File Names
    TEST_SUMMARY_FILE = "test_summary.csv"
    UI_ELEMENTS_H4 = os.path.join(UI_DIR, "h4_ui_elements.json")

    # Settings Config
    APP_PACKAGE_SETTINGS = "com.android.settings"
    APP_ACTIVITY_SETTINGS = "com.android.settings.Settings"

    # Phone app config
    DIALER_PACKAGE_SETTINGS = "com.android.dialer"
    DIALER_ACTIVITY_SETTINGS = "com.android.dialer.main.impl.MainActivity"

    # Music app config
    MUSIC_PACKAGE_SETTINGS = "com.android.music"
    MUSIC_ACTIVITY_SETTINGS = "com.android.music.MusicBrowserActivity"

    VOICE_MSG = "This is a test message for voice calling"

    # # Spotify Config
    # APP_PACKAGE_SPOTIFY = "com.spotify.music"
    # APP_ACTIVITY_SPOTIFY = "com.spotify.music.MainActivity"
    # SPOTIFY_PLAYLIST_3 = "RM"

    # # Network Tools Config
    # APP_PACKAGE_NETWORK_TOOLS = "net.he.networktools"
    # APP_ACTIVITY_NETWORK_TOOLS = "net.he.networktools.MainActivity"

    # # A2DP Config
    # A2DP_VALIDATION_ARWIRELESS_PREFIX = "A2DP: Got Audio State change:"
    # A2DP_VALIDATION_LOG = "NOT_PLAYING -> PLAYING"
    # A2DP_VALIDATION_LOG2 = "PLAYING -> NOT_PLAYING"

    # # HFP Config
    # HFP_VOICE_CALL_VALIDATION_PREFIX = "Success: Succesfully executed"
    # HFP_VOICE_CALL_INCOMING_STATUS = "INCOMING"
    # HFP_VOICE_CALL_DIALING_STATUS = "DIALING"
    # HFP_VOICE_CALL_TERMINATED_STATUS = "TERMINATED"

    # Time Formats
    TIME_FORMAT = "%m-%d-%Y %H:%M:%S"
 
    ADB_SHELL_DEFAULT_RUN_WAIT = 5
