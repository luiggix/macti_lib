# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:13:39 2019

@author: luiggi
"""

def get_all(name):
    print(name)
    
def get_objects(name, obj):
    print(name, obj)
    return obj

import h5py
f = h5py.File('test01.h5','r')

for key in f.keys():
   print(key)

print(f['mesh'])
print(f['vars'])

print('-'*30)
print(' visit() ')
print('-'*30)
f.visit(get_all)
print('-'*30)
print(' visititems() ')
print('-'*30)
g = f.visititems(get_objects)
print(g)
print('-'*30)
print('--> malla ')
malla = f['mesh']
print('-'*30)

for i in malla.attrs:
    print(i, malla.attrs[i])

print('-'*30)
print('--> variables ')
print('-'*30)
variables = f['vars']

for i in variables.attrs:
    print(i, variables.attrs[i])

Nx = malla.attrs['NX'][0] ## access the first element of a numpy array
Ny = malla.attrs['NY']  ## access the full numpy array
longitud_x = malla.attrs['WX'][0]
longitud_y = malla.attrs['WY']
print('-'*30)
print(Nx, Ny, longitud_x, longitud_y)
print(type(Nx), type(Ny), type(longitud_x), type(longitud_y))

print('-'*30)
print('f.keys()')
print('-'*30)
for key in f.keys():
   print(key, f[key])
   atributos = f[key].attrs
   for a in atributos:
       print(a, atributos[a], type(atributos[a]))
   
   
f.close()
