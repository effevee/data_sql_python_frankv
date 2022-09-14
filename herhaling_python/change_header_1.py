#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 19:39:59 2022

@author: frank
"""

lijst_zorg = []  # lege lijst
with open("/home/frank/Documents/data_sql_python_frankv/header_zorg.txt","r") as file:
    # door het bestand lopen
    for line in file:
        # lijn toevoegen aan lijst maar \n verwijderen door substring van begin tot einde !
        lijst_zorg.append(line[:-1])

# als with wordt verlaten wordt het bestand gesloten
print(lijst_zorg)
    
# door lijst lopen met behulp van index, want we moeten de inhoud aanpassen
for i in range(len(lijst_zorg)):
     if not ":" in lijst_zorg[i]:
         # als geen : ga dan verder
         continue
     pos_2_points = lijst_zorg[i].index(':')
     # punt bij de eerste karakters, volgende lijn
     if "." in lijst_zorg[i][:pos_2_points]:
         continue
     # indien getal voor dubbelpunt groter is dan 6
     if int(lijst_zorg[i][:pos_2_points])>=6:
         oud = int(lijst_zorg[i][:pos_2_points])
         nieuw=oud+2 # met 2 verhogen
         # vervang het oude getal door het nieuwe
         lijst_zorg[i]=lijst_zorg[i].replace(str(oud),str(nieuw),1)
         
print('gewijzigde lijst:')
print(lijst_zorg)

# lijst wegschrijven naar nieuw bestand
with open("/home/frank/Documents/data_sql_python_frankv/header_zorg_changed.txt","w") as file:
    for line in lijst_zorg:
        file.write(line+"\n")

