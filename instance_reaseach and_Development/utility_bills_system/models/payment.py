#!/usr/bin/python3
"""Module for payment app for utility system"""
from models.base_model import BaseModel, Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey





class Payment(BaseModel, Base):
    """Representation of the payement class and their attribute"""
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'payments'

    amount_paid = Column(Float, default=0.0, nullable=False)
    payment_date = Column(DateTime, default=(datetime.now()), nullable=False)
    payment_method = Column(Enum('Credit card', 'Debit Card', 'Bank Transfer', 'Paypal'), name='payment methods', nullable=False)
    utility_id = Column(String(60), ForeignKey("utilities.id"))
    customer_id = Column(String(60), ForeignKey("customers.id"))
    utility = relationship('Utility', back_populates='payments')
    customer = relationship('Customer', back_populates='payments')

    payment_histories = relationship('PaymentHistory', back_populates='payment')