#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 18:31:35 2022

@author: frank
"""

# tuple definieren met ronde haken
wind_richting = ('noord', 'oost', 'zuid', 'west')
# tuples kan je niet wijzigen
#wind_richting[0] = "noord-oost"
print(wind_richting[1])

# dictionary begint met { key:value, key:value, ... }
persoon = {'naam':'Julius', 'leeftijd':102}
persoon['leeftijd']=80
print(persoon)
# key:value paar toevoegen
persoon.update({'schoenmaat':45})
print(persoon)
persoon.update({'leeftijd':60})
print(persoon)
# waarde van key opvragen
waarde = persoon.get('leeftijd', 'unknown')
print(waarde)
# key:value verwijderen uit dictionary
persoon.pop('schoenmaat')
print(persoon)
# aantal elementen in dictionary
print(len(persoon))