#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 17:48:16 2022

@author: frank
"""

import mysql.connector as sql

def write_small_df_to_dbtable(cninfo,insert_query,data):
    
    cn=None
    cr=None
    try:
        cn=sql.connect(db=cninfo[0],user=cninfo[1],password=cninfo[2],host=cninfo[3])
        cr=cn.cursor()
    except Exception as E:
        print('Connectie probleem')
        print(E)
        return False
    
    try:
        cr.executemany(insert_query, data)
        cn.commit()
    except Exception as E:
        print('Probleem met schrijven')
        print(E)
        return False
    
    if cr is not None: cr.close()
    if cn is not None: cn.disconnect()
    