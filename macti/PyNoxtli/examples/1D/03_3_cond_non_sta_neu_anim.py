#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 12:40:11 CST 2020].

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
from macti.PyNoxtli.fvm.tDiffusion import tDiffusion1D
from macti.PyNoxtli.fvm.pde import PDE
from macti.PyNoxtli.utils.displayInfo import printInfo
import macti.PyNoxtli.vis.flowix as flx
#
# Calcula la solución analítica
#
def analyticSol(x,n):
    return (TA - Tambiente) * np.cosh(n * (longitud - x)) / np.cosh(n * longitud) + Tambiente
#
# Función que ejecuta FuncAnimation() en cada paso de tiempo
#
def solver(i, ax, dt):
    convective_heat.solve()
    line.set_ydata(T)
    
    time_step = i * dt
    title_graf = 'Sol. Numérica :  Step = {:>3d} Time = {:>6.5f}'.format(i, time_step)
    ax.set_title(title_graf)
#
# Datos del problema
#
longitud = 1.0 # metros
Tambiente = 20  # °C 
TA = 100  # °C 
n2 = 25 # /m^2
fluxB = 0 # Flujo igual a cero
N = 16 # Número de nodos
k = 1
q = 0
dt = 0.01 # Paso de tiempo
Tmax = 20 # Número de pasos en el tiempo
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
dif_scheme = tDiffusion1D(malla, Su, dt = dt, Gamma = k)
dif_scheme.Sp(-n2)
#
# Definimos la ecuación a resolver
#
convective_heat = PDE(rod, T)
#
# Creamos el sistema lineal y lo resolvemos
#
convective_heat.setNumericalScheme(dif_scheme)
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
xa = np.linspace(0,longitud,100)
Ta = analyticSol(xa, np.sqrt(n2))
#
# Preparamos la visualización con VisCoFlow
#
axis_par = [{'title':'Numerica vs Exacta', 'xlabel':'x [cm]', 'ylabel':'T [$^o$C]'}]   
v = flx.Plotter(2,1,axis_par)
line, = v.plot(1,x,T, {'marker':'o', 'ls':'-', 'lw':0.75, 'zorder':5})
#
# Resolvemos y graficamos para varios pasos de tiempo
#
from matplotlib.animation import FuncAnimation

anim = FuncAnimation(v.fig,    # La figura donde se hace la animación
                     solver,        # la función que resuelve y cambia los datos
                     fargs = (v.axes(1), dt,),
                     interval=500,  # Intervalo entre cuadros en milisegundos
                     frames=Tmax+1, # Número de iteraciones (Cuadros)
                     repeat=False)  # Permite poner la animación en un ciclo 

v.plot(1, xa, Ta, {'color':'r', 'ls':'-', 'lw':3, 'label':'Sol. Exacta'})
v.plot_mesh(2, malla, label=True)
v.legend()
v.grid()
v.show()

