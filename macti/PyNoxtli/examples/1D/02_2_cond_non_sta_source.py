#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 12:04:25 CST 2020].

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
from macti.PyNoxtli.fvm.tDiffusion import tDiffusion1D
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
dt = 0.00001 # Paso de tiempo
Tmax = 40 # Número de pasos en el tiempo
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
T = np.ones(nvx+2) # El arreglo contiene unos
T *= TA          # Inicializamos T = TA
T[0]  = TA       # Condición de frontera izquierda
T[-1] = TB       # Condición de frontera derecha
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
Su = np.zeros(ivx)
Su[:] = q
#
# Definimos el esquema de disccretización
#
dif_scheme = tDiffusion1D(malla, Su, dt = dt, Gamma = k)
#
# Definimos la ecuación a resolver
#
poisson = PDE(rod, T)
#
# Preparamos el sistema lineal y creamos la matriz
#
poisson.setNumericalScheme(dif_scheme)
#
# Preparamos la visualización con VisCoFlow
#
axis_par = [{'title':'Numerica vs Exacta', 'xlabel':'x [cm]', 'ylabel':'T [$^o$C]'}]   
v = flx.Plotter(2,1,axis_par)
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
xa = np.linspace(0,longitud,100)
Ta = analyticSol(xa)
#
# Resolvemos para varios pasos de tiempo
#
v.plot(1,x * 100,T, {'marker':'o', 'ls':'-', 'lw':0.5})
for k in range(0,Tmax):
    print('k = ', k)
    poisson.solve()
    v.plot(1,x * 100,T, {'marker':'o', 'ls':'-', 'lw':0.5, 'zorder':5, 'alpha':0.5})
#
# Visualización
#
v.plot(1,xa * 100,Ta, {'color':'r', 'ls':'-', 'lw':3, 'label':'Sol. Exacta'})
v.plot_mesh(2, malla, label=True)
v.legend()
v.grid()
v.show()
