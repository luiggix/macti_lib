#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 13:11:49 CST 2020].

Acoculco
----------------------------------


"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("pynoxtli/base" in sys.path[0][-13:]):
    sys.path.insert(0, os.path.abspath('../../../base'))
#-----------------------------------------------------------

import numpy as np
from scipy import interpolate
#
# Importar módulos de pynoxtli
#
from geo.line import Line
from acoculco1D import tDiffusion1D
from fvm.pde import PDE
from utils.displayInfo import printInfo
import vis.flowix as flx
#
# Datos del problema
#
longitud = 4000.0 # meters
N  = 101 # 101 Número de nodos
TA = 15 # °C 
TB = 750 # °C 
dt = 3600*24*365 # Paso de tiempo:  1 año [s]
Nspeedup = 100
dt *= Nspeedup
Tmax = int(250000 / Nspeedup) # Number of time steps.
#
# Definición del dominio y condiciones de frontera
#
reservoir = Line(longitud)
reservoir.boundaryConditions(dirichlet = {'RIGHT':TB, 'LEFT':TA})
#
# Creamos la malla y obtenemos datos importantes
#
malla     = reservoir.constructMesh(N)
ivx, _, _ = malla.bounds(bi = 1, ei = N-1)
nx        = malla.nx    # Número de nodos
nvx       = malla.vx    # Número de volúmenes
dx        = malla.dx    # Tamaño de los volúmenes
#
# Depth coordinates
#
z, _, _ = malla.coordinatesMeshFVM()
#
# Se construye el arreglo donde se guardará la solución
#
#T = np.zeros(nvx) # El arreglo contiene ceros
#T[0]  = TA        # Condición de frontera izquierda
#T[-1] = TB        # Condición de frontera derecha
#
# Temperaturas iniciales y finales a diferentes profundidades (Datos) e interpolación
#
z_ini = [0, 100, 200, 400, 710, 803, 1100, 1200, 1400, 1500, 1600, 1700, 1800, 2000, 2500, 3000, 3500, 4000]
T_ini = [15, 113, 145, 178, 155, 201, 215, 282, 223, 226, 252, 284, 310, 350, 450, 550, 650, 750]
T_ini_int = interpolate.splev(z, interpolate.splrep(z_ini, T_ini, s = 0), der = 0)
#
z_fin = [0, 96, 192, 389, 596, 798, 1000, 1197, 1408, 1495, 1586, 1649, 1702, 1750, 1803, 1851, 1904, 1942, 1967, 2000, 2500, 3000, 3500, 4000]
T_fin = [15, 69, 74, 95, 121, 159, 168, 192, 213, 213, 236, 251, 267, 272, 284, 288, 298, 293, 310, 325, 440, 550, 650, 750]
T_fin_int = interpolate.splev(z, interpolate.splrep(z_fin, T_fin, s = 0), der = 0)
#
# Preparamos la visualización con VisCoFlow
#
axis_par = [{'title':'Numérica', 'xlabel':'T [$^o$C]', 'ylabel':'depth [km]',
             'ylim':(4100.0,-100), 'xlim':(0,800)}]   
v = flx.Plotter(1,1,axis_par)
#v.plot(1,T_ini,z_ini, {'marker':'o', 'ls':'-','label':'Temp. inicial (datos)'})
v.plot(1,T_ini_int,z, {'marker':'', 'ls':'-', 'lw':2.5})

#v.plot(1,T_fin,z_fin, {'marker':'o', 'ls':'-','label':'Temp. final (datos)'})
v.plot(1,T_fin_int,z, {'marker':'', 'ls':'-', 'lw':2.5})
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud = longitud,
          Temperatura_A = TA,
          Temperatura_B = TB,
          Nodos = nx, 
          Volúmenes = nvx,
          dx = dx,
          dt = dt,
          Tmax = Tmax)
#
# Definimos la fuente 
#
Su = np.zeros(ivx)
#
# Definimos el esquema de disccretización
#
acoculco = tDiffusion1D(malla, Su, dt = dt)
acoculco.calcConductivity()
#acoculco.Gamma = 1.0e-7
#v.plot(1,acoculco.Gamma*5000,z, {'marker':'.','color':'b', 'ls':'-', 'lw':1})
print(len(acoculco.Gamma))

# Definimos la ecuación a resolver
#
T = np.copy(T_ini_int)
print(len(T_ini_int))
heat_transfer = PDE(reservoir, T)
#v.plot(1,T,z, {'marker':'.','color':'k', 'ls':'--', 'lw':1})

#
# Preparamos el sistema lineal y creamos la matriz
#
heat_transfer.setNumericalScheme(acoculco)
#
# Resolvemos para varios pasos de tiempo
#
print(Tmax)
#input('press enter')
for k in range(0,Tmax):
    heat_transfer.solve()
    if (k % 10) == 0:
        v.plot(1,T,z, {'marker':'', 'ls':'-', 'lw':0.5})

heat_transfer.printMat(nice=True)

##
## Visualización usando VisCoFlow
##
v.plot(1,T,z, {'marker':'','color':'k', 'ls':'-', 'lw':2, 'label':'Sol. Final'})
##v.plot_mesh(2, malla)
v.grid()
v.legend()
v.show()
