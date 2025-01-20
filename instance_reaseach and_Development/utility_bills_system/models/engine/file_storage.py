#!/usr/bin/python3
import json
import os
from models.base_model import BaseModel
#from models.payment import Payment
#from models.utility import Utility
#from models.customer import Customer
#from models.customutility import CustomerUtility
from models.user import User
"""
module store file of any instance created write and read them

"""
class FileStorage:
    """
    json file serialize and deserialize instances
        Private class attribute:
        __file_path: json file name
        __object: dictionary in python
    
    """
    __file_path = "file.json"
    __objects = {}

    #def classes(self):
        #""" modules class for utility payment system"""
        #classes = {"BaseModel": BaseModel,
                   #"User": User,
                   #"Utility": Utility,
                   #"Customer": Customer,
                   #"CustomerUtility" : CustomerUtility,
                   #"Payment": Payment}
        #return classes
    
    def all(self, cls=None):
        """Method that retrives all object created from system"""
        if cls is not None:
            dict1 = {}
            for k, v in self.__objects.items():
                   if isinstance(v, cls):
                        dict1[k] = v
            return dict1
        return FileStorage.__objects
    
    def new(self, obj):
        """Method created new object and it been store in filestorage"""
        class_n = obj.__class__.__name__
        self.__objects["{}.{}".format(class_n, obj.id)] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(FileStorage.__file_path) as f:
                obj = json.load(f)
                mydic = {}
                for key, value in obj.items():
                    clas = value['__class__']
                    mydic[key] = self.classes()[value['__class__']](**value)
                    del value['__class__']
                FileStorage.__object = mydic
        except FileNotFoundError:
            pass
