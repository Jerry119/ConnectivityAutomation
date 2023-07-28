import subprocess

# from acts.controllers import android_device


def run_cmd(cmd, shell=True, to=10):
    subprocess.run(cmd, shell=shell, timeout=to)

def output_cmd(cmd, shell=True, to=10):
    return subprocess.check_output(cmd, shell=shell, timeout=to, stderr=subprocess.DEVNULL).decode("utf-8").strip()

# def execute_shell_cmd(ad, cmd):
#     return ad.adb.shell(cmd)