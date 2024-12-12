from sqlalchemy import Column, Integer, String, Float
from src.database import Base


class Cat(Base):
    __tablename__ = 'spy_cats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
