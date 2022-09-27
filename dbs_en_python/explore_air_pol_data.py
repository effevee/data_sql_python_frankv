#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:07:18 2022

@author: frank
"""

import pandas as pd

# inlezen csv in dataframe
# df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_info.csv')
# default datatypes kolommen aanpassen
df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_info.csv',\
               dtype={'Station code':'int8', 'Item code':'int8', 'Instrument status':'int8', \
                      'Average value':'float16','Measurement date':'string'})
# eerste 5 records
print(df.head())
# statistieken van kolommen nmet getallen (aantal, gemiddelde, minimum, maximum...)
print(df.describe())
# dimensie van dataframe [aantal_rijen_df, aantal_kolommen_df]
dims=df.shape
# nagaan of dat alle kolommen zijn ingevuld
print(100*df.count()/dims[0]) # procent ingevuld
# checken van datatypes kolommen van dataframe
print(df.dtypes)
# hoeveel geheugen gebruikt dataframe
print('dataframe geheugen:', df.memory_usage(index=False,deep=True).sum())