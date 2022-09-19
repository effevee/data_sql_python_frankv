#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:52:52 2022

@author: frank
"""

import requests            # om webpagina's aan te spreken
import lxml.html           # om html en xml te lezen
import pandas as pd        # bib voor data analyse
#import matplotlib.pyplot as plt   # om grafieken te maken
import sys

URL='https://www.tiobe.com/tiobe-index/'

res=requests.get(URL) # connectie maken met website
if res.status_code != 200:  # kijken of status 200 (=OK) is
    sys.exit()

pg=res.content  # haal webpagina op
html=lxml.html.fromstring(pg)  # maak html object
table=html.xpath('//*[@id="top20"]')  # haal tabel op
head_table=table[0].xpath('//*[@id="top20"]/thead')  # haal header tabel op
cols=[]  # lijst met header teksten
for i in range(1,7):  # door de headers lopen
    col = head_table[0].xpath('//*[@id="top20"]/thead/tr/th['+str(i)+']')
    cols.append(col[0].text)  # tekst ophalen die bij th staat
print(cols)
print('='*80)
body_table=table[0].xpath('//*[@id="top20"]/tbody')  # haal body tabel op
data=[] # lijst voor cell teksten = 20 lijsten van 6 elementen
for rij in range(1,21): # door de 20 rijen lopen
    rij_data=[]  # lijst voor de rij cellen 
    for kol in range(1,8):  # door de 7 kolommen lopen
        if kol!=4:  # kolom 4 overslaan (figuurtje)
            cell=body_table[0].xpath('//*[@id="top20"]/tbody/tr['+str(rij)+']/td['+str(kol)+']')
            rij_data.append(cell[0].text)
    data.append(rij_data)  # rij_data toevoegen aan lijst data
print(data)
print('='*80)

df=pd.DataFrame(data,columns=cols)  # pandas dataframe maken
print(df.head())  # header + eerste 5 rijen tonen
print('='*80)

cols[2]='Change sign'  # kolom 3 hernoemen
df.columns=cols  # verandering doorvoeren
# None in de kolom vervangen door - of +
# per rij wordt het 1ste karakter uit de laatste kolom in de 3de kolom gestopt
df['Change sign']=df['Change'].str[:1]  # kolom Change sign opvullen ahv kolom Change 
print(df.head())
print('='*80)

# bij Ratings % (laatste karaketer) laten vallen en omzetten naar float
# veranderingenn moeten gebeuren in de originele dataframe
df['Ratings']=df['Ratings'].str[:-1].astype(float)

print('De stijgers')
# stijgers uit het dataframe ophalen door te filteren op +
stijgers=df[df['Change sign']=="+"]
print(stijgers.head())
print('='*80)

print('De dalers')
# dalers uit het dataframe ophalen door te filteren op -
dalers=df[df['Change sign']=='-']
print(dalers.head())
print('='*80)

print('De stijgers grafiek')
stijgers.plot.bar(x='Programming Language', y='Ratings')

print('De dalers grafiek')
dalers.plot.bar(x='Programming Language', y='Ratings')

print('Pie chart Programming Languages')
df.plot.pie(y='Ratings', figsize=(20,20), autopct='%1.1f%%', labels=list(df['Programming Language']))
