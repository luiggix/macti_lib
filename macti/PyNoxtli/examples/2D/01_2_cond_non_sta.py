#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on mié abr 15 16:31:23 CDT 2020].
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
from macti.PyNoxtli.fvm.tDiffusion import tDiffusion2D
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
dt = 0.01
Tmax = 50
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
axis_par = [{'aspect':'equal'}]   
v = flx.Plotter(1,2,axis_par)
v.plot_mesh(1, malla, vol='.', nod='.')

x, y, _ = malla.coordinatesMeshFVM()
#
# Se construye el arreglo donde se guardará la solución
#
T = np.zeros((nvy+2, nvx+2)) # El arreglo contiene ceros
T[-1,:] = TT      # Condición de frontera pared superior
T[0,:] = TB      # Condición de frontera pared inferior
T[:,0] = TL      # Condición de frontera pared izquierda
T[:,-1] = TR      # Condición de frontera pared derecha
#
# Definimos la fuente 
#
Su = np.zeros((ivy, ivx))
#
# Definimos el esquema de disccretización
#
dif_scheme = tDiffusion2D(malla, Su, dt = dt, Gamma = k)
#
# Definimos la ecuación a resolver
#
laplace = PDE(placa, T)
#
# Creamos el sistema lineal y lo resolvemos
#
Su.shape = ivy * ivx
laplace.setNumericalScheme(dif_scheme)
for k in range(0,Tmax):
    print('k = ', k)
    sol = laplace.solve()
#
# Graficación
#
con = v.contourf(2,x,y,T,{'cmap':'hot', 'levels':20})
v.colorbar(2, con)
v.show()

