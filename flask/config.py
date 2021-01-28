# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 19:24:51 2021

@author: bennimi
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False
    ALLOWED_FILE_UPLOAD_EXTENSIONS = ['csv','txt']
    ALLOWED_FILE_UPLOAD_SIZE = 0.2 * 1024 * 1024 
    MODEL_IMPORT_PATH = "/usr/app/app/static/Model/"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")

class DevelopmentConfig(Config):
    DEBUG = True

    
class ProductionConfig(Config):    
    DEBUG = False


