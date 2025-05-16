from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import os
from app.models.db_classes import Base
from app.parser import give, url_content
from settings import get_db_url


SQLALCHEMY_DATABASE_URL = get_db_url()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


if not os.path.isfile("instance/sql_app.db"):
    Base.metadata.create_all(bind=engine)
    match_cats = give(url_content)
    for match_cat in match_cats:
        db.add(match_cat)
        db.commit()
