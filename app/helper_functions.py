# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 21:51:16 2021

@author: bennimi
"""

from sklearn.base import BaseEstimator, TransformerMixin
import pickle

class TextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None, *parg, **kwarg):
        return self

    def transform(self, X):
        return X[self.key]
    

class CustomUnpickler(pickle.Unpickler):
    """
    found on:
    https://stackoverflow.com/questions/27732354/unable-to-load-files-using-pickle-and-multiple-modules
    """
    def find_class(self, module, name):
        if name == 'TextTransformer':
            #from app.helper_functions import TextTransformer
            return TextTransformer
        return super().find_class(module, name)
    
    
    

