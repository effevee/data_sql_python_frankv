#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 20:52:52 2022

@author: frank
"""

import requests       # om webpagina's aan te spreken
import lxml.html      # om html en xml te lezen
import pandas as pd   # bib voor data analyse
import sys

URL='https://www.tiobe.com/tiobe-index/'

res=requests.get(URL) # connectie maken met website
if res.status_code != 200:  # kijken of status 200 (=OK) is
    sys.exit()

pg = res.content  # haal pagina op

html = lxml.html.fromstring(pg)  # maak html object
table = html.xpath('//*[@id="top20"]')  # haal tabel op
head = table[0].xpath('//*[@id="top20"]/thead')  # haal header tabel op
cols = []
for i in range(1,7):
    col = head[0].xpath('//*[@id="top20"]/thead/tr/th['+str(i)+']')
    cols.append(col[0].text)  # tekst ophalen die bij th staat
print(cols)