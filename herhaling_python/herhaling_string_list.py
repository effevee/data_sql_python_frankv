#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 20:22:41 2022

@author: frank
"""

zin = 'De 1ste les Python'  # variabele type string
temperatuur = 27.5  # variabele type float
goed_weer = True  # variabele type boolean True of False

# string is rij/lijst van karakters
print('karakter 1 uit string zin', zin[3])
# lokatie bepalen van karakter uit string
loc_1 = zin.index('1')
print('index van karakter 1: '+str(loc_1))
# de lengte van een string
print('lengte string zin:', len(zin))
# haal het laatste karakter uit de string zin
print('laatste karakter van zin:', zin[-1:])
# foutieve index in string opvangen
try:
    print('index k in string zin:',zin.index('k'))
except Exception as E:
    print('foute index', E)
    
# haal substring les uit de string zin
# substring [van:tot]  !!! niet tem !!!
print('een substring van zin:',zin[8:11])
# haal De uit de string zin
print('nog een substring uit zin:',zin[:2])
# vervang Python door SQL in de string zin
print('vervang Python door SQL in zin:',zin.replace('Python','SQL'))

# maken van een lijst
rugzak = ['brood','mes','kaas','wijn']
# lengte van de lijst
print('lengte van de lijst rugzak:',len(rugzak))
# 2de element in de rugzak
print('2de element in de rugzak:',rugzak[1])
# laatste element in de rugzak
print('laatste element in de rugzak:',rugzak[-1])
# maak een sublijst kleine_rugzak met mes en kaas
kleine_rugzak = rugzak[1:3]
print('in de kleine rugzak zitten:',kleine_rugzak)
# voeg een kaart toe aan je rugzak (op het einde)
rugzak.append('kaart')
print('rugzak:',rugzak)
# voeg op de 2de positie bestek toe aan de rugzak
rugzak.insert(1, 'bestek')
print('rugzak:',rugzak)
# laatste element uit rugzak halen
laatste=rugzak.pop()
print('laatste element:',laatste, '- rugzak heeft nu:',rugzak)
# haal mes uit rugzak met index ophalen
mes = rugzak.pop(rugzak.index('mes'))
print('gaat eruit:', mes, '- rugzak bevat nu:',rugzak)

# lijsten aan elkaar plakken met +
lijst1 = ['a', 'b', 'c']
lijst2 = ['d', 'e']
lijst = lijst1 + lijst2
print('lijst:',lijst)

# van de woorden van een string een lijst maken
lijst_zin = zin.split()
print(lijst_zin)
# van een lijst een string maken
een_string = ' '.join(lijst_zin)
print(een_string)

# string met verschillende spaties
test = 'dit is een string met veel      spaties'
print(test.split()) # zonder argument worden alle spaties verwijderd
print(test.split(' ')) # met argument 1 spatie gebeurt dat niet

# lengte van string of lijst
print('lengte lijst: ', len(lijst))