from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, Float


class Base(DeclarativeBase):
    pass


class PriceList(Base):
    __tablename__ = 'price_list'
    id = Column(Integer, primary_key=True, index=True)

    edition = Column(Integer)
    price = Column(Float)
    all_price = Column(Integer)

    match_id = Column(Integer, ForeignKey('safety_match.id'))


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, index=True)

    comment = Column(String)
    stars = Column(Integer)

    match_id = Column(Integer, ForeignKey('safety_match.id'))


class SafetyMatch(Base):
    __tablename__ = 'safety_match'
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    description = Column(String)
    price_list = relationship("PriceList", backref="safety_match", cascade="all, delete-orphan")
    commentaring = relationship("Comment", backref="safety_match", cascade="all, delete-orphan")
    time = Column(Integer)
    star = Column(Integer)
    expected_price = Column(Integer)
    img = Column(String)

    cat_id = Column(Integer, ForeignKey('cat.id'))


class MatchCat(Base):
    __tablename__ = 'cat'
    id = Column(Integer, primary_key=True, index=True)

    catagory = Column(String)

    cat_id = relationship("SafetyMatch", backref="match_cat", cascade="all, delete-orphan")


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True, index=True)

    match_name = Column(String)
    match_edition = Column(Integer)
    match_price = Column(Integer)
