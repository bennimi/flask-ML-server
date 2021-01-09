# -*- coding: utf-8 -*-
"""
@author: Bennimi

info: flask app
"""

from flask import Flask, request, render_template
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

#path = "C:/Virtual-Environments/docker-shared/airflow-setup/datasets/cleaned/"
path = "/usr/app/"
model_name = 'svc'

app = Flask(__name__) #run when .py is called 

#all_files = glob.glob(path+"*.pkl")

model = pickle.load(open(path+model_name+".pkl", 'rb'))

@app.route('/about')
def project_about():
    context = {'title':"About",
               'header':"About this page"}

    return render_template('about.html', context=context)


@app.route('/tweet',methods=['GET','POST'])
def model_predict():
    context = {'title':"predict tweets",
               'header':"About this page"}

    in_text = request.form.get('input_tweet')   
    #in_text = "This is a test to see if I am happy"
    
    if not in_text:
        return render_template('single_predict.html',context=context)
    
    pred = model.predict(pd.DataFrame([in_text], columns = ['tweet']))

    #if pred[0] == 4: return "This is a postive tweet"
    #if pred[0] == 0: return "This is a negative tweet"
    return render_template('single_predict.html',
                           context=context,pred=pred[0],
                           in_text=in_text)

@app.route('/tweets_csv',methods=['POST'])
def model_predict_file():
    in_file = pd.read_csv(request.files.get('csv_file'),names=['tweet'])
    preds = model.predict(in_file)
    
    preds_percentage = collections.Counter(preds)
    preds_percentage_neg = round(preds_percentage[0]/preds,2)
    
    return str(preds_percentage_neg) + " of tweets are negative\n\n" + str((preds))
if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',port=8000) #,debug=True)
  