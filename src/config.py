import os
from pathlib import Path

from dotenv import load_dotenv

CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Credentials:
    APP_KEY = os.getenv("APP_KEY")
    USER_ID = os.getenv("USER_ID")
    PASSWORD = os.getenv("USER_PASSWORD")


class LzExportConfig:
    class Product:
        FILE_ID = "6"
        PTRN_ID = "0"

    class Stock:
        FILE_ID = "4"
        PTRN_ID = "1"

    class D2C:
        FILE_ID = "3"
        PTRN_ID = "1"

    class B2B:
        FILE_ID = "2"
        PTRN_ID = "1"

    DEFAULT_PROCESS_FLAG = "1"
    DEFAULT_OWNER_ID = "1"
    DEFAULT_AREA_ID = "1"


class Endpoints:
    BASE_URL = os.getenv("BASE_URL")
    LOGIN = f"{BASE_URL}login/login/userlogin"
    KEY_LOGIN = f"{BASE_URL}login/login/keylogin"
    EXPORT = f"{BASE_URL}common/export/export"


if __name__ == "__main__":
    print(f"Debug: Loaded Environment File: {ENV_PATH}")
    print(f"Debug: BASE_URL is: {Endpoints.BASE_URL}")
