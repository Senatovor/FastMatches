from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.model import Base


class Shop(Base):
    match_name: Mapped[str] = mapped_column(String)
    match_edition: Mapped[int] = mapped_column(Integer)
    match_price: Mapped[int] = mapped_column(Integer)
