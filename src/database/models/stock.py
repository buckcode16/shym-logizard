from datetime import datetime

from sqlalchemy import DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class Stock(Base):
    __tablename__ = "stock"

    block_id: Mapped[str] = mapped_column(Text, primary_key=True)
    block_short_name: Mapped[str] = mapped_column(Text, nullable=True)
    loc: Mapped[str] = mapped_column(Text, primary_key=True)
    item_id: Mapped[str] = mapped_column(Text, primary_key=True)
    stock_qty: Mapped[str] = mapped_column(Text, nullable=True)
    # 引当数
    assign_qty: Mapped[str] = mapped_column(Text, nullable=True)
    last_arv_date: Mapped[str] = mapped_column(Text, nullable=True)
    last_ship_date: Mapped[str] = mapped_column(Text, nullable=True)

    snapshot_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
