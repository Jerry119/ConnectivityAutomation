
# Wireless Automation

This script is intended to validate wireless components on H4

## Prerequisites

- Install node.js

- Install appium
> npm install -g appium

- Install all the required packages
> pip3 install -r requirements.txt

## How to run the test

This will run all the test cases 
> python3 main.py

To select one specific category of test
> python3 main.py -m <test_category>

## Test Categories: 
"module", 
"aosp", 
"ironman", 
"sanity", 
"performance", 
"bluetooth", 
"wifi", 
"coex", 
"call,
"dev", 
"ota",
"all"

## If you want to upload test result to the drive

1.  set UPLOAD_TO_DRIVE to True in config.py,
2.  update CRED_KEY in config.py, you can get the credential info by following https://docs.gspread.org/en/latest/oauth2.html
