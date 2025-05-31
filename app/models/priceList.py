from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database.model import Base


class PriceList(Base):
    __tablename__ = 'price_lists'

    edition: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    all_price: Mapped[int] = mapped_column(Integer)

    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'))
