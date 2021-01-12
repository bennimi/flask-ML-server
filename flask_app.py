# -*- coding: utf-8 -*-
"""
@author: Bennimi

info: flask app
"""

from flask import Flask, request, render_template, redirect, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import pickle, sys, io, csv, time, itertools, collections, glob, datetime
from sklearn.base import BaseEstimator, TransformerMixin

class TextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None, *parg, **kwarg):
        return self

    def transform(self, X):
        return X[self.key]

def allowed_extensions(name_file):
    try: extension_file = name_file.rsplit('.',1)[1] 
    except: return False
    
    if extension_file.lower() in app.config["ALLOWED_FILE_UPLOAD_EXTENSIONS"]:
        return True
    else: False

def allowed_filesize(fobj):
    if fobj.content_length:
        return fobj.content_length
    try:
        pos = fobj.tell()
        fobj.seek(0, 2)  #seek to end
        size = fobj.tell()
        fobj.seek(pos)  # back to original position
        return size
    except (AttributeError, IOError):
        pass

    # in-memory file object that doesn't support seeking or tell
    return 0  #assume small enough


#path = "C:/Virtual-Environments/docker-shared/airflow-setup/datasets/cleaned/"
path = "/usr/app/"
model_name = 'svc'

app = Flask(__name__) #run when .py is called 
app.config["ALLOWED_FILE_UPLOAD_EXTENSIONS"] = ['csv','txt']
app.config["ALLOWED_FILE_UPLOAD_SIZE"] = 0.2 * 1024 * 1024 
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
        if request.files:
            
            name_file = request.files['inputfile'].filename  
            if not allowed_extensions(name_file):
                print("File extension validation was apparently bypassed, please check...",flush=True)
                return redirect(request.url)
        
            length_file = allowed_filesize(request.files['inputfile'])
            if not length_file <= app.config["ALLOWED_FILE_UPLOAD_SIZE"]: 
                print("Uploaded file exceeded the size limit {}: {}".format(app.config["ALLOWED_FILE_UPLOAD_SIZE"],
                                                                        length_file),flush=True)
                return redirect(request.url)
            
            ### if save to filesytem..
            #name_file = secure_filename(name_file)  

            in_file = pd.read_csv(request.files['inputfile'],index_col=None, names=['tweet'])
            print("--> Uploaded file name: " + name_file, flush=True)
            print("Shape of input: {}".format(in_file.shape),flush=True)
            #for row in in_file.iterrows():
            #    print(row,flush=True)
            preds = model.predict(in_file)
            print("--> Predictions: {}".format(preds), flush=True)
            preds_percentage = collections.Counter(preds)
            preds_percentage_neg = round(preds_percentage[0]/len(preds),2)
            print("--> Percentage of negative tweets in upload: {}".format(preds_percentage_neg),flush=True)
            return redirect(request.url)
        else:
           return redirect(request.url) 
    else:
        return render_template('file_predict.html',context=context)
    
@app.route('/eventtrigger',methods=['POST'])
def input_event_trigger():
    if request.method == 'POST':
        trigger_response = make_response(jsonify({'event_trigger':"True"}),2002)
        return trigger_response

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0',port=8000) #,debug=True)
  