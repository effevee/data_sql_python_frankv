#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 17:48:16 2022

@author: frank
"""

import mysql.connector as sql
import pandas as pd

class actions:
    # constructor van de klasse actions
    def __init__(self,db='proto1',host='127.0.0.1',usr='dev1',pwd='hetcvo_2022.be'):
        # properties van de klasse actions
        # _ voor de naam = private memeber (afspraak)
        self._user=usr
        self._password=pwd
        self._host=host
        self._db=db
        self._cn=None  # eigenschap die het connectie object bijhoudt. Initieel op None
        
    # method om connectie met database op te zetten
    def connect(self):
        try:
            self._cn=sql.connect(db=self._db,host=self._host,user=self._user,password=self._password)
        except Exception as E:
            print('Probleem connectie databank')
            print(E)
        
    # method om connectie met database af te sluiten
    def quitdb(self):
        if self._cn is not None:
            self._cn.disconnect()
            
    # method om (een stuk van) een dataframe in database tabel in te voegen
    def write_small_df_to_dbtable(self,query,data):
        if self._cn is not None:
            cr = self._cn.cursor()
            try:
                cr.executemany(query,data)
                self._cn.commit()
                cr.close()
                return True
            except Exception as E:
                print('Probleem schrijven data')
                print(E)
                return False
            
    # method om een select query op een database tabel in een dataframe te stoppen
    def read_df_from_dbtable(self,query,data):
        if self._cn is not None:
            try:
                df=pd.read_sql(query,self._cn,params=data)
                return df
            except Exception as E:
                print('Probleem lezen data')
                print(E)
                return None
        else:
            return None
        
