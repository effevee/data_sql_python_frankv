#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 17:13:50 2022

@author: frank
"""

import pandas as pd
import mysql.connector as sql

# niet veilig (intern gebruik)
# eventueel gebruiker en paswoord opvragen via input
user='usr1'
passwd='hetcvo.be'
host='127.0.0.1'
db='proto1'

select_query='''select measure_time,avg(average_val)
    from air_pol_measurement where station_id=101 and measure_type_id=1 
    group by measure_time'''
    
try:
    # connectie maken met mysql database proto1 als gebruiker usr1
    cn=sql.connect(db=db,user=user,password=passwd,host=host)

    # dataframe maken van de select query
    df=pd.read_sql(select_query,cn)
    
    # kolommen hernoemen
    df.columns=['time','average']

    # tonen enkele records
    print(df.head())
    
    # tonen lijngrafiek
    df.plot.line(x='time', y='average')
    
except Exception as E:
    print('problemen met lezen uit databank')
    print(E)
finally:
    cn.disconnect()

