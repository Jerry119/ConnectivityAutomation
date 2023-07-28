import subprocess
from cmd_execute import run_cmd, output_cmd
import time

# from acts.controllers import android_device

DEFAULT_UI = "adb shell set_home default"
# IRONMAN_UI = 'adb shell am start -n "hu.ma.ne.ironman/humaneinternal.system.MainActivity" -a android.intent.action.MAIN -c android.intent.category.LAUNCHER'
# KEYEVENT_H = "adb shell input keyevent KEYCODE_H"
IRONMAN_UI = "adb shell set_home ironman"
SETENFORCE = "adb shell setenforce 0"
GETENFORCE = "adb shell getenforce"
ROOT = "adb root"


def go_to_ironman():
    try:
        go_to_default()
        run_cmd(IRONMAN_UI)
        # run_cmd(KEYEVENT_H, to=20)
        time.sleep(5)
    except Exception as e:
        print(f"Failed to switch to ironman UI - {e}")

def go_to_default():
    try:
        if int(output_cmd("adb shell id -u")) != 0:
            print("Rooting the device")
            run_cmd(ROOT)
        if output_cmd(GETENFORCE) == "Enforcing":
            print("Setting to Permissive")
            run_cmd(SETENFORCE)
        run_cmd(DEFAULT_UI)
        time.sleep(5)
    except Exception as e:
        print(f"Failed to switch to humane UI - {e}")


go_to_ironman()
