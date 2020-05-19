from flask import Flask,render_template,url_for,request,make_response
import pandas as pd 
import json
from flask_cors import cross_origin
import string
import re
import pandas as pd
import numpy as np



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',prediction = originalTitlelist)


if __name__ == '__main__':
    app.run(debug=True)
