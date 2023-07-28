import argparse
import pytest
from lib.config import Config
from lib.utils import Utils


def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect logcat from the device"
    )

    parser.add_argument(
        "-m",
        "--mark",
        default="all",
        const='all',
        nargs='?',
        choices=[
            "module", 
            "aosp", 
            "ironman", 
            "sanity", 
            "performance", 
            "bluetooth", 
            "wifi", 
            "coex", 
            "call", 
            "dev", 
            "ota", 
            "all"
        ],
        help="Run tests on a specific stack component"
    )

    parser.add_argument(
        "-e",
        "--exclude",
        default="None",
        const="None",
        nargs="?",
        choices=["bluetooth", "wifi", "None"],
        help="Exclude test cases from a mark to be run"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    test_cases = []
    ALL_TESTS = ["-v"] + Config.WIFI_SANITY_TEST + Config.WIFI_PERFORMANCE_TEST + \
        Config.BT_SANITY_TEST + Config.BT_PERFORMANCE_TEST + Config.COEX_TEST + Config.CALL_TEST + Config.OTA_TEST
    if args.mark == "all":
        test_cases = ALL_TESTS
    else:
        if args.exclude != "None":
            mark = args.mark + f" and not {args.exclude}"
        test_cases = ["-m", args.mark] + ALL_TESTS
    pytest.main(test_cases)