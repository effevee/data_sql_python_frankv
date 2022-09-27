#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 15:03:58 2022

@author: frank
"""

import mysql.connector as sql
import pandas as pd

# niet veilig (intern gebruik)
# eventueel gebruiker en paswoord opvragen via input
user='dev1'
passwd='hetcvo_2022.be'
host='127.0.0.1'
db='proto1'

df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_info.csv',\
               dtype={'Station code':'int8', 'Item code':'int8', 'Instrument status':'int8', \
                      'Average value':'float16','Measurement date':'string'})
    
insert_query='''INSERT INTO air_pol_measurement(measure_time,station_id,
measure_type_id,average_val,sensor_state) values(%s,%s,%s,%s,%s)'''

# connectie maken met mysql database proto1 als gebruiker dev1
cn=sql.connect(db=db,user=user,password=passwd,host=host)
# om queries te kunnen uitvoeren heb je een cursor object nodig
cr=cn.cursor()
print('got cursor:',cr)

data=list(zip(df['Measurement date'],df['Station code'],df['Item code'],
              df['Average value'],df['Instrument status']))

try:
    cr.executemany(insert_query, data)
    cn.commit()
except Exception as E:
    print('problemen met schrijven naar databank')
    print(E)
    
cr.close() # cursor afsluiten
cn.disconnect()  # connectie met database afsluiten