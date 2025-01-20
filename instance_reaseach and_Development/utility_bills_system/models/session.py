#!/usr/bin/python3
"""Module representation for utility system
"""
from model.basemodel import BaseModel
from datetime import datetime

class Session(BaseModel):
    """Representation of the session for managing user
    session 
    """
    session_token = ""
    expires_at = datetime.dataetime.now()

