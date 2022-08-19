# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 18:47:30 2019

@author: luiggi
"""

import numpy as np

wall1 = np.array([1,2,3])
wall2 = np.array([4,5])
wall3 = np.array([7])
dirichlet = {'R':{10:wall1, 15:wall2}, 'T':{25:wall3}}
neumman = {'L':{11:wall2}, 'R':{34:wall1}, 'T':{56:1}}
for key, value in dirichlet.items():
#    print(key, ':', value)
    if key == 'R':
        for v, w in value.items():
            print(v,':', w)
    elif key == 'T':
        for v, w in value.items():
            print(v,':', w)
    else:
        print('Nada')

print('-'*50)

for key, value in neumman.items():
#    print(key, ':', value)
    if key == 'R':
        for v, w in value.items():
            print(v,':', w)
    elif key == 'T':
        for v, w in value.items():
            print(v,':', w)
    else:
        print('Nada')
        
#print(dirichlet)