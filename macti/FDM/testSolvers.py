#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:58:12 2018

@author: luiggi
"""
#-----------------------------------------------------------
# Ruta biblioteca macti
#
#import os, sys
#sys.path.insert(0, os.path.abspath('../../'))
#print(sys.path)
#-----------------------------------------------------------

import numpy as np
import macti.SistemasLineales.statSolvers as sol
from macti.visual import plotGrid, plotMalla, plotContornos

import time
from colorama import Fore

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
mpl.rcParams['figure.titlesize'] = 12
mpl.rcParams['axes.labelsize'] = 12

def buildMatrix(Nx, Ny, diagonal):
    N = Nx * Ny
    A = np.zeros((N,N))

# Primero llena los bloques tridiagonales
    for j in range(0,Ny):
        ofs = Nx * j
        A[ofs, ofs] = diagonal; 
        A[ofs, ofs + 1] = 1
        for i in range(1,Nx-1):
            A[ofs + i, ofs + i]     = diagonal
            A[ofs + i, ofs + i + 1] = 1
            A[ofs + i, ofs + i - 1] = 1
        A[ofs + Nx - 1, ofs + Nx - 2] = 1; 
        A[ofs + Nx - 1, ofs + Nx - 1] = diagonal 

# Despues llena las dos diagonales externas
    for k in range(0,N-Nx):
        A[k, Nx + k] = 1
        A[Nx + k, k] = 1

    return A

def RHS(Nx, Ny, boundaries):
    f = np.zeros((Ny,Nx)) # RHS
# Aplicacion de las condiciones de frontera Dirichlet
    f[Ny-1,:] -= boundaries['RIGHT'] 
    f[0   ,:] -= boundaries['LEFT']    
    f[:,Nx-1] -= boundaries['TOP'] 
    f[:,0   ] -= boundaries['BOT']  
    f.shape = f.size     # Cambiamos los arreglos a formato unidimensional

    return f

def solucion(B,T,L,R, metodo, N):
    Lx = 1.0
    Ly = 1.0
    Nx = N
    Ny = N

    boundaries = {'BOT':B, 'TOP':T, 'LEFT':L, 'RIGHT':R}

    A = buildMatrix(Nx, Ny,-4) # Matriz del sistema
    b = RHS(Nx, Ny, boundaries)
    
    tol = 1e-6
    max_iter = 200
    w = 1.5

    t1 = time.perf_counter()
    
    if metodo == 'linalg.solve':
        ut = np.linalg.solve(A,b)
        error = 0.0
        it = 1
    elif metodo == 'Jacobi':
        ut,error,it, ea = sol.jacobi(A,b,tol,max_iter)
    elif metodo == 'Gauss-Seidel':
        ut,error,it, ea = sol.gauss_seidel(A,b,tol,max_iter)
    elif metodo == 'SOR':
        ut,error,it, ea = sol.sor(A,b,tol,max_iter,w)

    t2 = time.perf_counter()
    te = t2 - t1
    print(Fore.BLUE + "Método: {}\n".format(metodo) +
          Fore.RESET + " CPU: {:5.4f} [s] ".format(te) +
          Fore.MAGENTA + " Sistema : {}x{} = {}\n".format(N*N, N*N, (N * N)**2) +
          Fore.RED   + " Error : {:5.4e} ".format(error) + 
          Fore.GREEN + " Iter : {} ".format(it))

    u = np.zeros((Ny+2, Nx+2))
    u[Ny+1,:   ] = boundaries['RIGHT']
    u[0   ,:   ] = boundaries['LEFT']
    u[:   ,Nx+1] = boundaries['TOP']
    u[:   ,0   ] = boundaries['BOT'] 
    ut.shape = (Ny, Nx) # Regresamos el arreglo a formato bidimensional
    u[1:Ny+1,1:Nx+1] = ut
    
    titulo = 'Método: {} ][ Error = {:5.4f} | Iter = {} | CPU = {:5.4f} [s] ][ Sistema : {}]'.format(metodo, error, it, te, N * N)
#    plotSolution(u,Lx, Ly, Nx,Ny,titulo)

    x = np.linspace(0,Lx,Nx+2)
    y = np.linspace(0,Ly,Ny+2)
    xg, yg = np.meshgrid(x, y, indexing='ij', sparse=False)
    
    fig = plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plotMalla(xg, yg, 'Malla (incógnitas:{}x{})'.format(N,N))
    
    plt.subplot(1,2,2)
    plotContornos(xg, yg, u, 'Solución ({})'.format(metodo, ), 'box')
    
    plt.show()
    
if __name__ == '__main__':

    R = 7   # Derecha 
    L = 34  # Izquierda
    T = 0   # Arriba
    B = 100 # Abajo
    
    N = 3 
    m = 'Jacobi'
    solucion(B,T,L,R,m,N)
