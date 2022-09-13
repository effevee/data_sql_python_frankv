#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 18:48:56 2022

@author: frank
"""
import time
import random
import os

aantalGoals=0
aantalBuiten=0
aantalPaal=0
aantalShots=50

def beep(duration, freq, volume):
    # sudo apt install sox
    # play -n synth <duration in seconds> sine <freq in Hz> vol <volume (0-1)>
    # redirect play warning messages to the big bucket in the sky with 2> /dev/null
    command = 'play -n -q synth %.1f sine %d vol %.1f 2> /dev/null' % (duration, freq, volume)
    #print(command)
    os.system(command)
    
    
# lus shotten
for i in range(aantalShots):
    # coordinaten shot
    x=random.randint(0, 900)
    y=random.randint(0, 500)
    # in doel ?
    # dikte paal/deklat = 10
    if x>300 and x<600 and y<220:
        print('GOAL!!!')
        beep(.1, 1600, .1)
        aantalGoals+=1
    elif x<290 or x>610 or y>230:
        print('Ohhh!!!')
        beep(.1, 400, .1)
        aantalBuiten+=1
    else:
        print('PAAL!!!')
        beep(.1, 800, .1)
        aantalPaal+=1
    # korte pauze
    time.sleep(.5)

# aantal Goals
print('Goals %d - Paal %d - Buiten %d' %(aantalGoals, aantalPaal, aantalBuiten))