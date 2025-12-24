import csv
from typing import List

# delete on prod
import pandas as pd

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
        # Strict validation handled by Pydantic here
        clean_data.append(StockRow(**row))

    # allow debugger to run and open dwranger
    # df = pd.DataFrame([row.model_dump() for row in clean_rows])
    # print(df)

    async with AsyncSessionLocal() as session:
        repo = BaseRepository(session, model=Stock)
        await repo.bulk_upsert(clean_data)
    return clean_data
