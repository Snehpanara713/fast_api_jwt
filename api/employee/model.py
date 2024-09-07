from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    DateTime,
    SmallInteger,
)
from sqlalchemy.orm import relationship
from enum import Enum
from datetime import datetime

from db.database import Base


class Employee(Base):
    __tablename__ = "employee"
    emp_id = Column(Integer, primary_key=True, index=True, unique=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    password = Column(String)
    phone = Column(Integer)
    Role = Column(String(50))
    Date_of_birth = Column(Date)
