from flask import Flask,render_template,url_for,request,make_response
import pandas as pd 
import json
from flask_cors import cross_origin
import string
import re
import pandas as pd
import numpy as np



df = pd.read_csv("dataset.csv")
originalTitlelist = df.originalTitle.values.tolist()
def process(message):
    
    def get_similar_from_originalTitle(originalTitle):
        try :
            a = df[df.originalTitle == originalTitle]["similar"].values[0]
        except :
            a = 'not found'
        return a
    def get_poster_from_index(index):
        try :
            a=df[df.originalTitle == index]["poster"].values[0]
        except :
            a = 'not found'
        return a
    
    def get_url_from_index(index):
        try :
            a=df[df.originalTitle == index]["URL"].values[0]
        except :
            a = 'not found'
        return a
    
    def get_ytb_from_index(index):
        try :
            a=df[df.originalTitle == index]["youtube"].values[0]
        except :
            a = 'not found'
        return a
    def get_year_from_index(index):
        try :
            a=df[df.originalTitle == index]["startYear"].values[0]
        except :
            a = 'not found'
        return a
    
    def get_runtime_from_index(index):
        try :
            a=df[df.originalTitle == index]["runtimeMinutes"].values[0]
        except :
            a = 'not found'
        return a
    def get_gen_from_index(index):
        try :
            a=df[df.originalTitle == index]["genres"].values[0]
        except :
            a = 'not found'
        return a
    
    def get_ar_from_index(index):
        try :
            a=df[df.originalTitle == index]["averageRating"].values[0]
        except :
            a = 'not found'
        return a
    
    def get_nv_from_index(index):
        try :
            a=df[df.originalTitle == index]["numVotes"].values[0]
        except :
            a = 'not found'
        return a
    
    def get_content_from_index(index):
        try :
            a=df[df.originalTitle == index]["content"].values[0]
        except :
            a = 'not found'
        return a

    movie_user_likes = message
    ## Step 6: Get index of this movie from its originalTitle
    movie = get_similar_from_originalTitle(movie_user_likes)
    movie = movie.replace('[','')
    movie = movie.replace(']','')
    movie = movie.replace("'",'')
    #movie0 = movie0.replace(",",'')
    movie0 = [x.strip() for x in movie.split(',')]
    
    movie0 = movie0[0:8]
    
    movie1 = []
    movie2 = []
    movie3 = []
    movie4 = []
    movie5 = []
    movie6 = []
    movie7 = []
    movie8 = []
    movie9 = []

    
    for element in movie0:
        print(element)            
        movie1.append(get_url_from_index(element))
        movie2.append(get_poster_from_index(element))
        movie3.append(get_ytb_from_index(element))
        movie4.append(get_year_from_index(element))
        movie5.append(get_gen_from_index(element))
        movie6.append(get_ar_from_index(element))
        movie7.append(get_nv_from_index(element))
        movie8.append(get_runtime_from_index(element))
        movie9.append(get_content_from_index(element))

        

    return movie0,movie1,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',prediction = originalTitlelist)

@app.route('/predict',methods=['POST'])


def predict():
    
   
    if request.method == 'POST':
        message = request.form.get('message')
        movie0,movie1,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9 = process(message)

    return render_template('result.html',movie0=movie0,movie1=movie1,movie2=movie2,movie3=movie3,movie4=movie4,movie5=movie5,movie6=movie6,movie7=movie7,movie8=movie8,movie9=movie9)



@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():


    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):


    result = req.get("queryResult")
    
    #Fetching the data points
    parameters = result.get("parameters")
    user = parameters.get("response")

    usertext = str(user)
    
  
    
    #Getting the intent which has fullfilment enabled
    intent = result.get("intent").get('displayName')
    
    #Fitting out model with the data points

    try:
        movie0,movie1,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9 = process(usertext)
    except:
        movie0 = "Not found"
    return {

    "fulfillmentMessages": [
        {
        "card": {
            "title": movie0[0],
            "subtitle": movie9[0],
            "imageUri": movie2[0],
            "buttons": [
            {
                "text": "IMDB",
                "postback": movie1[0]
            }
            ]
        }
        }
    ]
    }

if __name__ == '__main__':
    app.run(debug=True)
