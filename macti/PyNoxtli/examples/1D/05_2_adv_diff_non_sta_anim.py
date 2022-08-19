#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 13:02:56 CST 2020].

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
# Función que ejecuta FuncAnimation() en cada paso de tiempo
#
def solver(i, ax, dt,title_graf):
    adv_diff.solve(sym=False)
    line.set_ydata(phi)
    
    time_step = i * dt
    title_graf += ': Step = {:>3d} Time = {:>6.5f}'.format(i, time_step)
    ax.set_title(title_graf)
#
# Solución analítica
#
def analyticSol(x, u, t, Gamma):
    print(t,Gamma)
    divisor = 2 * np.sqrt(Gamma * t)
    sol = 0.5 * (special.erfc((x - u * t)/ divisor) + \
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
dt = 0.01 # Paso de tiempo
Tmax = 1
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
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
xa = np.linspace(0,L,100)
exac = analyticSol(xa, u, Tmax, Gamma)
#
# Preparamos la visualización con VisCoFlow
#
title_graf = '$\dfrac{\partial \phi}{\partial t} +  \dfrac{\partial (u \phi)}{\partial x}= \kappa \dfrac{\partial^2 \phi}{\partial x^2}$'
title_inicial = title_graf + ': Step = {:>3d} Time = {:>6.5f}'.format(0,0)
axis_par = [{'title':title_inicial, 'xlabel':'$x$ [m]', 'ylabel':'$\phi$'}]   
v = flx.Plotter(1,1,axis_par)
line, = v.plot(1,x,phi, {'color':'C0', 'ls':'--', 'lw':1.5, 'zorder':5, 'label':'Numérica'})
#
# Resolvemos y graficamos para varios pasos de tiempo
#
from matplotlib.animation import FuncAnimation

anim = FuncAnimation(v.fig,    # La figura donde se hace la animación
                     solver,        # la función que resuelve y cambia los datos
                     fargs =(v.axes(1), dt, title_graf),
                     interval=500,  # Intervalo entre cuadros en milisegundos
                     frames=Nmax+1, # Número de iteraciones (Cuadros)
                     repeat=False)  # Permite poner la animación en un ciclo 

v.plot(1,xa,exac, {'color':'red', 'ls':'-', 'lw':3, 'label':'Exacta'})        
v.grid()
v.legend()
v.show()
