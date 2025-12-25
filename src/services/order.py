import csv
from datetime import datetime
from typing import List

# delete on prod
import pandas as pd

from src.api.client import LogizardClient
from src.database.engine import AsyncSessionLocal
from src.database.models.order import Order
from src.database.repository import BaseRepository
from src.schemas.b2b import B2BRow
from src.schemas.d2c import D2CRow
from src.schemas.response import ExportResponse


async def fetch(
    client: LogizardClient, url: str, payload: dict
) -> List[B2BRow | D2CRow]:
    now = datetime.now()

    formatted_date = now.strftime("%Y%m%d")

    # payload variable (dict mutable) in memory will be extended across all reference in runtime env
    payload.update(
        {"TARGET_DATE_FROM": formatted_date, "TARGET_DATE_TO": formatted_date}
    )
    res = await client.post_json(url, payload, response_model=ExportResponse)

    reader = csv.DictReader(res.data.csv_lines)

    # clean: group and aggregate qty
    clean_data = []

    accumulator = {}
    if payload["FILE_ID"] == "3":
        for row in reader:
            validated = D2CRow(**row)

            key = (validated.item_id, validated.ship_define_date)
            if key not in accumulator:
                accumulator[key] = {
                    "item_id": validated.item_id,
                    "ship_define_date": validated.ship_define_date,
                    "cust_id": validated.cust_id,
                    "cust_name": validated.cust_name,
                    "ship_qty": 0,
                    "duties_type": "mailorder",
                }

                accumulator[key]["ship_qty"] += int(validated.ship_qty or 0)

        clean_data = list(accumulator.values())
    else:
        for row in reader:
            validated = B2BRow(**row)

            key = (validated.item_id, validated.ship_define_date)
            if key not in accumulator:
                accumulator[key] = {
                    "item_id": validated.item_id,
                    "ship_define_date": validated.ship_define_date,
                    "cust_id": validated.cust_id,
                    "cust_name": validated.cust_name,
                    "ship_qty": 0,
                    "duties_type": "wholesale",
                }

                accumulator[key]["ship_qty"] += int(validated.ship_define_qty or 0)

        clean_data = list(accumulator.values())

    # allow debugger to run and open dwranger
    # df = pd.DataFrame([row.model_dump() for row in clean_rows])
    # print(df)

    async with AsyncSessionLocal() as session:
        repo = BaseRepository(session, model=Order)
        await repo.bulk_upsert(clean_data)
    return clean_data
