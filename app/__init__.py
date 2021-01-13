# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 17:36:21 2021

@author: bennimi
"""

from flask import Flask

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")

#__all__ = ['views','helper_functions']

#from app import helper_functions
#from app import views
