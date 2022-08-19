#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 11:42:12 CST 2020].

Example 4.2 from Malalasekera Book
"""
#-----------------------------------------------------------
# PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
#import os, sys
#if not("/base" in sys.path[0][-5:]):
#    sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

import numpy as np
#
# Importar módulos de pynoxtli
#
from macti.PyNoxtli.geo.line import Line
from macti.PyNoxtli.fvm.sDiffusion import sDiffusion1D
from macti.PyNoxtli.fvm.pde import PDE
from macti.PyNoxtli.utils.displayInfo import printInfo
import macti.PyNoxtli.vis.flowix as flx
#
# Calcula la solución analítica
#
def analyticSol(x):
    return ((TB - TA) / longitud + q * (longitud - x) / (2 * k) ) * x + TA
#
# Datos del problema
#
longitud = 0.02 # meters
TA = 100  # °C 
TB = 200  # °C 
k  = 0.5  # W/m.K
q  = 1e+06 # 1e+06 W/m^3 = 1000 kW/m^3 Fuente uniforme
N  = 6 # Número de nodos
#
# Definición del dominio y condiciones de frontera
#
rod = Line(longitud)
rod.boundaryConditions(dirichlet = {'LEFT':TA, 'RIGHT':TB})
#
# Creamos la malla y obtenemos datos importantes
#
malla     = rod.constructMesh(N)
ivx, _, _ = malla.bounds(bi = 1, ei = N-1)
nx        = malla.nx    # Número de nodos
nvx       = malla.vx    # Número de volúmenes
delta     = malla.dx    # Tamaño de los volúmenes
#
# Se construye el arreglo donde se guardará la solución
#
T = np.zeros(nvx+2) # El arreglo contiene ceros
T[0]  = TA        # Condición de frontera izquierda
T[-1] = TB        # Condición de frontera derecha
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud = longitud,
          Temperatura_A = TA,
          Temperatura_B = TB,
          Conductividad = k,
          Nodos = nx, 
          Volúmenes = nvx,
          Delta = delta)
#
# Definimos la fuente 
#
S = np.zeros(ivx)
S[:] = q
#
# Definimos el esquema de disccretización
#
dif_scheme = sDiffusion1D(malla, S, Gamma = k)
#
# Definimos la ecuación a resolver
#
poisson = PDE(rod, T)
#
# Creamos el sistema lineal y lo resolvemos
#
poisson.setNumericalScheme(dif_scheme)
poisson.solve()
#
# Solución analítica
#
xa = np.linspace(0,longitud,100)
Ta = analyticSol(xa)
#
# Visualización
#
x, _, _ = malla.coordinatesMeshFVM()
axis_par = [{'title':'Numerica vs Exacta', 'xlabel':'x [cm]', 'ylabel':'T [$^o$C]'}]   
v = flx.Plotter(2,1,axis_par)
v.plot(1, x*100, T, {'marker':'o', 'ls':'-', 'label':'Numérica', 'zorder':5})
v.plot(1, xa*100, Ta, {'marker':'', 'ls':'-', 'c':'red', 'lw':3, 'label':'Exacta'})
v.plot_mesh(2, malla, label=True)
v.legend()
v.grid()
v.show()
