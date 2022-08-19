#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on mié abr 15 17:09:37 CDT 2020].
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
from fvm.sAdvDiff import sAdvDiff2D
from fvm.pde import PDE
from utils.displayInfo import printInfo
import vis.flowix as flx
#
# Datos del problema
#
longitud_x = 1.0 # meters
longitud_y = 1.0
k  = 1.0 #0.001 # W/m.K
Nx = 9 # Número de nodos 81 x 81
Ny = 9
#dt = 0.0001
#Tmax = 100 # 3000
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
xvol, yvol, _ = malla.coordinatesMeshFVM()
xnod, ynod, _ = malla.coordinatesMeshFDM()
xnod_u, yvol_u = np.meshgrid(xnod, yvol, sparse='True')
xvol_v, ynod_v = np.meshgrid(xvol, ynod, sparse='True')

print('xvol =', xvol.shape)
print('yvol =', yvol.shape)
print('xnod =', xnod.shape)
print('ynod =', ynod.shape)

print('xnod_u =', xnod_u.shape)
print('yvol_u =', yvol_u.shape)
print('xvol_v =', xvol_v.shape)
print('ynod_v =', ynod_v.shape)

from geo.mesh.umesh import uMesh as Mesh
malla_u = Mesh(nx = nx, lx = longitud_x, ny = nvy, ly = longitud_y)
malla_v = Mesh(nx = nvx, lx = longitud_x, ny = ny, ly = longitud_y)

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
axis_par = [{'aspect':'equal','title':'Vel vols'},
            {'aspect':'equal', 'title':'Vel nods'}]
v = flx.Plotter(1,2,axis_par)
v.plot_mesh(1,malla, label=False)
v.scatter(2, xnod_u, xnod_u, {'marker':'|'})
v.scatter(2, yvol_u, yvol_u, {'marker':'.'}, )
v.scatter(2, xvol_v, xvol_v, {'marker':'v'})
v.scatter(2, ynod_v, ynod_v, {'marker':'^'}, )
v.legend()
#
# A vector field
#
A = 1.0
alpha = 1.0
uvel = -A * np.cos(np.pi * alpha * yvol_u) * np.sin(np.pi * alpha * xnod_u)
vvel =  A * np.sin(np.pi * alpha * ynod_v) * np.cos(np.pi * alpha * xvol_v)


#uvel_v = -A * np.cos(np.pi * alpha * yg_v) * np.sin(np.pi * alpha * xg_u)
#vvel_v =  A * np.sin(np.pi * alpha * yg_v) * np.cos(np.pi * alpha * xg_u)

print('uvel =', uvel.shape)
print('vvel =', vvel.shape)

# print('uvel_v =', uvel_v.shape)
# print('vvel_v =', vvel_v.shape)
#
# Visualización usando VisCoFlow
#
# axis_par = [{'aspect':'equal','title':'Vel nodos'},
#             {'aspect':'equal', 'title':'Vel vols'}]
# v = flx.Plotter(1,2,axis_par)
# #vel_norm = np.sqrt(uvel_v**2 + vvel_v**2)
# #con_i = v.contourf(2,xd,yd,vel_norm, {'levels':50,'cmap':'Blues'})
# v.quiver(1,xd,yd,uvel_v,vvel_v, {'scale':10})
# v.quiver(2,xd,yd,uvel_v,vvel_v, {'scale':10})

# #uvel = -A * np.ones(yg_u) * np.ones(xg_u)
# #vvel =  A * np.ones(yg_u) * np.ones(xg_u)
# #uvel_v = -A * np.ones(yg_u) * np.ones(xg_u)
# #vvel_v =  A * np.ones(yg_u) * np.ones(xg_u)

# #
# # Initial concentration
# #
# T = np.zeros((nvx+2, nvy+2))
# T[:, 0] = -0.5
# T[:,-1] = 0.5
# #
# # Visualización usando VisCoFlow
# #
# axis_par = [{'aspect':'equal','title':'Temperatura'},
#             {'aspect':'equal', 'title':'Velocidad'}]
# v = flx.Plotter(1,2,axis_par)
# vel_norm = np.sqrt(uvel_v**2 + vvel_v**2)
# con_i = v.contourf(2,xd,yd,vel_norm, {'levels':50,'cmap':'Blues'})
# v.quiver(2,xd,yd,uvel_v,vvel_v, {'scale':10})
# #
# # Definimos la fuente 
# #
# Su = np.zeros((ivy, ivx))
# #print('Su = ', Su)
# #
# # Definimos el esquema de disccretización
# #
# advdif_scheme = sAdvDiff2D(malla, Su, Gamma = k)
# advdif_scheme.setVelocity(uvel,vvel)
# #
# # Definimos la ecuación a resolver
# #
# transport = PDE(placa, T)
# #print(T)
# #
# # Creamos el sistema lineal y lo resolvemos
# #
# Su.shape = ivy * ivx
# transport.setNumericalScheme(advdif_scheme)
# transport.solve(sym=False)
# #
# # Graficación
# #
# con_f = v.contourf(1,xv,yv,T,{'levels':20, 'cmap':'inferno'})
# v.colorbar(1,con_f)
v.show()

