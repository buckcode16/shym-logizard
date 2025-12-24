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
from src.services import product, stock

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


async def main():
    async with LogizardClient() as client:
        await client.post_json(
            Endpoints.LOGIN_URL, payload=payload_login, response_model=LoginResponse
        )

        print("Initiate fetch.")

        results = await asyncio.gather(
            # export_master
            product.fetch(
                client, url=Endpoints.EXPORT_URL, payload=payload_master_product
            ),
            # export_stock
            stock.fetch(client, url=Endpoints.EXPORT_URL, payload=payload_stock),
            # # export_d2c
            #     d2c_service.fetch(client, url=..., payload=...),
            # # export_b2b
            #     b2b_service.fetch(client, url=..., payload=...)
        )

        print("Fetch complete.")


if __name__ == "__main__":
    asyncio.run(main())
