#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 18:02:01 2022

@author: frank
"""

import pandas as pd
from db_actions import actions

#constructor klasse oproepen met default waarden voor connectie
dba=actions()

# connecteren met de databank
dba.connect()

# inlezen csv in dataframe
df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_station_info.csv')

# we willen enkel de 2 eerste kolommen in een nieuw dataframe
df_info_station=df[['Station code','Station name(district)']]

# kolommen hernoemen
df_info_station.columns=['id','name']

# kolom gegevens in lijst steken
data=list(zip(df_info_station['id'],df_info_station['name']))

# insert query
insert_query='''INSERT INTO station_info(id,name) values(%s,%s)'''

# gegevens webschrijven naar tabel
dba.write_small_df_to_dbtable(insert_query, data)
    
# database afsluiten
dba.quitdb()
