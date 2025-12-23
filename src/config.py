import os
from pathlib import Path

from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

APP_KEY = os.getenv("APP_KEY")
USER_ID = os.getenv("USER_ID")
USER_PASSWORD = os.getenv("USER_PASSWORD")

PROCESS_FLG = "1"

BASE_URL = os.getenv("BASE_URL")

LOGIN_URL = f"{BASE_URL}login/login/userlogin"
KEYLOGIN_URL = f"{BASE_URL}login/login/keylogin"
EXPORT_URL = f"{BASE_URL}common/export/export"


if __name__ == "__main__":
    print(f"Debug: Loaded Environment File: {ENV_PATH}")
    print(f"Debug: BASE_URL is: {BASE_URL}")
