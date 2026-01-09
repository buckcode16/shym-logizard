import csv
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from src.api.client import LogizardClient
from src.database.engine import AsyncSessionLocal
from src.database.models.product import Product
from src.database.repository import BaseRepository
from src.schemas.product import ProductRow
from src.schemas.response import ExportResponse


async def fetch(client: LogizardClient, url: str, payload: dict) -> List[ProductRow]:
    # ExportResponse is base pydantic class for all LZ export endpoint
    res = await client.post_json(url, payload, response_model=ExportResponse)

    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST).replace(tzinfo=None)

    if not res.data or res.data.csv_lines is None:
        raise ValueError(f"API Error: No data returned for {payload.get('range_key')}")
    reader = csv.DictReader(res.data.csv_lines)

    accumulator: Dict[str, dict] = {}

    for row in reader:
        item_id = row.get("商品ID")
        barcode = row.get("バーコード")

        if not item_id:
            continue

        if item_id not in accumulator:
            accumulator[item_id] = {"row_data": row, "barcodes": set()}

        if barcode:
            accumulator[item_id]["barcodes"].add(barcode)

    clean_data = []

    for item in accumulator.values():
        row = item["row_data"]
        barcode_set = item["barcodes"]

        if barcode_set:
            row["バーコード"] = ",".join(sorted(barcode_set))
        else:
            row["バーコード"] = None

        row["snapshot_dt"] = now
        clean_data.append(ProductRow(**row))

    async with AsyncSessionLocal() as session:
        repo = BaseRepository(session, model=Product)
        await repo.bulk_upsert(clean_data)

    return clean_data
