# -*- coding: utf-8 -*-
"""
@author: Bennimi

info: flask app
"""
from app import app, db
from flask import request, render_template, redirect, make_response, jsonify, abort
from werkzeug.utils import secure_filename
from sqlalchemy.ext.automap import automap_base
import pandas as pd
#import numpy as np
import os, pickle, sys, io, csv, time, itertools, collections, glob, datetime
from app.helper_functions import CustomUnpickler


# check file specs matching config
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

# print in logs file_predict(test purpose)
def print_logs(name_file,in_file_shape,preds,preds_percentage_neg):
    print("--> Uploaded file name: " + name_file, flush=True)
    print("Shape of input: {}".format(in_file_shape),flush=True)
    print("--> Predictions: {}".format(preds), flush=True)
    print("--> Percentage of negative tweets in upload: {}".format(preds_percentage_neg),flush=True)


# init connection to already existing db table
try: 
    Base = automap_base()
    Base.prepare(db.engine,reflect=True)
    tweet_table = Base.classes.tweets_data
except Exception as e: print("While connecting to DB, an error has occured: \n"+ str(e),flush=True)

# data inserter
def db_insert_data(tweets,preds):
    for idx, tweet in enumerate(tweets):
        pred = int(preds[idx]) # need to be converted from np.int to int
        try:
            tweet_insert = tweet_table(timestamp_col=datetime.datetime.now(), tweets_org=tweet, predictions=pred)
            db.session.add(tweet_insert)
            db.session.commit()
            print("DB commit successful: {}".format(tweet),flush=True)
        except Exception as e:
            print("While commiting to DB, an error has occured: {}\n{}".format(tweet,str(e)),flush=True)
        

# load model 
 
#all_files = glob.glob(path+"*.pkl")
path = app.config['MODEL_IMPORT_PATH']
model_name = 'svc'
#model = pickle.load(open(path+model_name+".pkl", 'rb'))
model = CustomUnpickler(open(path+model_name+".pkl", 'rb')).load()


@app.route('/')
def project_home():
    return render_template('about.html', title='start')

@app.route('/about')
def project_about():
    #abort(500)
    return render_template('about.html', title='home')


@app.route('/tweet',methods=['GET','POST'])
def model_predict():
    if request.method == 'GET':
        return render_template('single_predict.html', title='predict tweet')
    
    in_text = request.form.get('input_tweet')   
    pred = model.predict(pd.DataFrame([in_text], columns = ['tweet']))
    db_insert_data([in_text],pred)
 
    if pred [0] == 4: pred = "This is a positive Tweet"
    else: pred = "This is a negative Tweet"
    return render_template('single_predict.html',
                           title='predicted!',
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
        
            size_file = allowed_filesize(request.files['inputfile'])
            if not size_file <= app.config["ALLOWED_FILE_UPLOAD_SIZE"]: 
                print("Uploaded file exceeded the size limit {}: {}".format(app.config["ALLOWED_FILE_UPLOAD_SIZE"],
                                                                        size_file),flush=True)
                return redirect(request.url)
            
            ### if save to filesytem..
            #name_file = secure_filename(name_file)  
            
            in_file = pd.read_csv(request.files['inputfile'],index_col=None, names=['tweet'])
            
            if not pd.api.types.is_string_dtype(in_file['tweet']):
                print("Invalid input structure",flush=True)
                #return make_response(jsonify({'valid_structure':'False'}),222)
                return render_template('file_predict.html', title='predict tweets',structure_file ='invalid')
            
            #for row in in_file.iterrows():
            #    print(row,flush=True)
            
            ### there might be a problem if cleaned tweets are empty... solution pending (change pre-processing?!)
            preds = model.predict(in_file)
            
            db_insert_data(in_file['tweet'],preds)
            
            preds_percentage = collections.Counter(preds)
            preds_percentage_neg = round(preds_percentage[0]/len(preds),2)
            print_logs(name_file,in_file.shape,preds,preds_percentage_neg)
            
            results_response = list(zip(preds.tolist(),in_file.tweet.to_list()))
            #results_response = {'predictions': preds.tolist(), 'tweets': in_file.tweet.to_list()}
            
            return render_template('file_predict.html',results_response = results_response)
        else:
           return redirect(request.url) 
    else:
        return render_template('file_predict.html')

    
@app.route('/eventtrigger',methods=['POST'])
def input_event_trigger():
    if request.method == 'POST':
        received_info = request.get_json()
        print(received_info,flush=True)
        if not allowed_extensions(received_info['filename']): valid_extension = 'False'
        else: valid_extension = 'True'
        
        if not received_info['filesize'] <= app.config["ALLOWED_FILE_UPLOAD_SIZE"]: valid_filesize = 'False'
        else: valid_filesize = 'True'

        trigger_response = make_response(jsonify({'valid_extension':[
                                {'status':valid_extension, 'extensions': app.config["ALLOWED_FILE_UPLOAD_EXTENSIONS"]}
                                ],
                                'valid_filesize':[
                                 {'status':valid_filesize, 'filesize': app.config["ALLOWED_FILE_UPLOAD_SIZE"]},  
                                 ]
                                }
                                ),200)
        return trigger_response


if __name__ == '__main__':
     #app.run(host='localhost',port=8000) #,debug=True) # to run on windows directly
     #app.run(host='0.0.0.0',port=8000) #,debug=True)
     
     app.run()  #defs in docker files
  