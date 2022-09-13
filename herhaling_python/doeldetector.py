#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 18:48:56 2022

@author: frank
"""
import time
import random

aantalGoals= 0
aantalShots=10

# lus shotten
for i in range(aantalShots):
    # coordinaten shot
    x=random.randint(0, 900)
    y=random.randint(0, 500)
    # in doel ?
    if x>300 and x<600 and y<220:
        print('GOAL!!!')
        aantalGoals+=1
    else:
        print('Ohhh!!!')
    # korte pauze
    time.sleep(1)

# aantal Goals
print('aantal goals:', aantalGoals)