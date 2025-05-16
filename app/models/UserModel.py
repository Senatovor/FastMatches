from sqlalchemy import Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
import enum


class GenderEnum(str, enum.Enum):
    MALE = 'мужчина'
    FEMALE = 'женщина'
    OTHER = 'чужой'


class User(Base):
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(default=GenderEnum.OTHER, server_default=text("'OTHER'"))
