# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 14:06:47 2020

@author: ethan
"""

from datetime import datetime as dt
import pandas as pd
from selenium import webdriver


URL = "https://www.fedsearch.org/fomc-docs/search;jsessionid=F21F049CB8B080588FBF12A16BA983C7?advanced_search=true&from_year=2002&search_precision=All+Words&start={}&sort=Most+Recent+First&to_month=4&to_year=2020&number=10&fomc_document_type=policystatement&Search=Search&text=&from_month=12"

with webdriver.Chrome() as driver:
    dates = []
    j = 0
    for i in range(0, 200, 10):
        driver.get(URL.format(i))
        lst = driver.find_elements_by_tag_name("p")
        
        for tag in lst:
            text = tag.text.lower()
            if "for release at " in text:
                ind = text.find("for release at ") + 15
                print(j, text[ind:ind+10])
                j = j + 1
                dates.append(text[ind:ind+10])
            #dates.append(dt.strptime(text[26:36], "%m/%d/%Y"))
            #print(dates[-1], end=", ")
        #print()
    scraped = dates
print(scraped)
#%%
dates = pd.Series(scraped)
dates = dates.drop_duplicates().sort_values(ignore_index=True)
dates.to_excel("data/dates2.xlsx")

print(dates)
#%%
