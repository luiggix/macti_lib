# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este ejemplo muestra como se manejan las mallas y los campos escalares,
su forma de creación, su indexación y su graficación correcta.

"""

import numpy as np
import vis.VisCoFlow as vis
from utils.nicePrint import printData
from geo.Mesh import Mesh

axis_par = [{'aspect':'equal', 'xlabel':'x', 'ylabel':'y','title':'u[i:]=i'},
            {'aspect':'equal', 'xlabel':'x', 'ylabel':'y','title':'u[0,:]=100,u[-1,:] =-100'},
            {'aspect':'equal', 'xlabel':'x', 'ylabel':'y','title':'u[:,0]=100,u[:,-1] =-100'},
            {'aspect':'equal', 'xlabel':'x', 'ylabel':'y','title':'u = np.sin(xg * yg)'}]
visco = vis.Plotter(2,2,axis_par)

Lx = 2.0 
Ly = 1.0
Nx = 9
Ny = 5
#
# La malla se crea como sigue:
#                Nx = 9 nodos en la dirección x; 
#                Ny = 5 nodos en la dirección y
#
malla = Mesh(length_x = Lx, nodes_x = Nx, 
             length_y = Ly, nodes_y = Ny)

ivx, ivy, ivz = malla.bounds(bi = 1, ei = Nx-1,
                            bj = 1, ej = Ny-1)
#
# nx y ny son los nodos; vx y vy son los volúmenes; ivx y ivy son los volúmenes internos
#
printData(lx_ly = (malla.lx, malla.ly),
          nx_ny = (malla.nx, malla.ny),
          vx_vy = (malla.vx, malla.vy),
          ivx_ivy = (malla.ivx, malla.ivy))

############  
#
# x : arreglo con 9 elementos cuando se usa FDM; con 10 elementos cuando se usa FVM
# y : arreglo con 5 elementos cuando se usa FDM; con 6 elementos cuando se usa FVM
# DE LAS SIGUIENTES DOS LÍNEAS, COMENTE UNA Y DESCOMENTE LA OTRA.
#x, y, _ = malla.constructMeshFDM(); vol = ''; nod='X'
x, y, _ = malla.constructMeshFVM(); vol='.'; nod=''
#
# xg y yg : arreglos usados para crear otros arreglos con las dimensiones 
#           correctas de la malla en cuestión. Se usa sparse para ahorrar
#           memoria e indexing='xy' para generar arreglos con el siguiente
#           shape: xg = (1,9) y yg = (5,1)  ESTO PARA FDM
#                  xg = (1,10) y yg = (6,1) ESTO PARA FVM
# OJO: Por omisión se usa indexing = 'xy', de tal manera que no es necesario
# poner explícitamente esta opción.
#
xg, yg = np.meshgrid(x,y,sparse=True, indexing='xy')
#
# Lo siguiente crea el arreglo u con el shape (5,9), es decir 5 renglones para
# la dirección vertical y 9 columnas para la dirección horizontal, ESTO PARA FDM.
# PARA FVM se crea un arreglo de (6,10).
#
u = np.zeros((y.shape[0], x.shape[0]))
#
# Imprimimos los shapes de los arreglos para corroborar.
#
print('x ', x.shape, 'y ', y.shape, 
      'xg ', xg.shape, 'yg ', yg.shape, 
      'u ', u.shape, )
print(x)
print(y,'\n')
#
# Hacemos que todos los elementos de cada renglón de u tengan un mismo valor 
#
for i in range(u.shape[0]):
    u[i,:] = i
print(u, '\n')
visco.contourf(1,x,y,u)
visco.plot_mesh(1,malla, vol=vol, nod=nod)
#
# Hacemos que todos los elementos del primer renglón tengan un mismo valor
# (Pared inferior)
#
u[0,:] = 100
#
# Hacemos que todos los elementos del último renglón tengan un mismo valor
# (Pared superior)
#
u[-1:] = -100
print(u, '\n')
visco.contourf(2,x,y,u)
visco.plot_mesh(2,malla, vol=vol, nod=nod)
#
# Hacemos que todos los elementos de la primera columna tengan un mismo valor
# (Pared izquierda)
#
u[:, 0] = 100
#
# Hacemos que todos los elementos de la última columna tengan un mismo valor
# (Pared derecha)
#
u[:,-1] = -100
print(u, '\n')
visco.contourf(3,x,y,u)
visco.plot_mesh(3,malla, vol=vol, nod=nod)
#
# Usamos xg y yg para llenar u mediante alguna función.
#
u = np.sin(xg*yg)
print(u)

visco.contourf(4,x,y,u)
visco.plot_mesh(4,malla, vol=vol, nod=nod)

#############  

visco.show()