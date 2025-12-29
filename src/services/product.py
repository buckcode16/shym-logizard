import csv
from datetime import datetime, timedelta, timezone
from typing import List

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
    now = datetime.now(JST)

    if not res.data or not res.data.csv_lines:
        return []
    reader = csv.DictReader(res.data.csv_lines)

    clean_data = []
    for row in reader:
        row["snapshot_dt"] = now
        clean_data.append(ProductRow(**row))

    async with AsyncSessionLocal() as session:
        repo = BaseRepository(session, model=Product)
        await repo.bulk_upsert(clean_data)
    return clean_data
