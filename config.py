# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 19:24:51 2021

@author: bennimi
"""

class MainConfig(object):
    DEBUG = False
    TESTING = False
    

class DevelopmentConfig(MainConfig):
    DEBUG = True
    ALLOWED_FILE_UPLOAD_EXTENSIONS = ['csv','txt']
    ALLOWED_FILE_UPLOAD_SIZE = 0.2 * 1024 * 1024 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    
    
