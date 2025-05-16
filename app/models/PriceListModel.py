from sqlalchemy import Integer, String, text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class PriceList(Base):
    __tablename__ = 'price_lists'

    edition: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    all_price: Mapped[int] = mapped_column(Integer)

    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'))
