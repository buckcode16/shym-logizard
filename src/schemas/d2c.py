from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class D2CRow(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cust_id: Optional[str] = Field(alias="取引先ID")
    cust_name: Optional[str] = Field(alias="取引先名")
    ship_define_date: Optional[str] = Field(alias="出荷確定日")
    ship_qty: Optional[str] = Field(alias="出荷数")
    item_id: Optional[str] = Field(alias="商品ID")
    duties_type: str = "mailorder"
    # request_date: Optional[str] = Field(alias="注文日")
