from typing import List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

SQLModel = TypeVar("SQLModel")
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class BaseRepository:
    def __init__(self, session: AsyncSession, model: Type[SQLModel]):
        self.session = session
        self.model = model

    """
    current bulk_upsert is insufficient for the Stock and Order strategies
    for stock, we use truncate and load (t&l), since replacing all data ensure no stale 
    data or duplicates

    Scenario when not using t&l 
    (Stale): product_A, product_B, 
    latest api response show changes to product A (new qty is 0, 
    not showing in response body) 
    and B (delta +5), but since previously both product exist and incoming api resp
    do not show product A, product A in db still showing previous number, whereas,
    product B is updated. 
    Why: Because request only ask for non-zero, zero qty product is automatically 
    omitted

    (Duplicates when location change): product_A, block_A, loc_A
    When product_A changes location (block_A -> block_B), since response either changes
    existing value attributes or create, it does not check if product_A, block_A, loc_A
    cause response body is probably product_A, block_B, loc_A, which old bulk_insert
    will treat it as completely new instance, leaving product_A, block_A, loc_A 
    unchanged. Therefore now in the table there are product_A, block_A, loc_A and
    product_A, block_B, loc_A
    """

    async def bulk_upsert(self, items: List[PydanticModel]):
        # prevent empty state logic to fail silently
        if not items:
            await self.session.commit()
            return

        for item in items:
            # Pydantic to python dict
            item_data = item.model_dump()

            # Python dict to sqlalchemy model
            db_item = self.model(**item_data)

            await self.session.merge(db_item)

        await self.session.commit()

    async def replace_all(self, items: List[PydanticModel]):
        # ACID concept
        await self.session.execute(delete(self.model))

        if items:
            await self.bulk_upsert(items)
        else:
            await self.session.commit()

    async def replace_by_date_range(self, items, date_col, target_date):
        # add WHERE clause : column(date_col) == target_date
        # getattr() is used to resolve the string 'date_col' to the actual Model Attribute
        stmt = delete(self.model).where(getattr(self.model, date_col) == target_date)
        await self.session.execute(stmt)

        if items:
            await self.bulk_upsert(items)
        else:
            await self.session.commit()
