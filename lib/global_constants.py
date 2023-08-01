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
    PHONE_PACKAGE_SETTINGS = "com.android.dialer"
    PHONE_ACTIVITY_SETTINGS = "com.android.dialer.main.impl.MainActivity"

    # Dialer app config
    DIALER_PACKAGE_SETTINGS = "humane.experience.dialer"
    DIALER_ACTIVITY_SETTINGS = "humaneinternal.system.ipc.HumaneExperienceActivity"

    # Music app config
    MUSIC_PACKAGE_SETTINGS = "com.android.music"
    MUSIC_ACTIVITY_SETTINGS = "com.android.music.MusicBrowserActivity"

    VOICE_MSG = "This is a test message for voice calling"

    # Time Formats
    TIME_FORMAT = "%m-%d-%Y %H:%M:%S"
 
    ADB_SHELL_DEFAULT_RUN_WAIT = 5
