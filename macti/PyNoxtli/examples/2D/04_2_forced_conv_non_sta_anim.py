#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on mié abr 15 17:25:46 CDT 2020].
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
from fvm.tAdvDiff import tAdvDiff2D
from fvm.pde import PDE
from utils.displayInfo import printInfo
import vis.flowix as flx
#
# Función que ejecuta FuncAnimation() en cada paso de tiempo
#
def solver(i, ax, dt):
    print(i,sep=' ', end = ' ')
    transport.solve()
#    ax.collections = []
    v.contourf(1, xv, yv, T, par_contour)
    v.quiver(1,xd,yd,uvel_v,vvel_v, {'scale':20})
    
par_contour = {'cmap':'cool', 'levels':20}
#
# Datos del problema
#
longitud_x = 1.0 # meters
longitud_y = 1.0
k  = 0.01 #0.001 # W/m.K
Nx = 41 # Número de nodos 81 x 81
Ny = 41
dt = 0.0001
Tmax = 400 # 3000
#
# Definición del dominio y condiciones de frontera
#
placa = Rectangle(longitud_x, longitud_y)
placa.boundaryConditions(dirichlet = {'LEFT':-0.0, 'RIGHT':0.0}, neumman ={'BOTTOM':0, 'TOP':0})
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
xv, yv, _ = malla.coordinatesMeshFVM()
xd, yd, _ = malla.coordinatesMeshFDM()
xg, yg = np.meshgrid(xv, yv, sparse=False)
xg_u, yg_u = np.meshgrid(xd,yv,sparse=True)
xg_v, yg_v = np.meshgrid(xv,yd,sparse=True)
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud_x = longitud_x,
          Longitud_y = longitud_y,
          Conductividad = k,
          Nodos = (nx,ny),
          Volúmenes = (nvx,nvy),
          Deltas = (dx,dy),
          Inner = (ivx, ivy))
#
# A vector field
#
A = 1.0
alpha = 2.0
uvel = -A * np.cos(np.pi * alpha * yg_u) * np.sin(np.pi * alpha * xg_u)
vvel =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_v)
uvel_v = -A * np.cos(np.pi * alpha * yg_v) * np.sin(np.pi * alpha * xg_u)
vvel_v =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_u)
#
# Initial concentration
#
T = np.zeros((nvx+2, nvy+2))
cx = 0.5
cy = 0.65
rsize1 = 0.30
rsize2 = 0.10
for i in range(T.shape[0]):
    for j in range(T.shape[1]):
        r = np.sqrt((xg[i,j]-cx)**2 +(yg[i,j]-cy)**2)
        if r < rsize1:
            T[i,j] = np.sin(0.5*np.pi*(1.0-r/rsize1))**2
        r = np.sqrt((xg[i,j]-(cx+.25))**2 +(yg[i,j]-(cy-0.25))**2)
        if r < rsize2:
            T[i,j] = 1*np.sin(0.5*np.pi*(1.0-r/rsize2))**2        
#
# Visualización usando VisCoFlow
#
axis_par = [{'aspect':'equal','xlabel':'x','ylabel':'y'}]
v = flx.Plotter(1,1,axis_par)
con_i = v.contourf(1,xv,yv,T, par_contour)
v.colorbar(1,con_i, {'shrink':0.25, 'orientation':'horizontal', 'ticks':[0, 0.25, 0.5]})
v.quiver(1,xd,yd,uvel_v,vvel_v, {'scale':20})
#
# Definimos la fuente 
#
Su = np.zeros((ivy, ivx))
#print('Su = ', Su)
#
# Definimos el esquema de disccretización
#
advdif_scheme = tAdvDiff2D(malla, Su, dt = dt, Gamma = k)
advdif_scheme.setVelocity(uvel,vvel)
#
# Definimos la ecuación a resolver
#
transport = PDE(placa, T)
#print(T)
#
# Creamos el sistema lineal y lo resolvemos
#
Su.shape = ivy * ivx
transport.setNumericalScheme(advdif_scheme)
#
# Resolvemos y graficamos para varios pasos de tiempo
#
from matplotlib.animation import FuncAnimation

anim = FuncAnimation(v.fig,    # La figura donde se hace la animación
                     solver,        # la función que resuelve y cambia los datos
                     fargs=(v.axes(1), dt, ),   # argumentos para la función solver()                     
                     interval=500,  # Intervalo entre cuadros en milisegundos
                     frames=Tmax+1, # Número de iteraciones (Cuadros)
                     repeat=False)  # Permite poner la animación en un ciclo 
#
# Graficación
#
v.show()

