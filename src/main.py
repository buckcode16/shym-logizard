"""

api
config
create asyncClient
let other services to use this asyncClient
asyncClient requires setup of env

revisit docker config
configure alembic.ini to use db url
"""

import asyncio
import os

from src.api import LogizardClient
from src.config import (
    APP_KEY,
    EXPORT_URL,
    KEYLOGIN_URL,
    LOGIN_URL,
    PROCESS_FLG,
    USER_ID,
    USER_PASSWORD,
)

payload_login = {
    "APP_KEY": APP_KEY,
    "USER_ID": USER_ID,
    "PASSWORD": USER_PASSWORD,
    "PROCESS_FLG": PROCESS_FLG,
}


async def main():
    async with LogizardClient() as client:
        res_login = await client.post(LOGIN_URL, json=payload_login)

        data = res_login.json()

        # calls apis
        # export_master
        # export_stock
        # export_d2c
        # export_b2b

        pass


if __name__ == "__main__":
    asyncio.run(main())
