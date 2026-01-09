import csv
import logging
from datetime import datetime, timedelta, timezone
from typing import List

from src.api.client import LogizardClient
from src.database.engine import AsyncSessionLocal
from src.database.models.order import Order
from src.database.repository import BaseRepository
from src.schemas.b2b import B2BRow
from src.schemas.d2c import D2CRow
from src.schemas.response import ExportResponse

logger = logging.getLogger(__name__)


async def fetch(
    client: LogizardClient, url: str, payload: dict
) -> List[B2BRow | D2CRow]:
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST).replace(tzinfo=None)
    start_date = (now - timedelta(days=1)).strftime("%Y%m%d")
    end_date = now.strftime("%Y%m%d")

    # start_date = "20251206"
    # end_date = "20260104"
    # YYYYMMDD
    # API ignore more than 30 days range
    payload.update({"TARGET_DATE_FROM": start_date, "TARGET_DATE_TO": end_date})

    file_id = payload.get("FILE_ID")

    res = await client.post_json(url, payload, response_model=ExportResponse)

    if file_id == "2" and res.error_code == "4":
        logger.warning(
            f"API returned Code 4 for B2B (FileID 2). "
            f"Assuming 'No Data' and wiping range {start_date}-{end_date}."
        )
        reader = []

    # lz error code 0 is success
    elif res.error_code != "0":
        logger.error(f"API Critical Error {res.error_code}: {res.data}")
        raise ValueError(f"API returned Error Code {res.error_code}: {res.data}")

    elif not res.data or not res.data.csv_lines:
        logger.info(
            f"0 Orders found (Code 0) for FileID {file_id}. Wiping range {start_date}-{end_date}."
        )
        reader = []

    else:
        reader = csv.DictReader(res.data.csv_lines)

    accumulator = {}
    is_d2c = payload["FILE_ID"] == "3"

    if reader:
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
        data["snapshot_dt"] = now
        obj = D2CRow(**data) if is_d2c else B2BRow(**data)
        clean_data.append(obj)

    async with AsyncSessionLocal() as session:
        # !revisit
        repo = BaseRepository(session, model=Order)

        await repo.replace_by_date_range(
            clean_data, "ship_define_date", start_date, end_date
        )

    count = len(clean_data)
    logger.info(f"Processed {count} orders for range {start_date}-{end_date}.")
    return clean_data
