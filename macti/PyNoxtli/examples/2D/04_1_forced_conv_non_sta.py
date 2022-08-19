#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on mié abr 15 17:20:31 CDT 2020].
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

import numpy as np
import h5py

#
# Importar módulos de pynoxtli
#
from geo.rectangle import Rectangle
from fvm.tAdvDiff import tAdvDiff2D
from fvm.pde import PDE
from utils.displayInfo import printInfo
import vis.flowix as flx
#
# Lee datos del problema de un archivo HDF5
#
# Las siguientes dos lineas son para evitar repeticion en la escritura
from shutil import copyfile
copyfile('test_write_file.h5','input_example10.h5')
#
file = h5py.File('input_example10.h5','r+')

mesh = file['mesh']
longitud_x = mesh.attrs['WX']
longitud_y = mesh.attrs['WY']
Nx = mesh.attrs['NX']
Ny = mesh.attrs['NY'] 

inputs = file['inputs']
dt = inputs.attrs['dt']
k = inputs.attrs['k']
Tmax = inputs.attrs['Tmax']

#
# Definición del dominio y condiciones de frontera
#
placa = Rectangle(longitud_x, longitud_y)
placa.boundaryConditions(dirichlet = {'LEFT':-0.0, 'RIGHT':0.0}, 
                         neumman ={'BOTTOM':0, 'TOP':0})
#
# Creamos la malla y obtenemos datos importantes
#
malla     = placa.constructMesh(Nx, Ny)
ivx, ivy, _ = malla.bounds(bi = 1, ei = Nx-1,
                           bj = 1, ej = Ny-1)
nx  = malla.nx    # Número de nodos
ny  = malla.ny    # Número de nodos
nvx = malla.vx    # Número de volúmenes
nvy = malla.vy    # Número de volúmenes
dx  = malla.dx    # Tamaño de los volúmenes
dy  = malla.dy    # Tamaño de los volúmenes
xv, yv, _ = malla.coordinatesMeshFVM()
xd, yd, _ = malla.coordinatesMeshFDM()
xg, yg = np.meshgrid(xv, yv, sparse=False)
xg_u, yg_u = np.meshgrid(xd,yv,sparse=True)
xg_v, yg_v = np.meshgrid(xv,yd,sparse=True)
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud_x = longitud_x,
          Longitud_y = longitud_y,
          Conductividad = k,
          Nodos = (nx,ny),
          Volúmenes = (nvx,nvy),
          Deltas = (dx,dy),
          Inner = (ivx, ivy))
#
# A vector field
#
A = 1.0
alpha = 2.0
uvel = -A * np.cos(np.pi * alpha * yg_u) * np.sin(np.pi * alpha * xg_u)
vvel =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_v)
uvel_v = -A * np.cos(np.pi * alpha * yg_v) * np.sin(np.pi * alpha * xg_u)
vvel_v =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_u)
#
# Initial concentration
#
T = np.zeros((nvx+2, nvy+2))
cx = 0.5
cy = 0.65
rsize1 = 0.30
rsize2 = 0.10
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        r = np.sqrt((xg[i,j]-cx)**2 +(yg[i,j]-cy)**2)
        if r < rsize1:
            T[i,j] = np.sin(0.5*np.pi*(1.0-r/rsize1))**2
        r = np.sqrt((xg[i,j]-(cx+.25))**2 +(yg[i,j]-(cy-0.25))**2)
        if r < rsize2:
            T[i,j] = 1*np.sin(0.5*np.pi*(1.0-r/rsize2))**2        
#
# Definimos la fuente 
#
Su = np.zeros((ivy, ivx))
#
# Definimos el esquema de disccretización
#
advdif_scheme = tAdvDiff2D(malla, Su, dt = dt, Gamma = k)
advdif_scheme.setVelocity(uvel,vvel)
#
# Definimos la ecuación a resolver
#
transport = PDE(placa, T)
#
# Creamos el sistema lineal y lo resolvemos
#
Su.shape = ivy * ivx
transport.setNumericalScheme(advdif_scheme)
#
# Visualización usando VisCoFlow
#
axis_par = [{'aspect':'equal','xlabel':'x','ylabel':'y','title':'Contaminante inicial'},
            {'aspect':'equal','xlabel':'x','ylabel':'y','title':'Transporte final'}]
v = flx.Plotter(1,2,axis_par)
par_contour = {'cmap':'cool', 'levels':20}
v.contourf(1,xv,yv,T, par_contour)
#
# Abrimos el grupo de salidas del archivo HDF5 para almacenar los resultados
#
outputs = file['outputs']
#
# Comenzamos la simulación
#
for k in range(0,Tmax):
    print('k = ', k, end=' ')
    sol = transport.solve(sym=False)
    name_dataset = 'Temperature ' + str(k).zfill(3) # fill zeros the number
    outputs.create_dataset(name_dataset, data=T)
    
#outputs.create_dataset('Temperature', data=T)
file.close()

con = v.contourf(2,xv,yv,T, par_contour)
v.colorbar(2,con, {'shrink':0.75, 'orientation':'horizontal', 'ticks':[0, 0.25, 0.5]})
v.quiver(1,xd,yd,uvel_v,vvel_v, {'scale':20})
v.colorbar(1,con, {'shrink':0.75, 'orientation':'horizontal', 'ticks':[0, 0.25, 0.5]})
v.show()

