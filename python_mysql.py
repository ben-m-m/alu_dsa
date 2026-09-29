import sqlalchemy
from sqlalchemy import String, Column, Integer, BLOB
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
import os


password = os.getenv("AIVEN_PASSWORD")
user = os.getenv("AIVEN_USER")
engine = sqlalchemy.create_engine("mysql+pymysql://avnadmin:password@user:15800/Analytics")

class Base(DeclarativeBase):
    pass

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String(255))
    n_max = Column(Integer)
    steps = Column(Integer)
    image = Column(BLOB)

Base.metadata.create_all(engine)
