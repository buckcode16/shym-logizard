from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class Product(Base):
    __tablename__ = "product"

    item_id: Mapped[str] = mapped_column(Text, primary_key=True)
    item_name: Mapped[str] = mapped_column(Text, nullable=True)
    barcode: Mapped[str] = mapped_column(Text, nullable=True)
    search_name: Mapped[str] = mapped_column(Text, nullable=True)
    search_name2: Mapped[str] = mapped_column(Text, nullable=True)
    buyer_price: Mapped[str] = mapped_column(Text, nullable=True)
    del_flg: Mapped[str] = mapped_column(Text, nullable=True)
    create_dttm: Mapped[str] = mapped_column(Text, nullable=True)
    update_dttm: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col001: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col002: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col003: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col004: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col005: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col006: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col007: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col008: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col009: Mapped[str] = mapped_column(Text, nullable=True)
    item_rsv_col010: Mapped[str] = mapped_column(Text, nullable=True)
