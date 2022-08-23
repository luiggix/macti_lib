#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 16:06:16 CST 2020].
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
#import os, sys
#if not("/base" in sys.path[0][-5:]):
#    sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

import numpy as np
#
# Importar módulos de pynoxtli
#
from macti.PyNoxtli.geo.rectangle import Rectangle
from macti.PyNoxtli.fvm.sDiffusion import sDiffusion2D
from macti.PyNoxtli.fvm.pde import PDE
from macti.PyNoxtli.utils.displayInfo import printInfo
import macti.PyNoxtli.vis.flowix as flx
#
# Datos del problema
#
longitud_x = 1.0 # meters
longitud_y = 2.0
TL = 0 # °C 
TR = 0 # °C
TB = 0 # °C
TT = 1 # °C
k  = 1 # W/m.K
Nx = 11 # Número de nodos
Ny = 21
#
# Definición del dominio y condiciones de frontera
#
placa = Rectangle(longitud_x, longitud_y)
placa.boundaryConditions(dirichlet = {'LEFT':TL, 'RIGHT':TR, 'BOTTOM':TB, 'TOP':TT})
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
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud_x = longitud_x,
          Longitud_y = longitud_y,
          TL_TR_TT_TB = (TL, TR, TT, TB),
          Conductividad = k,
          Nodos = (nx,ny),
          Volúmenes = (nvx,nvy),
          Deltas = (dx,dy),
          Inner = (ivx, ivy))
#
# Visualización usando VisCoFlow
#
axis_par = [{'aspect':'equal'},
            {'aspect':'equal'}]  
#
# Visualización de la malla
#
v1 = flx.Plotter(1,2,axis_par)
v1.plot_mesh(1, malla, vol='.', nod='|')
#
x, y, _ = malla.coordinatesMeshFVM()
#
# Se construye el arreglo donde se guardará la solución
#
T = np.zeros((nvy+2, nvx+2)) # El arreglo contiene ceros
T[-1,:] = TT      # Condición de frontera pared superior
T[0,:] = TB      # Condición de frontera pared inferior
T[:,0] = TL      # Condición de frontera pared izquierda
T[:,-1] = TR      # Condición de frontera pared derecha

#v.contourf(2,x,y,T,{'cmap':'inferno'})
#v.scatter(2,xg,yg)
#print(T)
#
# Definimos la fuente 
#
Su = np.zeros((ivy, ivx))
#print('Su = ', Su)
#
# Definimos el esquema de disccretización
#
dif_scheme = sDiffusion2D(malla, Su, Gamma = k)
#
# Definimos la ecuación a resolver
#
laplace = PDE(placa, T)
#
# Creamos el sistema lineal y lo resolvemos
#
Su.shape = (ivy * ivx)
laplace.setNumericalScheme(dif_scheme)
sol = laplace.solve()
#print(sol)
#
# Graficación de contornos
#
#v2 = flx.Plotter(1,1,axis_par)
con = v1.contourf(2,x,y,T,{'levels':20, 'cmap':'hot'})
v1.contour(2,x,y,T,{'levels':20, 'colors':'k', 'linewidths':0.5})
v1.colorbar(2, con, {'shrink':0.75})
#
# Graficación de Temperatura vs posición
#
axis_par2 = [{'xlabel':'$x$ [m]', 'ylabel':'$T [^o C]$', 'ylim':(0,1),
              'title':'Corte en $y$=0.5'},
            {'xlabel':'$y [m]$', 'ylabel':'', 'ylim':(0,1),
             'title':'Corte en $x$=0.5'}]             
#             ]   
v2 = flx.Plotter(1,2,axis_par2)
v2.plot(1, x, T[int(ny/2),:], {'ls':'-','marker':'.'})
v2.plot(2, y, T[:,int(nx/2)], {'ls':'-','marker':'.'})

v1.show()

