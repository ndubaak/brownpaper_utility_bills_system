#!/usr/bin/python3
""" Module represenntation for a utility payment system
"""
from datetime import datetime
import uuid
#import models
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()

class BaseModel:
    """ Representation of models where all the class is inherit
    from the Base of this module for utility payment system
    """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow))

    def __init__(self, *args, **kwargs):

        formt = "%Y-%m-%dT%H:%M:%S.%f"
        #
        #self.created_at = datetime.now()
        #self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key =="updated_at":
                    value = datetime.strptime(value, formt)
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            

    def save(self):
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        dic = self.__dict__.copy()
        dic["__class__"] = self.__class__.__name__
        dic["created_at"] = self.created_at.isoformat()
        dic["updated_at"] = self.updated_at.isoformat()

        return dic

    def __str__(self):
        clas_n = self.__class__.__name__
        return "[{}] ---  ({}) -- {}".format(clas_n, self.id, self.__dict__)
    
    def __repr__(self) -> str:
        return self.__str__()

    def delete(self):
        """ Method delete the instance of the object"""
        import models 
        models.storage.delete(self)



