# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 14:06:47 2020

@author: ethan
"""

from datetime import datetime as dt
import pandas as pd
from selenium import webdriver


URL = "https://www.fedsearch.org/fomc-docs/search?advanced_search=true&to_month=12&to_year=2020&number=10&fomc_document_type=policystatement&from_year=2002&Search=Search&search_precision=All+Words&start={}&text=&sort=Most+Recent+First&from_month=12"
MAX = 40 # Maximum number of entries to look up in the Fed's search page. 


with webdriver.Chrome() as driver:
    dates = []
    j = 0
    for i in range(0, MAX, 10):
        driver.get(URL.format(i))
        lst = driver.find_elements_by_tag_name("p")
        
        for tag in lst:
            text = tag.text.lower()
            if "for release at " in text:
                ind = text.find("for release at ") + 15
                time = text[ind:ind+10]
                line = text.split('\n')[2]
                date_text = line[-17:-7] 
                
                date = dt.strptime(date_text, '%m/%d/%Y')
                if time == '2 p.m. est':
                    date = date.replace(hour = 14)
                elif time == '2 p.m. edt':
                    date = date.replace(hour = 13)
                elif time == "10 a.m. es":
                    date = date.replace(hour = 10)
                elif time == "5 p.m. edt":
                    date = date.replace(hour = 16)
                elif time == '8:00 a.m. ':
                    date = date.replace(hour = 7)
                else:
                    print(time)
                print(j, date)
                j = j + 1
                dates.append(date)

#%%
dates = pd.Series(dates)
dates = dates.drop_duplicates().sort_values(ignore_index=True)
dates.to_csv("data/dates.csv", header=  ['timestamp'])

print(dates)
#%%
