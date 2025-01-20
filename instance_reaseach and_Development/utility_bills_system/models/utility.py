#!/usr/bin/python3
"""Module representation of utility syetem """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, String, ForeignKey



class Utility(BaseModel, Base):
    """Repesentation of utility attribute for 
    utility payment system
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = "utilities"

    company_name = Column(String(128), nullable=False)
    service_type = Column(String(128), nullable=False)
    rate_per_unit = Column(Float, default=0.0)
    customer_id = Column(String(60), ForeignKey('customers.id'))
    customer = relationship("Customer", back_populates="utilities", overlaps="utilities,customer")
    payments = relationship("Payment")
