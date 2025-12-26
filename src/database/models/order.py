from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


class Order(Base):
    __tablename__ = "order"

    cust_id: Mapped[str] = mapped_column(Text, nullable=True)
    cust_name: Mapped[str] = mapped_column(Text, nullable=True)
    ship_define_date: Mapped[str] = mapped_column(Text, primary_key=True)
    ship_qty: Mapped[str] = mapped_column(Text, nullable=True)
    item_id: Mapped[str] = mapped_column(Text, primary_key=True)
    duties_type: Mapped[str] = mapped_column(Text, nullable=True)
