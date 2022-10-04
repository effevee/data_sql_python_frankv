#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:51:24 2022

@author: frank
"""

import pandas as pd
import mysql.connector as sql

# niet veilig (intern gebruik)
# eventueel gebruiker en paswoord opvragen via input
user='dev1'
passwd='hetcvo_2022.be'
host='127.0.0.1'
db='proto1'

insert_query='''INSERT INTO measurement_type(id,name,unit) values(%s,%s,%s)'''

# connectie maken met mysql database proto1 als gebruiker dev1
cn=sql.connect(db=db,user=user,password=passwd,host=host)
# om insert queries te kunnen uitvoeren heb je een cursor object nodig
cr=cn.cursor()
print('got cursor:',cr)

# inlezen csv in dataframe
df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_item_info.csv')

# we willen enkel de 3 eerste kolommen in een nieuw dataframe
df_type_measurement=df[['Item code','Item name','Unit of measurement']]

# kolommen hernoemen
df_type_measurement.columns=['id','name','unit']

# kolom gegevens in lijst steken
data=list(zip(df_type_measurement['id'],df_type_measurement['name'],df_type_measurement['unit']))

try:
    cr.executemany(insert_query, data)
    cn.commit()
except Exception as E:
    print('problemen met schrijven naar databank')
    print(E)
    
cr.close() # cursor afsluiten
cn.disconnect()  # connectie met database afsluiten
          