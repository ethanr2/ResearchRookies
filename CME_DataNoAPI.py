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

URL_FFR = "https://www.cmegroup.com/CmeWS/mvc/Quotes/Future/305/G?quoteCodes=null&_=1null"
URL_LIBOR = "https://www.cmegroup.com/CmeWS/mvc/Quotes/Future/1/G?quoteCodes=null&_=1null"

TITLE_FFR = 'CME FFR Futures'
TITLE_LIBOR = 'CME Eurodollar (LIBOR) Futures'

DATABASE_FFR = 'data/cme_ffr.csv'
DATABASE_LIBOR = 'data/cme_libor.csv'

ASSETS = pd.DataFrame({
    'ffr':[URL_FFR, TITLE_FFR, DATABASE_FFR],
    'libor': [URL_LIBOR, TITLE_LIBOR, DATABASE_LIBOR]
    }, index = ['url', 'title', 'database'])

def get_futures(asset_key, path="" ):
    col = ASSETS[asset_key]
    url = col['url']
    
    df = {"ExpirationMonth": [], "Last": []}
    now = dt.now()
    quotes = requests.get(url).json()["quotes"]
    for quote in quotes:
        if not quote["last"] == "-":
            stamp = str(quote["expirationDate"])
            stamp = dt.strptime(stamp, "%Y%m%d")
            df["ExpirationMonth"].append(stamp)
            df["Last"].append(float(quote["last"]))

    df = pd.DataFrame(df)
    df["Last"] = 1 - df["Last"] / 100
    df["Timestamp"] = now
    df = df.loc[:, ["Timestamp", "ExpirationMonth", "Last"]]

    print("{}:".format(col['title']))
    print(df)

    df.to_csv(path + col['database'], mode="a", header=False, index=False)

    return df

#%%
if __name__ == "__main__":
    data_path = __file__[: __file__.find("CME")]
    get_futures('ffr',data_path)
    get_futures('libor',data_path)


#%%
