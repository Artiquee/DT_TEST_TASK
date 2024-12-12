from sqlalchemy import Column, String, Integer
from src.database import Base


class Mission(Base):
    __tablename__ = 'missions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    cat_id = Column(Integer, nullable=True)
    is_complete = Column(Integer, default=0)


class Target(Base):
    __tablename__ = 'targets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(String)
    complete = Column(Integer, default=0)
    mission_id = Column(Integer, nullable=False)
