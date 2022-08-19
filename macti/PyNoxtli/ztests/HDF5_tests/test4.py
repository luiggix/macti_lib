# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:50:24 2019

@author: luiggi
"""

#
# Datos del problema
#
longitud_x = 1.0 # meters
longitud_y = 1.0
Nx = 41 # Número de nodos 81 x 81
Ny = 41
k  = 0.01 #0.001 # W/m.K
ht = 0.0001
Tmax = 200 # 3000


import h5py

#
# CREAR UN ARCHIVO HDF5
#
f = h5py.File('test_write_file.h5','w')

mesh = f.create_group('mesh')
inputs = f.create_group('inputs')
outputs = f.create_group('outputs')
vis = f.create_group('visualization')

mesh.attrs['NX'] = Nx
mesh.attrs['NY'] = Ny
mesh.attrs['WX'] = longitud_x
mesh.attrs['WY'] = longitud_y

inputs.attrs['k'] = k
inputs.attrs['dt'] = ht
inputs.attrs['Tmax'] = Tmax

mesh.attrs.create('DX',0.5, (1,))

f.close()
#
# AHORA LEE EL ARCHIVO CREADO ANTES
#
f = h5py.File('test_write_file.h5','r')

print(f)
for key in f.keys():
    print('-'*80)
    print(key, f[key], type(f[key]))
    print('-'*80)
    
    atributos = f[key].attrs
    for a in atributos:
        print(a, atributos[a], type(atributos[a]))
        
f.close()