# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 17:29:12 2018

@author: kutouxiyiji
"""

from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import json as sjson
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models.formatters import DatetimeTickFormatter
app = Flask(__name__)

app_vars={}

def newdf(ticker='GOOG'):
    if app_vars["period"]=="month":
        start_date=pd.to_datetime('today')-pd.Timedelta('31 days')
        date_array=pd.date_range(start_date,periods=31)
    else:
        start_date=pd.to_datetime('today')-pd.Timedelta('365 days')
        date_array=pd.date_range(start_date,periods=365)
    dates=",".join(date_array.strftime('%Y-%m-%d'))

    key= U7kaTHzg1MovTyXi6qCJ #API key

    parameters={'ticker':ticker,'date':dates,'api_key':key}
    url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json'

    try:
        r=requests.get(url, params=parameters)
        d=sjson.loads(r.text)
        cols = [a['name'] for a in d['datatable']['columns']]
        data=d['datatable']['data']
        df = pd.DataFrame(data=data,columns=cols)
        df["date"]=df["date"].apply(pd.to_datetime).dt.date
        app_vars['df']=df
        app_vars["code"]="success"
    except:
        app_vars["code"]="failed"
        
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
def create_figure():
    df=app_vars['df']
    p=figure(title="Stock Prices",tools=TOOLS)
    p.xaxis.axis_label='Date'
    p.xaxis.formatter=DatetimeTickFormatter(days=['%m/%d'])
    if app_vars['c1']:
        p.line(df["date"],df["close"],color='blue',line_width=1,legend=app_vars['ticker']+': Closing Price')
    if app_vars['c2']:
        p.line(df["date"],df["adj_close"],color='green',line_width=1,legend=app_vars['ticker']+': Adjusted Closing Price')
    if app_vars['c3']:
        p.line(df["date"],df["open"],color='yellow',line_width=1,legend=app_vars['ticker']+': Opening Price')
    if app_vars['c4']:
        p.line(df["date"],df["adj_open"],color='red',line_width=1,legend=app_vars['ticker']+': Adjusted Opening Price')
    p.legend.location='top_left'
    return p

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output',methods=['POST'])
def index2():
    app_vars['ticker']=request.form['ticker_in']
    app_vars['c1']=request.form.get('check1') != None
    app_vars['c2']=request.form.get('check2') != None
    app_vars['c3']=request.form.get('check3') != None
    app_vars['c4']=request.form.get('check4') != None
    app_vars['period']=request.form['period']
    newdf(ticker=app_vars['ticker'])
    if app_vars["code"]=="success":
        plot = create_figure()
        script,div=components(plot)
        return render_template('graph.html',script=script,div=div,ticker=app_vars['ticker'])
    else:
        return render_template('error.html',ticker=app_vars['ticker'])

if __name__ == '__main__':
    app.run(port=33507)
