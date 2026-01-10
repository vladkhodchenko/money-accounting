import sqlalchemy
import os

from sqlalchemy.orm import sessionmaker


DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

engine = sqlalchemy.create_engine(f"sqlite:///{DIR}/onlycash.db")

session = sessionmaker(bind=engine)
