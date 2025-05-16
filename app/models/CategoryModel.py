from sqlalchemy import Integer, String, text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from app.database import Base


class Category(Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(String)

    match_id: Mapped[list['Match']] = relationship(
        'Match',
        back_populates='categories',
        cascade='all, delete-orphan')

