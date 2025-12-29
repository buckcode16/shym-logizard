import csv
from datetime import datetime, timedelta
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
    start_date = (now - timedelta(days=1)).strftime("%Y%m%d")
    end_date = now.strftime("%Y%m%d")

    payload.update({"TARGET_DATE_FROM": start_date, "TARGET_DATE_TO": end_date})

    try:
        res = await client.post_json(url, payload, response_model=ExportResponse)
        if not res.data or not res.data.csv_lines:
            return []
    except Exception:
        return []

    reader = csv.DictReader(res.data.csv_lines)
    accumulator = {}
    is_d2c = payload["FILE_ID"] == "3"

    for row in reader:
        validated = D2CRow(**row) if is_d2c else B2BRow(**row)

        key = (validated.item_id, validated.ship_define_date)

        if key not in accumulator:
            accumulator[key] = {
                "item_id": validated.item_id,
                "ship_define_date": validated.ship_define_date,
                "cust_id": getattr(validated, "cust_id", None),
                "cust_name": getattr(validated, "cust_name", None),
                "ship_qty_int": 0,
            }

        accumulator[key]["ship_qty_int"] += int(validated.ship_qty or 0)

    clean_data = []
    for data in accumulator.values():
        qty_str = str(data.pop("ship_qty_int"))
        data["ship_qty"] = qty_str

        obj = D2CRow(**data) if is_d2c else B2BRow(**data)
        clean_data.append(obj)

    async with AsyncSessionLocal() as session:
        # !revisit
        repo = BaseRepository(session, model=Order)

        await repo.replace_by_date_range(
            clean_data, "ship_define_date", start_date, end_date
        )

    return clean_data
