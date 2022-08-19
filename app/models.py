from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from .database import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    
    _id = Column(Integer, primary_key=True, index=True)
    payer = Column(String, nullable=False)
    points = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    
