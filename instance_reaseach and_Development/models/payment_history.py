#!/usr/bin/python3
"""Module for a customer detail for utility payment"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Float, Column, DateTime ,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class PaymentHistory(BaseModel, Base):
    """Representation for customer"""
    __table_args__ = {'extend_existing': True}
    __tablename__ = "payment_histories"


    status = Column(String(60), nullable=False)
    transaction_date = Column(DateTime, default=(datetime.now()), nullable=False)
    company_name = Column(String(128), nullable=False)
    payment_id  = Column(String(60), ForeignKey("payments.id"))
    payment = relationship('Payment', back_populates='payment_histories')