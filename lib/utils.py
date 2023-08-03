import csv
import glob
import gspread
import json
import os
import shutil
import signal
import time
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from sys import platform

from lib.config import Config
from lib.global_constants import GlobalConstants as Global
from lib.logger.logger import Logger

logger_obj = Logger(logger_name=__name__)
logger = logger_obj.logger
cur_log_file = logger_obj.log_file


class Utils:
    @staticmethod
    def time_delay_s(sec):
        """
        Apply a time delay (in seconds)
        """
        time.sleep(sec)

    @staticmethod
    def get_current_time():
        """
        Get the current time in HH:mm:ss format
        """
        return datetime.now()

    @staticmethod
    def get_current_date():
        """
        Returns current datetime in the following format: YYYY_mm_dd
        :return:
        """
        return datetime.now().strftime("%Y_%m_%d")

    @staticmethod
    def get_current_time_with_format(dt_format):
        """
        Get the current time in specified format
        """
        return datetime.now().strftime(dt_format)

    @staticmethod
    def get_time_diff_s(t1, t2, precision=3):
        """
        Get time difference in seconds with 3 decimal precision
        """
        time_delta_s = round((t2 - t1).total_seconds(), precision)
        return time_delta_s

    @staticmethod
    def convert_time_str_to_datetime(time_str, time_format="%H:%M:%S.%f"):
        """
        Convert time string to datetime object
        """
        return datetime.strptime(time_str.strip(), time_format)

    @staticmethod
    def get_time_diff_from_time_str(t1, t2, time_format="%H:%M:%S.%f", precision=3):
        """
        Get time difference in milliseconds
        """
        t1 = Utils.convert_time_str_to_datetime(t1, time_format)
        t2 = Utils.convert_time_str_to_datetime(t2, time_format)
        return Utils.get_time_diff_s(t1, t2, precision)

    @staticmethod
    def mk_dir(dir_name):
        """
        Make directory if it does not exist
        """
        try:
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)
        except Exception as e:
            logger.exception(
                "Exception occurred while creating directory: %s | "
                "ERROR: %s" % (dir_name, e)
            )

    @staticmethod
    def cp_dir(src_dir, dest_dir):
        """
        Copy files from source directory to destination directory
        """
        try:
            shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True)
        except Exception as e:
            logger.exception(
                "Exception occurred while copying files from %s to %s | "
                "ERROR: %s" % (src_dir, dest_dir, e)
            )

    @staticmethod
    def rm_dir(dir_name):
        """
        Delete directory if it exists
        """
        try:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        except Exception as e:
            logger.exception(
                "Exception occurred while deleting directory: %s | "
                "ERROR: %s" % (dir_name, e)
            )

    @staticmethod
    def rm_dir_files(dir_name):
        """
        Delete all files inside a given directory
        """
        try:
            if os.path.exists(dir_name):
                files = glob.glob("%s/*" % dir_name)
                for f in files:
                    os.remove(f)
        except Exception as e:
            logger.exception(
                "Exception occurred while deleting files from the "
                "directory: %s | ERROR: %s" % (dir_name, e)
            )

    @staticmethod
    def remove_file(file_path):
        """
        Delete file from file path
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.exception(
                "Exception occurred while deleting the file: %s | "
                "ERROR: %s" % (file_path, e)
            )

    @staticmethod
    def get_pass_fail_str(resp):
        """
        Return the string 'PASS' for True and 'FAIL' for False
        """
        return "PASS" if resp is True else "FAIL"

    @staticmethod
    def get_key_list_from_dict(d):
        """
        Get all keys as list from a given dict
        """
        resp = []
        for _k, _v in d.items():
            resp.append(_k)
        return resp

    @staticmethod
    def write_csv(test, dut):
        """
        Write data to csv file
        """
        data = [
            {
                "Test ID": test.id,
                "Test Description": test.objective,
                "Test Status": Utils.get_pass_fail_str(test.status),
                "Test Start Time": test.start_time,
                "Test End Time": test.end_time,
                "Expected Result": test.expected_result,
                "Expected Response": test.expected_resp,
                "Actual Response": test.actual_resp,
                "H4 Serial": str(dut.id),
                "H4 Build Version": str(dut.build_version)
            }
        ]
        Utils.mk_dir(Global.OUTPUT_DIR)
        out_file = os.path.join(Global.OUTPUT_DIR, Global.TEST_SUMMARY_FILE)
        write_header = False
        if not os.path.exists(out_file):
            write_header = True
        try:
            with open(out_file, "a") as f:
                writer = csv.DictWriter(
                    f, fieldnames=Utils.get_key_list_from_dict(data[0])
                )
                if write_header:
                    writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            logger.exception(
                "Exception occurred while writing to csv file | ERROR: %s" % e
            )
    
    @staticmethod
    def move_column_to_front(df, col_name):
        col = df.pop(col_name)
        df.insert(1, col_name, col)
        return df
    
    @staticmethod
    def upload_data_to_google_sheet(data, dut):
        try:
            logger.info("Uploading data to google drive")
            creds = ServiceAccountCredentials.from_json_keyfile_dict(Config.CRED_KEYS, Config.SCOPES)
            client = gspread.authorize(creds)
            sheet = client.open(Config.SHEET_NAME).worksheet(Config.TAB_NAME)
            df = pd.DataFrame(sheet.get_all_records())
            num_col = df.shape[1]
            idx = 1
            prefix = f"{dut.id}\n{dut.build_version}\n" + Utils.get_current_time_with_format("%m/%d")
            new_col = prefix + f"\nRUN_{idx}"
            while new_col in df:
                idx += 1
                new_col = prefix + f"\nRUN_{idx}"

            df[new_col] = df["Test ID"].map(data)
            if num_col > 1:
                df = Utils.move_column_to_front(df, new_col)
            df[new_col] = df[new_col].fillna("Not Started")
            sheet.format(f"A1:{chr(65+num_col)}1", {
                "backgroundColor": {
                    "red": 0.0,
                    "green": 0.0,
                    "blue": 0.0
                },
                "horizontalAlignment": "CENTER",
                "textFormat": {
                    "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0
                    },
                    "fontSize": 10
                }
            })
            sheet.update([df.columns.values.tolist()] + df.values.tolist())
        except Exception as e:
            logger.exception(f"Exception occurred while uploading data to GDrive. | ERROR: {e}")

    @staticmethod
    def create_date_run_folder_in_directory(target_dir, dut):
        """
        Creates a folder with test execution date and inside that creates a run folder
        for a specific test run as 'Run <RUN_COUNT>'in the specified directory.
        Eg: <PROJECT_ROOT>/tests/results/2022_05_20/Run 1/
        Returns the newly created Run folder's full path.
        """
        try:
            # Create a folder with today's date
            if not os.path.exists(target_dir):
                Utils.mk_dir(target_dir)
            subdir = os.path.join(target_dir, dut.id + "_" + Utils.get_current_date())
            if not os.path.exists(subdir):
                Utils.mk_dir(subdir)
            # Create 'Run <RUN_COUNT>' folder inside the date folder
            file_count = len([f for f in os.listdir(subdir) if not f.startswith('.')]) + 1
            run_dir_name = "Run_%s" % file_count
            run_dir_path = os.path.join(subdir, run_dir_name)
            Utils.mk_dir(run_dir_path)
            return run_dir_path
        except Exception as e:
            logger.exception(
                "Exception occurred while creating /<DATE>/RUN <COUNT>/ "
                "folder in directory: %s. ERROR: %s" % (target_dir, e)
            )

    @staticmethod
    def rm_log_files_except_current_log():
        """
        Delete all log files from logs directory except the current log file
        """
        try:
            if os.path.exists(Global.LOG_DIR):
                files = glob.glob("%s/*" % Global.LOG_DIR)
                for f in files:
                    if f != cur_log_file:
                        os.remove(f)
        except Exception as e:
            logger.exception(
                "Exception occurred while deleting log files | ERROR: %s" % e
            )

    @staticmethod
    def init_results_dir_setup():
        """
        Clear contents from results folder and create new folder structure for results
        """
        Utils.rm_log_files_except_current_log()
        Utils.rm_dir_files(Global.OUTPUT_DIR)

    @staticmethod
    def archive_test_results(dut):
        """
        Copy current run results to archive directory
        """
        try:
            logger.info("Saving test data to archive folder")
            arch_results_dir = Utils.create_date_run_folder_in_directory(
                Global.ARCHIVES_DIR, dut
            )
            Utils.cp_dir(Global.RESULTS_DIR, arch_results_dir)
        except Exception as e:
            logger.exception(
                "Exception occurred while archiving test "
                "results | ERROR: %s" % e
            )

    @staticmethod
    def read_json_data(file_name):
        """
        Returns contents of a json file
        :return: List
        """
        with open(file_name) as f:
            json_data = json.load(f)
        return json_data

    @staticmethod
    def get_timestamp_from_log_line(log_line):
        """
        Get time value from the given log line
        """
        if not log_line:
            logger.error("Log line not found | Exiting !")
            return None
        log_time = log_line.split("  ")[0].split(" ")[1]
        return log_time

    @staticmethod
    def get_time_diff_from_log_lines(start_log_line, end_log_line):
        """
        Get time difference from the given start and end log lines
        """
        if not start_log_line and not end_log_line:
            logger.error("Log lines not found | Exiting !")
            return None

        end_log_time = Utils.get_timestamp_from_log_line(end_log_line[-1])
        for line in start_log_line[::-1]:
            start_log_time = Utils.get_timestamp_from_log_line(line)
            if start_log_time < end_log_time:
                logger.debug("Start Log Line: %s" % line)
                break
        logger.debug("End Log Line: %s" % end_log_line[-1])

        logger.debug("Start Log Time: %s" % start_log_time)
        logger.debug("End Log Time: %s" % end_log_time)

        if start_log_time and end_log_time:
            time_delta = Utils.get_time_diff_from_time_str(start_log_time, end_log_time)
            logger.debug("Log Time Delta: %s" % time_delta)
            return time_delta
        else:
            logger.error("Unable to find start or end log times")
            return None

    @staticmethod
    def kpi_validation(expected_range, actual_value):
        """
        Check whether the actual KPI value is inside the expected KPI range or not.
        """
        logger.info("Expected response is: %s" % expected_range)
        logger.info("Actual response is: %s" % actual_value)

        status = False
        if isinstance(actual_value, str):
            if expected_range == actual_value.strip():
                status = True
        elif actual_value is not None:
            lower_bound, upper_bound = expected_range.split("-")
            if (
                float(lower_bound)
                <= float(round(actual_value, 3))
                <= float(upper_bound)
            ):
                status = True

        if status:
            logger.info("KPI validation passed !")
        else:
            logger.error("KPI validation failed !")
        return status
    
    @staticmethod
    def collect_data(test, dut):
        dut.collect_adb_logcat(test.id)

    @staticmethod
    def kill_process(pid):
        try:
            if pid:
                os.kill(int(pid), signal.SIGKILL)
            else:
                logger.error("No process id was found to kill")
        except Exception as e:
            logger.exception(
                "Exception occurred while killing the process | " "ERROR: %s" % e
            )

    @staticmethod
    def get_host_platform():
        if platform == "darwin":
            return "mac"
        elif platform == "linux":
            return "linux"
        elif platform == "win32":
            return "windows"
        else:
            return "unsupported platform"

    @staticmethod
    def is_mac_host():
        if Utils.get_host_platform() == "mac":
            return True
        return False

    @staticmethod
    def is_linux_host():
        if Utils.get_host_platform() == "linux":
            return True
        return False

    @staticmethod
    def is_windows_host():
        if Utils.get_host_platform() == "windows":
            return True
        return False
