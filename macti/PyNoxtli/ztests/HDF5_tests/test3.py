#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 16:57:16 2019

@author: luiggi
"""
import h5py

def h5printR(item, leading = ''):
    for key in item:
#        print('---',item[key],'---')
        if isinstance(item[key], h5py.Dataset):
            print(leading + key + ': ', item[key])
            print(leading + '->  shape: ' + str(item[key].shape))
            print(leading + '->  dtype: ' + str(item[key].dtype))
            print(leading + '->   name: ' + str(item[key].name))
            print(leading + '-> parent: ' + str(item[key].parent))
            print(leading + '->   file: ' + str(item[key].file))
        elif isinstance(item[key], h5py.Group):
            print(leading + key + ' ' + str(item[key]))
            h5printR(item[key], leading + '  ')
        else:
            print(leading + key + ' ' + str(item[key]))
    
        atributos = item[key].attrs
        for a in atributos:
            print(leading, '   atributtes :', a, atributos[a], type(atributos[a]))
        
# Print structure of a `.h5` file            
def h5print(filename):
    with h5py.File(filename, 'r') as h:
        print(filename)
        h5printR(h, '  ')


archivo = 'test01.h5'
        
h5print(archivo)

