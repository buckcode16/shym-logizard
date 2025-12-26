import asyncio

from src.database.engine import engine
from src.database.models.base import Base
from src.database.models.order import Order
from src.database.models.product import Product
from src.database.models.stock import Stock


async def init_tables():
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_tables())
