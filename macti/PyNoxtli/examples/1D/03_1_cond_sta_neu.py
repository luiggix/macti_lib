#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 12:32:46 CST 2020].

Example 4.3 from Malalasekera Book
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
def analyticSol(x,n):
    return (TA - Tambiente) * np.cosh(n * (longitud - x)) / np.cosh(n * longitud) + Tambiente
#
# Datos del problema
#
longitud = 1.0 # metros
Tambiente = 20  # °C 
TA = 100  # °C 
n2 = 25 # /m^2
fluxB = 0 # Flujo igual a cero
N = 6 # Número de nodos
k = 1
q = 0
#
# Definición del dominio y condiciones de frontera
#
rod = Line(longitud)
rod.boundaryConditions(dirichlet = {'LEFT':TA}, neumman ={'RIGHT':fluxB})
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
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud = longitud,
          Temperatura_A = TA,
          Flujo_B = fluxB,
          n2 = n2,
          Nodos = nx, 
          Volúmenes = nvx,
          Delta = delta)
#
# Definimos la fuente 
#
Su = np.zeros(ivx)
Su[:] = n2 * Tambiente
#
# Definimos el esquema de disccretización
#
dif_scheme = sDiffusion1D(malla, Su, Gamma = k)
dif_scheme.Sp(-n2)
#
# Definimos la ecuación a resolver
#
convective_heat = PDE(rod, T)
#
# Creamos el sistema lineal y lo resolvemos
#
convective_heat.setNumericalScheme(dif_scheme)
convective_heat.solve()
#
# Corregimos el valor en la condicion Neumman
#
#convective_heat.updateNeumman()
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
xa = np.linspace(0,longitud,100)
Ta = analyticSol(xa, np.sqrt(n2))
#
# Visualización usando VisCoFlow
#
axis_par = [{'title':'Numerica vs Exacta', 'xlabel':'x [cm]', 'ylabel':'T [$^o$C]'}]   
v = flx.Plotter(2,1,axis_par)
v.plot(1, x, T, {'marker':'o', 'ls':'-', 'label':'Numérica', 'zorder':5})
v.plot(1, xa, Ta, {'marker':'', 'ls':'-', 'lw':3, 'c':'red', 'label':'Exacta'})
v.plot_mesh(2, malla, label=True)
v.legend()
v.grid()
v.show()

