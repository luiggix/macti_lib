#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on mié abr 15 17:15:56 CDT 2020].
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("pynoxtli/base" in sys.path[0][-13:]):
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
    v.contourf(4, xv, yv, T, par_contour)
#    v.contour(4,xv,yv,T,{'levels':10, 'linewidths':0.5,'colors':'k'})

    
par_contour = {'cmap':'inferno', 'levels':50}
#
# Datos del problema
#
longitud_x = 1.0 # meters
longitud_y = 1.0
k  = 1.0 #0.001 # W/m.K
Nx = 21 # Número de nodos 81 x 81
Ny = 21
dt = 0.0001
Tmax = 100 # 3000
#
# Definición del dominio y condiciones de frontera
#
placa = Rectangle(longitud_x, longitud_y)
placa.boundaryConditions(dirichlet = {'LEFT':-0.5, 'RIGHT':0.5}, 
                         neumman ={'BOTTOM':0, 'TOP':0})
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
xg_u, yg_u = np.meshgrid(xd,yv,sparse='True')
xg_v, yg_v = np.meshgrid(xv,yd,sparse='True')
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
A = 4.0
alpha = 1.0
uvel = -A * np.cos(np.pi * alpha * yg_u) * np.sin(np.pi * alpha * xg_u)
vvel =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_v)
uvel_v = -A * np.cos(np.pi * alpha * yg_v) * np.sin(np.pi * alpha * xg_u)
vvel_v =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_u)
#
# Initial concentration
#
T = np.zeros((nvx+2, nvy+2))
T[:, 0] = -0.5
T[:,-1] = 0.5
#
# Visualización usando VisCoFlow
#
axis_par = [{'aspect':'equal', 'title':'$x$-vel',
             'xlabel':'','ylabel':'y', 'xticks':[]}, 
            {'aspect':'equal', 'title':'$y$-vel',
             'xlabel':'','ylabel':'', 'xticks':[], 'yticks':[]},
            {'aspect':'equal', 'title':'Velocidad',
             'xlabel':'x','ylabel':'y'},
            {'aspect':'equal', 'title':'Temperatura',
             'xlabel':'x','ylabel':'', 'yticks':[]}]
v = flx.Plotter(2,2,axis_par)
con_f = v.contourf(4,xv,yv,T,{'levels':20, 'cmap':'inferno'})
#v.contour(4,xv,yv,T,{'levels':10, 'linewidths':0.5, 'colors':'k'})

v.contourf(1,xd,yv,uvel, {'levels':20,'cmap':'Purples'})
v.contourf(2,xv,yd,vvel, {'levels':20,'cmap':'Greens'})
vel_norm = np.sqrt(uvel_v**2 + vvel_v**2)
con_i = v.contourf(3,xd,yd,vel_norm, {'levels':50,'cmap':'Blues'})
v.quiver(3,xd,yd,uvel_v,vvel_v, {'scale':20})
#
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
                     fargs=(v.axes(4), dt, ),   # argumentos para la función solver()                     
                     interval=500,  # Intervalo entre cuadros en milisegundos
                     frames=Tmax+1, # Número de iteraciones (Cuadros)
                     repeat=False)  # Permite poner la animación en un ciclo 
#
# Graficación
#
v.show()

