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

from src.api.client import LogizardClient
from src.config import Credentials, Endpoints, ExportConfig
from src.schemas.auth import LoginResponse
from src.services import order, product, stock

payload_login = {
    "APP_KEY": Credentials.APP_KEY,
    "USER_ID": Credentials.USER_ID,
    "PASSWORD": Credentials.USER_PASSWORD,
    "PROCESS_FLG": ExportConfig.DEFAULT_PROCESS_FLAG,
}

payload_master_product = {
    "OWNER_ID": ExportConfig.DEFAULT_OWNER_ID,
    "AREA_ID": ExportConfig.DEFAULT_AREA_ID,
    "FILE_ID": ExportConfig.Product.FILE_ID,
    "PTRN_ID": ExportConfig.Product.PTRN_ID,
}

payload_stock = {
    "OWNER_ID": ExportConfig.DEFAULT_OWNER_ID,
    "AREA_ID": ExportConfig.DEFAULT_AREA_ID,
    "FILE_ID": ExportConfig.Stock.FILE_ID,
    "PTRN_ID": ExportConfig.Stock.PTRN_ID,
}

payload_d2c = {
    "OWNER_ID": ExportConfig.DEFAULT_OWNER_ID,
    "AREA_ID": ExportConfig.DEFAULT_AREA_ID,
    "FILE_ID": ExportConfig.D2C.FILE_ID,
    "PTRN_ID": ExportConfig.D2C.PTRN_ID,
}

payload_b2b = {
    "OWNER_ID": ExportConfig.DEFAULT_OWNER_ID,
    "AREA_ID": ExportConfig.DEFAULT_AREA_ID,
    "FILE_ID": ExportConfig.B2B.FILE_ID,
    "PTRN_ID": ExportConfig.B2B.PTRN_ID,
}


async def main():
    async with LogizardClient() as client:
        await client.post_json(
            Endpoints.LOGIN_URL, payload=payload_login, response_model=LoginResponse
        )

        print("Initiate fetch.")

        results = await asyncio.gather(
            # # export_master
            # product.fetch(
            #     client, url=Endpoints.EXPORT_URL, payload=payload_master_product
            # ),
            # # export_stock
            # stock.fetch(client, url=Endpoints.EXPORT_URL, payload=payload_stock),
            # export_d2c
            order.fetch(client, url=Endpoints.EXPORT_URL, payload=payload_d2c),
            # export_b2b
            order.fetch(client, url=Endpoints.EXPORT_URL, payload=payload_b2b),
        )

        print("Fetch complete.")


if __name__ == "__main__":
    asyncio.run(main())
