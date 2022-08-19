#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 12:43:50 CST 2020].

Example 5.1 from Malalasekera Book
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
from macti.PyNoxtli.fvm.sAdvDiff import sAdvDiff1D
from macti.PyNoxtli.fvm.pde import PDE
from macti.PyNoxtli.utils.displayInfo import printInfo
import macti.PyNoxtli.vis.flowix as flx
#
# Solución analítica
#
def analyticSol(x):
    return (np.exp(rho * u * x / Gamma) - 1) / (np.exp(rho * u * L / Gamma) - 1) * (phiL - phi0) + phi0
#
# Datos del problema
#
L = 1.0 # m
rho = 1.0 # kg/m^3
u = 0.25 # m/s
Gamma = 0.1 # kg / m.s
phi0 = 1 #
phiL = 0 #
N = 5 # Número de nodos
#
# Definición del dominio y condiciones de frontera
#
linea = Line(L)
linea.boundaryConditions(dirichlet = {'LEFT':phi0, 'RIGHT':phiL})
#
# Creamos la malla y obtenemos datos importantes
#
malla     = linea.constructMesh(N)
ivx, _, _ = malla.bounds(bi = 1, ei = N-1)
nx        = malla.nx    # Número de nodos
nvx       = malla.vx    # Número de volúmenes
delta     = malla.dx    # Tamaño de los volúmenes
#
# Se construye el arreglo donde se guardará la solución
#
phi = np.zeros(nvx+2) # El arreglo contiene ceros
phi[0]  = phi0        # Condición de frontera izquierda
phi[-1] = phiL        # Condición de frontera derecha
#
# Imprimimos los datos del problema (nicely)
#
printInfo(Longitud = L,
          phi_A = phi0,
          phi_B = phiL,
          Gamma = Gamma,
          rho = rho,
          Nodos = nx, 
          Volúmenes = nvx,
          Delta = delta,
          ivx = ivx)
#
# Definimos la fuente 
#
Su = np.zeros(ivx)
#
# Definimos el esquema de disccretización
#
dif_scheme = sAdvDiff1D(malla, Su, Gamma, rho)
vel = np.zeros(nvx+2)
vel.fill(u)
dif_scheme.setVelocity(vel)
#
# Definimos la ecuación a resolver
#
adv_diff = PDE(linea, phi)
#
# Creamos el sistema lineal y lo resolvemos
#
adv_diff.setNumericalScheme(dif_scheme)
adv_diff.solve(sym=False)
print(phi)
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
xa = np.linspace(0,L,50)
phi_a = analyticSol(xa)
#
# Visualización usando VisCoFlow
#
title_graf = '$\dfrac{\partial (u \phi)}{\partial x}= \kappa \dfrac{\partial^2 \phi}{\partial x^2}$'
axis_par = [{'title':title_graf, 'xlabel':'x [m]', 'ylabel':'$\phi$'},
            {'title':'Malla', 'xlabel':'x [m]', 'ylabel':'$\phi$'},]   
v = flx.Plotter(2,1,axis_par)
v.plot(1,x,phi, {'marker':'o', 'ls':'-', 'label':'Numérica', 'zorder':5})
v.plot(1,xa,phi_a, {'marker':'', 'ls':'-', 'lw':3, 'color':'red', 'label':'Exacta'})
v.plot_mesh(2, malla, label=True)
v.legend([1,2], par={'loc':'lower left', 'ncol':2})
v.grid()
v.show()
