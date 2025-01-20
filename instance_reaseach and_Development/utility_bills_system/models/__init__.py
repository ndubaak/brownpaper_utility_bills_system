#!/usr/bin/python3
import sys
import os

from models.engine.dbstorage import DBStorage
from os import getenv

#if getenv('PAY_TYPE_STORAGE') == 'db':
    
storage = DBStorage()
storage.reload()

