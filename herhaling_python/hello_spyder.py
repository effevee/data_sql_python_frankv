# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import math

naam = input('Wat is uw naam?\n')
# functie int zet string om naar integer
leeftijd = int(input('Wat is uw leeftijd?\n'))
print(naam, ',welkom by Spyder')
# concatinatie van strings met ,
print('De vierkantswortel van uw leeftijd is ', math.sqrt(leeftijd))
print('2de manier')
# concatinatie van strings met +
print('De vierkantswortel is '+str(math.sqrt(leeftijd)))
print('3de manier')
# machtsverheffing kan ook met **
print('De vierkantswortel is',leeftijd**0.5)
