# -*- coding: utf-8 -*-
"""
@author: Bennimi

info: flask app
"""

from flask import Flask, request
import pandas as pd
import numpy as np
import pickle, sys, time, itertools, collections, glob
from sklearn.base import BaseEstimator, TransformerMixin

class TextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None, *parg, **kwarg):
        return self

    def transform(self, X):
        return X[self.key]

path = "C:/Virtual-Environments/docker-shared/airflow-setup/datasets/cleaned/"
#df_name = "checked.csv"
model_name = 'svc'

app = Flask(__name__) #run when .py is called 

#all_files = glob.glob(path+"*.pkl")


model = pickle.load(open(path+model_name+".pkl", 'rb'))


@app.route('/tweet',methods=['GET'])
def model_predict():
    
    in_text = request.args.get('tweet')
       
    #in_text = "This is a test to see if I am happy"

    pred = model.predict(pd.DataFrame([in_text], columns = ['tweet']))

    if pred[0] == 4: return "This is a postive tweet"
    if pred[0] == 0: return "This is a negative tweet"

@app.route('/tweets_csv',methods=['POST'])
def model_predict_file():
    in_file = pd.read_csv(request.files.get('csv_file'),names=['tweet'])
    preds = model.predict(in_file)
    
    preds_percentage = collections.Counter(preds)
    preds_percentage_neg = round(preds_percentage[0]/preds,2)
    
    return str(preds_percentage_neg) + " of tweets are negative\n\n" + str((preds))
if __name__ == '__main__':
    app.run()