# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:44:24 2020

@author: ethan
"""
from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td

import numpy as np
import pandas as pd
from scipy import stats

from bokeh.io import export_png,output_file,show
from bokeh.plotting import figure
from bokeh.models import NumeralTickFormatter, LabelSet,ColumnDataSource
from bokeh.models.tickers import FixedTicker
from bokeh.layouts import row, column

URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={}&interval=1min&slice=year1month{}&apikey={}'
with open('apiKey.txt') as file:
    KEY = file.read().split(',')[1]
tks = ['VGSH', 'BSV', 'VGIT', 'VGLT'] # Stock tickers

now = dt.now()
dates = pd.read_csv('data/dates.csv', index_col = 0, parse_dates = [1])[::-1]['timestamp']


# Locates the FOMC press release within the month long data
def find_mtg_window(mtg_date, prices, start = 15, end = 60):
    prices = prices.set_index('time', drop=False)
    prices = prices.loc[prices.index < mtg_date + td(minutes = end),:]
    prices = prices.loc[prices.index > mtg_date -td(minutes = start),:]
    
    return prices

# Only use this for new queries
def AV_query(month, t):
    query = pd.read_csv(URL.format(t,month,KEY))
    query['time'] = pd.DatetimeIndex(query['time'])

    return query

# Set up dictionary for queries
df = {
      'mtg_date': [],
      'ticker': [],
      'time' : [],
      'price': []
      }


for date in dates[:1]:
    month = int((now - date).days / 30) + 1
    for t in tks:
        month_data = AV_query(month, t)
        mtg_data = find_mtg_window(date, month_data)
        
        df['price'].extend(list(mtg_data['close']))
        df['time'].extend(list(mtg_data['time']))
        n = len(mtg_data['close'])
        df['mtg_date'].extend([date]*n)
        df['ticker'].extend([t]*n)
        
        print(date, t)

df = pd.DataFrame(df)
print(df)
# TODO: move this to a different function, prolly different script entirely
# Fill in blanks and index to exact release time
# for t in tks:
#     prices[t] = prices[t].fillna(method = 'ffill')
#     base = prices.loc[mtg_date, t]
#     prices[t] = prices[t]/base
#%%

from bokeh.palettes import plasma

def set_up(x, y, truncated = True, margins = None):
    if truncated: 
        b = (3 * y.min() - y.max())/2
    else:
        b = y.min()
    if margins == None:    
        xrng = (x.min(),x.max())
        yrng = (b,y.max())
    else:
        xrng = (x.min() - margins,x.max() + margins)
        yrng = (b - margins,y.max() + margins)
        
    x = x.dropna()
    y = y.dropna()
    
    return(x,y,xrng,yrng)

# Chart of non-stationary time series, e.g. NGDP from 2008 to 2020    
def chart0(df):
    xdata, ydata, xrng, yrng = set_up(df.index,df['___'])
    
    p = figure(width = 1000, height = 500,
               title= '____', 
               x_axis_label = 'Date', x_axis_type = 'datetime',
               y_axis_label = '', 
               y_range = yrng, x_range = xrng)
    p.line(xrng,[0,0], color = 'black')
    
    p.line(xdata,ydata, color = 'blue', legend = '')
    
    p.xaxis[0].ticker.desired_num_ticks = 10
    p.legend.location = 'top_left'
    p.ygrid.grid_line_color = None
    p.yaxis.formatter=NumeralTickFormatter(format="____")
    
    export_png(p,filename ='imgs/chart0.png')

    return p

# Chart of approximately stionary time series, e.g. PCE-Core inflation from 2008 to 2020
def chart1(df):
    xdata, ydata, xrng, yrng = set_up(df.index, df.stack(), truncated = False)
    marg = .005
    yrng = (yrng[0]-marg, yrng[1] + marg)
    
    p = figure(width = 1000, height = 500,
               title="Monetary Shock: March 3rd, 2020" , 
               x_axis_label = 'Time of Day', x_axis_type = 'datetime',
               #y_axis_label = '', 
               y_range = yrng, x_range = xrng)
    p.line(xrng,[0,0], color = 'black')
    
    p.line([mtg_date,mtg_date], [0,100], color ='black')
    p.line(xdata, 1, color ='black', line_dash = 'dashed')
    colors = list(plasma(len(tks))[::-1])
    for t in tks:
        p.line(xdata,df[t], color = colors.pop(), legend_label = '${}'.format(t))
    
    p.xaxis[0].ticker.desired_num_ticks = 10
    p.legend.location = 'bottom_right'
    p.ygrid.grid_line_color = None
    #p.yaxis.formatter=NumeralTickFormatter(format="0.0%")

    export_png(p, filename='imgs/chart1.png')

    return p

# Chart of a regression e.g. inflation vs money supply
def chart2(df):
    xdata, ydata, xrng, yrng = set_up(df['_'], df['_'], 
                                      truncated = False, margins = .005)
    
    p = figure(width = 500, height = 500,
               title="_" , 
               x_axis_label = '_', 
               y_axis_label = '_', 
               y_range = yrng, x_range = xrng)
    p.line(xrng,[0,0], color = 'black')
    p.line([0,0],yrng, color = 'black')
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(xdata, ydata)
    leg = 'R = {:.4f}, P-Value = {:.4e}, Slope = {:.4f}'.format(r_value,p_value,slope)
    p.line(xdata, xdata*slope + intercept, legend = leg, color = 'black')
    p.circle(xdata,ydata, color = 'blue',size = 2)
    
    p.xaxis[0].ticker.desired_num_ticks = 10
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.formatter=NumeralTickFormatter(format="0.0%")
    p.yaxis.formatter=NumeralTickFormatter(format="0.0%")
    
    export_png(p, filename='images/chart2.png')
    
    return p

# show(chart1(df))