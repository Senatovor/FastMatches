from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import os
from db_classes import Base
from parser import give, url_content


db_name = 'sql_app.db'
SQLALCHEMY_DATABASE_URL = f'sqlite:///instance/{db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


if not os.path.isfile("instance/sql_app.db"):
    Base.metadata.create_all(bind=engine)
    match_cats = give(url_content)
    for match_cat in match_cats:
        db.add(match_cat)
        db.commit()
