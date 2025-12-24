from typing import List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

SQLModel = TypeVar("SQLModel")
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class BaseRepository:
    def __init__(self, session: AsyncSession, model: Type[SQLModel]):
        self.session = session
        self.model = model

    async def bulk_upsert(self, items: List[PydanticModel]):
        if not items:
            return

        for item in items:
            item_data = item.model_dump()

            db_item = self.model(**item_data)

            await self.session.merge(db_item)

        await self.session.commit()
