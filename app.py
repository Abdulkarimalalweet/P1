#!/usr/bin/env python
# coding: utf-8

# In[1]:


# input to the app : 
# stock name (a.k.a ticker for instance AAPL for Apple) symbol in out case, 
# the type of the price (Open, Close, High, Low, Adj Close), 
# the dates 
# output = price is requested and sketch it like we did in the homework. The type of the chart(candlestick, line, etc..) does not matter. 


# In[2]:


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
#import unirest
import requests
from matplotlib import rcParams
import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import json
import requests
import matplotlib.dates as mdates
from flask import Flask, request
from flask import Flask, render_template
from IPython.display import display, HTML, IFrame
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
import plotly.graph_objects as go


def stock(sym, start, end, price):
    name = sym
    startdate = datetime.strptime(start, '%Y-%m-%d')
    enddate = datetime.strptime(end, '%Y-%m-%d')
    pricetype = price
    url = 'https://yahoo-finance15.p.rapidapi.com/api/yahoo/hi/history/'+ str(name) + '/1d'
    
    headers = {
    'x-rapidapi-key': "673e951a13mshe9df3409ae55508p1f23b5jsn64761284c0ab",
    'x-rapidapi-host': "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    print(response)
    
    values = response.json()
    
    values = values['items'].values()
    
    values= list(values)
    date  = []
    openp  = []
    high = []
    low  = []
    adjclose = []
    for i in values:
        date.append(i['date']) 
        openp.append(i['open'])
        high.append(i['high'])
        low.append(i['low'])
        adjclose.append(i['adjclose'])
#df = pd.DataFrame([data], columns = ['Name', 'Age'])
    df = pd.DataFrame()
    df['Date'] = date
    df['Open'] = openp
    df['High'] = high
    df['Low'] = low
    df['Adjclose'] = adjclose
    #converting the dataset to time series
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace = True , drop = False)
    
    #Part5 Find the average Low price for all four stocks 
    #between the dates 03/15/2020 (included) and 06/15/2020 (excluded).
    # to extract specific dates range
    print(startdate.year,startdate.month,startdate.day)
    print(enddate.year,enddate.month,enddate.day)
    df = df[(df['Date']>=datetime(startdate.year,startdate.month,startdate.day))]
    df =  df[(df['Date']<datetime(enddate.year,enddate.month,enddate.day))]
 
    return list(df["Date"]) , list(df[pricetype])




app = Flask(__name__)
para = []

@app.route( "/post_field" , methods=["GET", "POST"])
def need_input():
    for key, value in request.form.items():
        print("request.form.items()",request.form.items())
        para.append(value)
        print("key: {0}, value: {1}".format(key, value))
        print(para) 
    x1 , y1 = stock(para[0],para[1] ,para[2], para[3] )
    #para = []
    my_plot_div = plot([Scatter(x = x1, y = y1)], output_type='div') 
    return render_template('index2.html',
                               div_placeholder=Markup(my_plot_div)
                              )    
     

@app.route("/", methods=["GET"])
def get_form():
    return render_template('index.html')


if __name__ == "__main__": 
        app.run() 
