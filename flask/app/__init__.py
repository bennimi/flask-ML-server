# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 17:36:21 2021

@author: bennimi
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

if app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
    
print("App config loaded: ", app.config["ENV"], flush=True)



#__all__ = ['views','helper_functions']
#from app import error_handlers
#from app import helper_functions
#from app import views
