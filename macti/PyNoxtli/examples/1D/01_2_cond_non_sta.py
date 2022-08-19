#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 11:08:06 CST 2020].

Ejemplo 4.1 de (Versteeg & Malalasekera, 2007) 

Referencia:
@book{versteeg2007introduction,
  title={An Introduction to Computational Fluid Dynamics: The Finite Volume Method},
  author={Versteeg, H.K. and Malalasekera, W.},
  isbn={9780131274983},
  lccn={95006736},
  url={https://books.google.com.mx/books?id=RvBZ-UMpGzIC},
  year={2007},
  publisher={Pearson Education Limited}

}
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
# Datos del problema
#
longitud = 0.5 # metros
TA = 100       # °C 
TB = 500       # °C 
k  = 1000      # W/m.K
N  = 6         # Número de nodos
dt = 0.00001   # Paso de tiempo
Tmax = 20      # Número de pasos en el tiempo
#
# Definición del dominio y condiciones de frontera
#
barra = Line(longitud)
barra.boundaryConditions(dirichlet = {'RIGHT':TB, 'LEFT':TA})
#
# Creamos la malla y obtenemos datos importantes
#
malla     = barra.constructMesh(N) # Se construye el objeto para la malla
ivx, _, _ = malla.bounds(bi = 1, ei = N-1) # Grados de libertad
nx        = malla.nx    # Número de nodos
nvx       = malla.vx    # Número de volúmenes
delta     = malla.dx    # Tamaño de los volúmenes
#
# Se construye el arreglo donde se guardará la solución
#
T = np.zeros(nvx+2) # Condición inicial T = 0
T[0]  = TA          # Condición de frontera izquierda
T[-1] = TB          # Condición de frontera derecha
#
# Imprimimos los datos del problema
#
printInfo(Longitud = longitud,
          Temperatura_A = TA,
          Temperatura_B = TB,
          Conductividad = k,
          Nodos = nx, 
          Volúmenes = nvx,
          Delta = delta,
          dt = dt)
#
# Definimos la fuente 
#
S = np.zeros(ivx)   # Por ahora no hay fuente.
#
# Definimos el esquema de disccretización
#
dif_scheme = tDiffusion1D(malla, S, Gamma = k, dt = dt)
#
# Definimos la ecuación a resolver
#
laplace = PDE(barra, T)
#
# Preparamos el sistema lineal y creamos la matriz
#
laplace.setNumericalScheme(dif_scheme)
#
# Preparamos la visualización con VisCoFlow
#
axis_par = [{'title':'Solución Numérica', 'xlabel':'x [cm]', 'ylabel':'T [$^o$C]'}]   
v = flx.Plotter(2,1,axis_par)
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
Ta = 800 * x + 100
#
# Resolvemos para varios pasos de tiempo
#
v.plot(1,x * 100,T, {'marker':'o', 'ls':'-', 'lw':3, 'color':'k', 'label':'Cond. inicial'})
print('Iteraciones :', end = ' ')
for n in range(0,Tmax):
    print(n, end = ' ')
    laplace.solve()
    v.plot(1,x * 100,T, {'marker':'o', 'ls':'-', 'lw':0.5, 'zorder':5, 'alpha':0.5})
#
# Visualización
#
v.plot(1,x * 100,Ta, {'color':'r', 'ls':'-', 'lw':3, 'label':'Sol. Final'})
v.plot_mesh(2, malla, label=True)
v.grid()
v.legend(par={'ncol':2})
v.show()
