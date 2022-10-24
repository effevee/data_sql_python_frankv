#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 14:08:57 2022

@author: frank
"""

import pandas as pd

# dataframe kopers
data_kopers={'name':['Jan','Ann','Piet','Kathleen','Filip','Marie','Anke'],
             'product-id':[3,2,3,1,5,4,8],
             'number':[2,5,1,7,7,3,2]}
df_kopers=pd.DataFrame(data_kopers)
print('df_kopers')
print(df_kopers)
print(' ')

# dataframe products
data_products={'product-id':[1,2,3,4,5,6,7,8],
              'name':['LEDs','breadboard','jumper cables','resistors','ULN2003','potentiometer','LDR','oled'],
              'price':[2,4,2.5,1,0.5,0.5,0.25,6]}
print('df_products')
df_products=pd.DataFrame(data_products)
print(df_products)
print(' ')

# left merge
df_left=pd.merge(df_kopers,df_products,on='product-id',how='left')
print('left merge on product-id')
print(df_left)
print(' ')

# right merge
df_right=pd.merge(df_kopers,df_products,on='product-id',how='right')
print('right merge on product-id')
print(df_right)
print(' ')

# inner merge
df_inner=pd.merge(df_kopers,df_products,on='product-id',how='inner')
print('inner merge on product-id')
print(df_inner)
print(' ')

# outer merge
df_outer=pd.merge(df_kopers,df_products,on='product-id',how='outer')
print('outer merge on product-id')
print(df_outer)
print(' ')

