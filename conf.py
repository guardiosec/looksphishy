#!/usr/bin/env python
import os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

# Log
LOG_FOLDER = os.path.join(WORKING_DIR, 'logs')
LOGGER_FILE = os.path.join(LOG_FOLDER, 'looksphishy.log')
LOGGER_NAME = 'looksphishy'
LOG_FILE_SIZE = 10 * 1000000  # 10 MB
LOG_FILE_NUMBER = 5

TEST_FOLDER = os.path.join(WORKING_DIR, 'test')
STATIC_FOLDER = os.path.join(WORKING_DIR, 'static')
BRAND_FOLDER = os.path.join(STATIC_FOLDER, 'brands')
LOGO_FOLDER = os.path.join(STATIC_FOLDER, 'logo')

LLM_CATEGORY = ['finance', 'sport', 'drug']

LOGO = os.path.join(STATIC_FOLDER, 'logo_looksphishy.png')
HOST = 'localhost:9000'

CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH',
                               '/opt/homebrew/Caskroom/chromedriver/125.0.6422.141/chromedriver-mac-arm64/chromedriver')
# we take the env variable if it exists, otherwise we take the default value ( here the path in MacOS)

URLS_SCANNED = 'urls_scanned'

UI_DESIGN = """
<style>
    /* main background color and text color */
    .stApp {
        background-color: #f9f9f9;
    }
    .stApp * {
        color: #333333;
    }
    .stTextInput > div > div > input {
        background-color: #f0f0f0; /* Light grey background for input box */
        color: #333333; /* Black text color */
    }
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #f0f0f0; /* Light grey background for file uploader */
        color: #333333; /* Black text color */
    }
    button[data-testid="baseButton-secondary"] {
        background-color: #dad8d8; /* Light grey background for file uploader button */
        color: #333333;
        border: #333333;
    }
    /* Change the header background color */
    header[data-testid="stHeader"] {
        background-color: #f0f0f0; /* Set header background to grey */
        color: white; /* Set header text color to white */
    }
    section[data-testid="stSidebar"] {
        background-color: #f0f0f0; /* Set header background to grey */
        color: white; /* Set header text color to white */
    }
    h2 {
        text-align: center;
    }
    label[data-testid="stWidgetLabel"] {
        color: red;
    }
    .centered-link {
        text-align: center;
        margin-top: 20px;
    }
    .centered-link a {
        text-decoration: none;
    }
    .step-title {
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        color: #333333;
    }
    div[role="radiogroup"] {
        flex-direction:row;
    }
    input[type="radio"] + div {
        background: #d9d9d9;
        color: #333333;
        border-radius: 20px;
        padding: 8px 18px;
    }
    input[type="radio"][tabindex="0"] + div {
        background: #dec5fd;
    }
    input[type="radio"][tabindex="0"] + div p {
        color: #333333;
    }
    div[role="radiogroup"] label > div:first-child {
        display: none;
    }
    div[role="radiogroup"] label {
        margin-right: 0px;
    }
    div[role="radiogroup"] {
        gap: 12px;
    }
    </style>
"""