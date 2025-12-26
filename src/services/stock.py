import csv
from typing import List

from src.api.client import LogizardClient
from src.database.engine import AsyncSessionLocal
from src.database.models.stock import Stock
from src.database.repository import BaseRepository
from src.schemas.response import ExportResponse
from src.schemas.stock import StockRow


async def fetch(client: LogizardClient, url: str, payload: dict) -> List[StockRow]:
    res = await client.post_json(url, payload, response_model=ExportResponse)

    reader = csv.DictReader(res.data.csv_lines)

    clean_data = []
    for row in reader:
        clean_data.append(StockRow(**row))

    async with AsyncSessionLocal() as session:
        repo = BaseRepository(session, model=Stock)
        await repo.replace_all(clean_data)
    return clean_data
