#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 12:53:13 CST 2020].

"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
#import os, sys
#if not("pynoxtli/base" in sys.path[0][-13:]):
#    sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

import numpy as np
from scipy import special

#
# Importar módulos de pynoxtli
#
from macti.PyNoxtli.geo.line import Line
from macti.PyNoxtli.fvm.tAdvDiff import tAdvDiff1D
from macti.PyNoxtli.fvm.pde import PDE
from macti.PyNoxtli.utils.displayInfo import printInfo
import macti.PyNoxtli.vis.flowix as flx
#
# Solución analítica
#
def analyticSol(x, u, t, Gamma):
 	divisor = 2 * np.sqrt(Gamma * t)
 	sol = 0.5 * (special.erfc((x - u * t)/ divisor) + 
 		np.exp(u * x) * np.exp(-Gamma) * special.erfc((x + u * t)/divisor))
 	return sol
 
# Datos del problema
#
L = 2.5 # m
rho = 1.0 # kg/m^3
u = 1.0 # m/s
Gamma = 0.001 # kg / m.s
phi0 = 1 #
phiL = 0 #
N = 200 # Número de nodos
dt = 0.002 # Paso de tiempo
Tmax = 1.0
Nmax = int(Tmax / dt)
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
ad_scheme = tAdvDiff1D(malla, Su, dt = dt, Gamma = Gamma, rho = rho)
vel = np.zeros(nvx+2)
vel.fill(u)
print(vel)
ad_scheme.setVelocity(vel)
#
# Definimos la ecuación a resolver
#
adv_diff = PDE(linea, phi)
#
# Creamos el sistema lineal y lo resolvemos
#
adv_diff.setNumericalScheme(ad_scheme)
#
# Preparamos la visualización con VisCoFlow
#
title_graf = '$\dfrac{\partial \phi}{\partial t} +  \dfrac{\partial (u \phi)}{\partial x}= \kappa \dfrac{\partial^2 \phi}{\partial x^2}$'
axis_par = [{'title':title_graf, 'xlabel':'$x$ [m]', 'ylabel':'$\phi$', 'ylim':(-0.1,1.1)}]   
v = flx.Plotter(1,1,axis_par)
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
xa = np.linspace(0,L,100)
exac = analyticSol(xa, u, Tmax, Gamma)
#
# Resolvemos para varios pasos de tiempo
#
v.plot(1,x,phi, {'color':'gray', 'ls':'--', 'lw':1.0})
for k in range(0,Nmax):
    print('k = ', k)
    adv_diff.solve(sym=False)
    if (k%100 == 0):
        v.plot(1,x,phi, {'color':'gray', 'ls':'--', 'lw':1.5})
#
# Visualización usando VisCoFlow
#
v.plot(1,x,phi, {'color':'C0', 'ls':'-', 'lw':1.5, 'label':'Numérica', 'zorder':5})      
v.plot(1,xa,exac, {'color':'red', 'ls':'-', 'lw':2.0, 'label':'Exacta'})
v.grid()
v.legend()
v.show()
