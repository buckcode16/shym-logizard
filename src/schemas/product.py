from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class ProductRow(BaseModel):
    # !revisit what is ConfigDict
    model_config = ConfigDict(populate_by_name=True)

    item_id: Optional[str] = Field(alias="商品ID")
    item_name: Optional[str] = Field(alias="商品名")
    barcode: Optional[str] = Field(alias="バーコード")
    search_name: Optional[str] = Field(alias="検索名称")
    search_name2: Optional[str] = Field(alias="検索名称2")
    buyer_price: Optional[str] = Field(alias="仕入単価")
    del_flg: Optional[str] = Field(alias="削除フラグ")
    create_dttm: Optional[str] = Field(alias="登録日時")
    update_dttm: Optional[str] = Field(alias="変更日時")
    item_rsv_col001: Optional[str] = Field(alias="商品予備項目００１")
    item_rsv_col002: Optional[str] = Field(alias="商品予備項目００２")
    item_rsv_col003: Optional[str] = Field(alias="商品予備項目００３")
    item_rsv_col004: Optional[str] = Field(alias="商品予備項目００４")
    item_rsv_col005: Optional[str] = Field(alias="商品予備項目００５")
    item_rsv_col006: Optional[str] = Field(alias="商品予備項目００６")
    item_rsv_col007: Optional[str] = Field(alias="商品予備項目００７")
    item_rsv_col008: Optional[str] = Field(alias="商品予備項目００８")
    item_rsv_col009: Optional[str] = Field(alias="商品予備項目００９")
    item_rsv_col010: Optional[str] = Field(alias="商品予備項目０１０")

    snapshot_dt: Optional[datetime] = None
