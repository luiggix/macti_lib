#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 11:24:37 2019

@author: luiggi
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

from inout.hdf5_tools import HDF5_info
from geo.mesh import uMesh
import vis.flowix as vis
import numpy as np

def animacion(i):
    print(i,sep=' ', end = ' ')    
#    ax.collections = []
    v.contourf(1, x, y, T[:,:,i], par_contour)
#    v.quiver(1,xd,yd,uvel_v,vvel_v)

par_contour = {'cmap':'cool', 'levels':20}

archivo = 'input_example10.h5'
h5_info = HDF5_info(archivo, verb=True)
f = h5_info.file()


malla = uMesh(nodes_x = f['mesh'].attrs['NX'], 
             length_x = f['mesh'].attrs['WX'], 
             nodes_y = f['mesh'].attrs['NY'],
             length_y = f['mesh'].attrs['WY'])

x, y, _ = malla.constructMeshFVM()    
axis_par = [{'aspect':'equal','title':'Malla', 'xlabel':'x', 'ylabel':'y'},
            {'aspect':'equal','title':h5_info.datasets_names[0], 'xlabel':'x', 'ylabel':'y'}]   
v = vis.Plotter(1,1,axis_par)
ax = v.getAxis(1)

#v.plot_mesh(1, malla, vol='', nod='')
Tmax = f['inputs'].attrs['Tmax']
print(Tmax)

T = np.zeros((malla.vx, malla.vy,Tmax))
for i in range(Tmax):
    T[:,:,i] = h5_info.datasets[i]
    
#con = v.contourf(1,x,y, T[:,:,0],par_contour)
#v.contour(1,x,y,T,{'levels':10})
#    v.colorbar(2, con)    
    
from matplotlib.animation import FuncAnimation

#for i in range(Tmax):
#    animacion(i)
    
anim = FuncAnimation(v.getFig(),    # La figura donde se hace la animación
                     animacion,        # la función que resuelve y cambia los datos
                     interval=500,  # Intervalo entre cuadros en milisegundos
                     frames=Tmax, # Número de iteraciones (Cuadros)
                     repeat=False)  # Permite poner la animación en un ciclo 

v.show()

h5_info.close()
