# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 22:57:06 2022

@author: gebruiker
"""

class store_df:
    
    def __init__(self,numdfs):
        self._num = numdfs
        self._dfs = []
        for i in range(numdfs):
            self._dfs.append(None)
    
    def set_df(self,pos,df):
        if pos >= self._num:
            return False
        self._dfs[pos]=df
        return True
    
    def get_df(self,pos):
        if pos >= self._num:
            return None
        return self._dfs[pos]
    
    def get_notnone_dfs(self):
        cnt = 0
        for i in range(self._num):
            if self._dfs[i] is not None:
                cnt+=1
        return cnt
    
    def clean_dfs(self):
        del self._dfs