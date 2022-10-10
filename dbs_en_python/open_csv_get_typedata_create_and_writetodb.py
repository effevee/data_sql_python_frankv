#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 20:51:24 2022

@author: frank
"""

import pandas as pd
from db_actions import actions

#constructor klasse oproepen met default waarden voor connectie
dba=actions()

# connecteren met de databank
dba.connect()

# inlezen csv in dataframe
df=pd.read_csv('/home/frank/Documents/data_sql_python_frankv/Measurement_item_info.csv')

# we willen enkel de 3 eerste kolommen in een nieuw dataframe
df_type_measurement=df[['Item code','Item name','Unit of measurement']]

# kolommen hernoemen
df_type_measurement.columns=['id','name','unit']

# kolom gegevens in lijst steken
data=list(zip(df_type_measurement['id'],df_type_measurement['name'],df_type_measurement['unit']))

# insert query
insert_query='''INSERT INTO measure_type(id,name,unit) values(%s,%s,%s)'''

# gegevens webschrijven naar tabel
dba.write_small_df_to_dbtable(insert_query, data)
    
# database afsluiten
dba.quitdb()
          