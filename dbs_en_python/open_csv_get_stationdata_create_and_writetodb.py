#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 18:02:01 2022

@author: frank
"""

import pandas as pd
#import mysql.connector as sql
import db_actions

# niet veilig (intern gebruik)
# eventueel gebruiker en paswoord opvragen via input
# cninfo is lijst met database, user, password, host
cninfo=('proto1','dev1','hetcvo_2022.be','127.0.0.1')

# insert query
insert_query='''INSERT INTO station_info(id,name) values(%s,%s)'''

# connectie maken met mysql database proto1 als gebruiker dev1
# cn=sql.connect(db=cninfo[0],user=cninfo[1],password=cninfo[2],host=cninfo[3])

# inlezen csv in dataframe
df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_station_info.csv')

# print(df.head())
# print(df.columns)

# we willen enkel de 2 eerste kolommen in een nieuw dataframe
df_info_station=df[['Station code','Station name(district)']]

# kolommen hernoemen
df_info_station.columns=['id','name']

# kolom gegevens in lijst steken
data=list(zip(df_info_station['id'],df_info_station['name']))

# tabel opvullen
status=db_actions.write_small_df_to_dbtable(cninfo, insert_query, data)
print('Status db actie:',status)
