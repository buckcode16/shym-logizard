from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import DB_URL

engine = create_async_engine(DB_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
