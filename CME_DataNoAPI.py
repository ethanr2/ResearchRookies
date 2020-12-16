# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 23:19:17 2020

@author: ethan
"""
import requests
from datetime import datetime as dt
from datetime import timedelta as td

import numpy as np
import pandas as pd

URL = "https://www.cmegroup.com/CmeWS/mvc/Quotes/Future/305/G?quoteCodes=null&_=1null"

def get_futures(path = ''):
    df = {
          'ExpirationMonth': [],
          'Last': []
          }
    now = dt.now()
    quotes = requests.get(URL).json()['quotes']
    for quote in quotes:
        if not quote['last'] == '-':
            print(quote['expirationDate'])
            stamp = str(quote['expirationDate'])
            stamp = dt.strptime(stamp, '%Y%m%d')
            df['ExpirationMonth'].append(stamp)
            df['Last'].append(float(quote['last']))
        
    df = pd.DataFrame(df)
    df['Last'] = 1 - df['Last']/100 
    df['Timestamp'] = now
    df = df.loc[:,['Timestamp', 'ExpirationMonth', 'Last']]
    
    print('CME FFR Futures:')
    print(df)
    
    df.to_csv(path + 'data/cme_ffr.csv', mode='a', header=False, index = False)
    
    return df

df = get_futures()

#%%


if __name__ == '__main__':
    data_path = __file__[:__file__.find('CME')]
    get_futures(data_path)


#%%




