from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from app.database.model import Base


class Comment(Base):
    content: Mapped[str] = mapped_column(String(300), nullable=False)
    star: Mapped[int] = mapped_column(Integer())

    match_id: Mapped[int] = mapped_column(ForeignKey('matches.id'))

    @validates('star')
    def validate_star(self, key, value):
        if not 0 <= value <= 5:
            raise ValueError('Звезда должна быть от 0 до 5')
        return value
