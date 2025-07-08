from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    TIMESTAMP,
)


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    hash_password = Column(String(50), unique=True, nullable=False)