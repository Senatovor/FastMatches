from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from app.database.model import Base


class Match(Base):
    __tablename__ = 'matches'

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    star: Mapped[int] = mapped_column(Integer)
    expected_price: Mapped[int] = mapped_column(Integer)
    img: Mapped[str] = mapped_column(String)

    price_list: Mapped[list['PriceList']] = relationship(
        "PriceList",
        backref="match",
        cascade="all, delete-orphan")

    comments: Mapped[list['Comment']] = relationship(
        "Comment",
        backref="match",
        cascade="all, delete-orphan")

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    @validates('star')
    def validate_star(self, key, value):
        if not 0 <= value <= 5:
            raise ValueError('Звезда должна быть от 0 до 5')
        return value
