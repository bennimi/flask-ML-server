# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 03:34:08 2021

@author: bennimi
"""
from app import app
from flask import request, render_template


@app.errorhandler(500)
def aplication_error(error):
     app.logger.info("Page not found: {}".format(request.url))
     print(error,flush=True)
     return "something went wrong"