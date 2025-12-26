from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class StockRow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    block_id: Optional[str] = Field(alias="ブロックID")
    block_short_name: Optional[str] = Field(alias="ブロック略称")
    loc: Optional[str] = Field(alias="ロケーション")
    item_id: Optional[str] = Field(alias="商品ID")
    stock_qty: Optional[str] = Field(alias="在庫数(引当数を含む)")
    assign_qty: Optional[str] = Field(alias="引当数")
    last_arv_date: Optional[str] = Field(alias="最終入荷日")
    last_ship_date: Optional[str] = Field(alias="最終出荷日")
