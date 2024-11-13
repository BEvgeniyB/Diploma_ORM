from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text


class Base(DeclarativeBase): pass



class A_Cinema(Base):
    __tablename__ = "app_cinema"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    movie_duration = Column(String)
    movie_year = Column(Integer)
    genres = Column(String)
    countries = Column(String)


