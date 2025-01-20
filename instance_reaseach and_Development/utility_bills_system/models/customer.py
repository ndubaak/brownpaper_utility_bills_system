#!/usr/bin/python3
"""Module for a customer detail for utility payment"""
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column, ForeignKey
from sqlalchemy.orm import relationship


class Customer(BaseModel, Base):
    """Representation for customer"""
    __table_args__ = {'extend_existing': True}
    __tablename__ = "customers"


    fullname = Column(String(128), unique=True, nullable=False)
    address = Column(String(128))
    phone_number = Column(String(128))
    user_id = Column(String(60), ForeignKey("users.id"))
    utilities = relationship("Utility", overlaps="customers,utilities")
    payments = relationship("Payment")
