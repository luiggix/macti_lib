# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:54:42 2019

@author: luiggi
"""
def get_all(name):
    print(name)
    
import h5py
f = h5py.File('test_dataset_Temperature.h5','r')

for key in f.keys():
    print('-'*80)
    print(key, f[key], type(f[key]))
    print('-'*80)
    
    atributos = f[key].attrs
    for a in atributos:
        print(a, atributos[a], type(atributos[a]))


print('-'*80)
f.visit(get_all)
print('-'*80)        

#malla = f['mesh']
#Nx = malla.attrs['NX']
#Ny = malla.attrs['NY']
#longitud_x = malla.attrs['WX']
#longitud_y = malla.attrs['WY']
#
#var = f['vars']
#ht = var.attrs['dt']
#k = var.attrs['k']
#Tmax = var.attrs['Tmax']
#
#print('-'*30)
#print(Nx, Ny, longitud_x, longitud_y)
#print('-'*30)
#print(k, ht, Tmax)
#print('-'*30)

datos = f['outputs']
print(datos, type(datos), datos['Temperature'], sep='\n')
T = datos['Temperature']
print(T[:])

dataset = datos['Temperature']
print("Dataset dataspace is", dataset.shape)
print("Dataset Numpy datatype is", dataset.dtype)
print("Dataset name is", dataset.name)
print("Dataset is a member of the group", dataset.parent)
print("Dataset was created in the file", dataset.file)

print('-'*80)


#
#import matplotlib.pyplot as plt
#
#plt.imshow(T)
#plt.show()

f.close()