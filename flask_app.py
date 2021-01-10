# -*- coding: utf-8 -*-
"""
@author: Bennimi

info: flask app
"""

from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import pickle, sys, time, itertools, collections, glob, datetime
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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
db = SQLAlchemy(app)

# class StoreTweets(db.Model):
#     id = db.Columns(db.Integer,primary_key=True)
#     timestamp = db.Columns(db.DateTime,default=datetime.datetime.now)
#     tweet = db.Columns(db.String(),nullable=True)
    
#     def __repr__(self):
#         return '<tweet %r>' %self.id 


#all_files = glob.glob(path+"*.pkl")
model = pickle.load(open(path+model_name+".pkl", 'rb'))

context = {'title':"predict tweets",
               'header':"About this page"}

@app.route('/')
def project_home():
    return render_template('about.html', context=context)

@app.route('/about')
def project_about():
    return render_template('about.html', context=context)


@app.route('/tweet',methods=['GET','POST'])
def model_predict():
    if request.method == 'GET':
        return render_template('single_predict.html', context=context)
    
    in_text = request.form.get('input_tweet')   
    try:
        pred = model.predict(pd.DataFrame([in_text], columns = ['tweet']))
    except:
        redirect('/tweet')
    try:
        db.session.add()
        db.session.commit()
    except:
        pass
    
    if pred [0] == 4: pred = "This is a positive Tweet"
    else: pred = "This is a negative Tweet"
    return render_template('single_predict.html',
                           context=context,
                           pred=pred,
                           in_text=in_text)

@app.route('/file',methods=['GET','POST'])
def model_predict_file():
    
    if request.method == 'POST':
        in_file = request.files.get('input_file')
        print(in_file)
        # in_file = pd.read_csv(,names=['tweet'])
        # preds = model.predict(in_file)
        # preds_percentage = collections.Counter(preds)
        # preds_percentage_neg = round(preds_percentage[0]/preds,2)
        # print(preds_percentage_neg)
        return render_template('file_predict.html',context=context)
        
    else:
       return render_template('file_predict.html',context=context)
    

    #return str(preds_percentage_neg) + " of tweets are negative\n\n" + str((preds))


if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',port=8000) #,debug=True)
  