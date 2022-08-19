#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on mié abr 15 16:55:45 CDT 2020].
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

import numpy as np
#
# Importar módulos de pynoxtli
#
from geo.rectangle import Rectangle
from fvm.tDiffusion import tDiffusion2D
from fvm.pde import PDE
from utils.displayInfo import printInfo
import vis.flowix as flx
#
# Función que ejecuta FuncAnimation() en cada paso de tiempo
#
def solver(i, ax, dt):
    print(i,sep=' ', end = ' ')
    laplace.solve()
    v.contourf(1, x, y, T, par_contour)

    time_step = i * dt
    title_graf = 'Sol. Numérica. Tiempo = {:>6.5f}'.format(i, time_step)
    ax.set_title(title_graf)
    
par_contour = {'cmap':'hot', 'levels':20}
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
Tmax = 30
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
# Malla para graficar
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
#
# Visualización usando VisCoFlow
#
axis_par = [{'aspect':'equal'}]   
v = flx.Plotter(1,1,axis_par, par_fig={'figsize':(4,6)})
con = v.contourf(1,x,y,T,par_contour)
v.colorbar(1, con, {'shrink':0.75})
#
# Definimos la fuente 
#
Su = np.zeros((ivy, ivx))
#print('Su = ', Su)
#
# Definimos el esquema de disccretización
#
dif_scheme = tDiffusion2D(malla,Su, dt = dt, Gamma = k)
#
# Definimos la ecuación a resolver
#
laplace = PDE(placa, T)
#
# Creamos el sistema lineal y lo resolvemos
#
Su.shape = ivy * ivx
laplace.setNumericalScheme(dif_scheme)
#
# Resolvemos y graficamos para varios pasos de tiempo
#
from matplotlib.animation import FuncAnimation

anim = FuncAnimation(v.fig,         # La figura donde se hace la animación
                     solver,        # la función que resuelve y cambia los datos
                     fargs=(v.axes(1), dt, ),   # argumentos para la función solver()
                     interval=500,  # Intervalo entre cuadros en milisegundos
                     frames=Tmax+1, # Número de iteraciones (Cuadros)
                     repeat=False)  # Permite poner la animación en un ciclo 

#
# Graficación
#
v.show()

