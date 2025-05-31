from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.model import Base


class Category(Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)

    matches: Mapped[list['Match']] = relationship(
        'Match',
        backref='categories',
        cascade='all, delete-orphan')
