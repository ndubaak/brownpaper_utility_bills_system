#!/usr/bin/python3
"""Module repesentation of the utility system
"""
import hashlib
from datetime import datetime
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Representation fusers for the reistrationn and
    login
    """
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'

    username = Column(String(128), unique=True,  nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    customer = relationship("Customer", backref="users", uselist=False)


    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def update_profile(self, new_email=None, new_password=None):
        if new_email:
            self.email = new_email
        if new_password:
            self.password = self.hash_password(new_password)
        self.updated_at = datetime.now()


