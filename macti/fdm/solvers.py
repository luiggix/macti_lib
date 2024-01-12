#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:26:55 2018
Updated on Fri Jan 12 08:32:59 PM UTC 2024
@author: luiggi
"""
import numpy as np
import matplotlib.pyplot as plt

def jacobi(A,b,x,tol,kmax):
    """
    Calcula la solución de un sistema de ecuaciones lineales usando
    el método de Jacobi. La solución inicial es x0 = np.zeros(N).

    Parameters
    ----------
    A : ndarray
    Matriz del sistema (en formato denso).

    b : ndarray
    Vector del lado derecho del sistema.

    x : ndarray
    Solución inicial.
    
    tol: float
    Tolerancia

    kmax: int
    Número de iteraciones máximas.

    Returns
    -------
    xnew : Solución final.
    error : Error final.
    k : Número de iteraciones realizadas.
    error_array : Arreglo con los residuos en cada iteración.
    """
    N = len(b)
    xnew = np.zeros(N)
    xold = x
    error = 10
    error_array = np.zeros(kmax)
    k = 0
    while(error > tol and k < kmax) :
        for i in range(0,N): 
            xnew[i] = 0
            for j in range(0,i):
                xnew[i] += A[i,j] * xold[j]
            for j in range(i+1,N):
                xnew[i] += A[i,j] * xold[j]                
            xnew[i] = (b[i] - xnew[i]) / A[i,i]
        error = np.linalg.norm(xnew-xold)
        error_array[k] = error
        k += 1
        xold[:] = xnew[:]
    return xnew, error, k, error_array

def gauss_seidel(A,b,x,tol,kmax):
    """
    Calcula la solución de un sistema de ecuaciones lineales usando
    el método de Gauss-Seidel. La solución inicial es x0 = np.zeros(N).

    Parameters
    ----------
    A : ndarray
    Matriz del sistema (en formato denso).

    b : ndarray
    Vector del lado derecho del sistema.

    x : ndarray
    Solución inicial.
    
    tol: float
    Tolerancia

    kmax: int
    Número de iteraciones máximas.

    Returns
    -------
    xnew : Solución final.
    error : Error final.
    k : Número de iteraciones realizadas.
    error_array : Arreglo con los residuos en cada iteración.
    """
    N = len(b)
    xnew = np.zeros(N)
    xold = x
    error = 10
    error_array = np.zeros(kmax)
    k = 0
    while(error > tol and k < kmax) :
        for i in range(0,N): # se puede hacer en paralelo
            xnew[i] = 0
            for j in range(0,i):
                xnew[i] += A[i,j] * xnew[j]
            for j in range(i+1,N):
                xnew[i] += A[i,j] * xold[j]                
            xnew[i] = (b[i] - xnew[i]) / A[i,i]
        error = np.linalg.norm(xnew-xold)
        error_array[k] = error
        k += 1
        xold[:] = xnew[:]
    return xnew, error, k, error_array

def sor(A,b,x,tol,kmax,w):
    """
    Calcula la solución de un sistema de ecuaciones lineales usando
    el método de sobre relajaciones sucesivas (SOR). La solución 
    inicial es x0 = np.zeros(N).

    Parameters
    ----------
    A : ndarray
    Matriz del sistema (en formato denso).

    b : ndarray
    Vector del lado derecho del sistema.
    
    x : ndarray
    Solución inicial.
    
    tol: float
    Tolerancia

    kmax: int
    Número de iteraciones máximas.

    Returns
    -------
    xnew : Solución final.
    error : Error final.
    k : Número de iteraciones realizadas.
    error_array : Arreglo con los residuos en cada iteración.
    """
    N = len(b)
    xnew = np.zeros(N)
    xold = x
    error = 10
    error_array = np.zeros(kmax)
    k = 0
    while(error > tol and k < kmax) :
        for i in range(0,N): # se puede hacer en paralelo
            sigma = 0
            for j in range(0,i):
                sigma += A[i,j] * xnew[j]
            for j in range(i+1,N):
                sigma += A[i,j] * xold[j]                
            sigma = (b[i] - sigma) / A[i,i]
            xnew[i] = xold[i] + w * (sigma -xold[i])
        error = np.linalg.norm(xnew-xold)
        error_array[k] = error
        k += 1
        xold[:] = xnew[:]
    return xnew, error, k, error_array

def steepest(A, b, x, tol, kmax):
    """
    Calcula la solución de un sistema de ecuaciones lineales usando
    el método de descenso del gradiente.

    Parameters
    ----------
    A : ndarray
    Matriz del sistema (en formato denso).

    b : ndarray
    Vector del lado derecho del sistema.

    x : ndarray
    Solución inicial.

    tol: float
    Tolerancia

    kmax: int
    Número de iteraciones máximas.

    Returns
    -------
    x : Solución final.
    res : Residuo final.
    k : Número de iteraciones realizadas.
    res_list : Arreglo con los residuos en cada iteración.
    """        
    r = b.T - A @ x
    res = np.linalg.norm(r, 2)
    res_list = []
    k = 0
    while(res > tol and k < kmax):
        alpha = r.T @ r / (r.T @ A @ r)
        x = x + r * alpha
        r = b.T - A @ x
        
        # Residuo
        res = np.linalg.norm(r, 2)
        res_list.append(res)
        
        k += 1

    return x, res, k, res_list        

def conjugateGradient(A, b, x, tol,kmax):
    """
    Calcula la solución de un sistema de ecuaciones lineales usando
    el método de gradiente conjugado.

    Parameters
    ----------
    A : ndarray
    Matriz del sistema (en formato denso).

    b : ndarray
    Vector del lado derecho del sistema.

    x : ndarray
    Solución inicial.

    tol: float
    Tolerancia

    kmax: int
    Número de iteraciones máximas.

    Returns
    -------
    x : Solución final.
    res : Residuo final.
    k : Número de iteraciones realizadas.
    res_list : Arreglo con los residuos en cada iteración.
    """
    r = b.T - A @ x
    d = r
    rk_norm = r.T @ r
    res = np.linalg.norm(rk_norm)
    res_list = []

    k = 0
    while(res > tol and k < kmax):
        alpha = float(rk_norm) / float(d.T @ A @ d)
        x = x + alpha * d
        r = r - alpha * A @ d
        
        # Residuo
        res = np.linalg.norm(r, 2)
        res_list.append(res)
        
        rk_old = rk_norm
        rk_norm = r.T @ r
        beta = float(rk_norm) / float(rk_old)
        d = r + beta * d
        k += 1
    return x, res, k, res_list        
    
if __name__ == '__main__':

    A = np.array([[3, 2],[2,6]] )
    b = np.array([2,-8])
    x0 = np.array([-2., 2.])
    tol = 1e-5
    kmax = 100
    w = 1.09
    
    sol, e, it, ea = jacobi(A, b, x0, tol, kmax)
    print('\n Jacobi \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))

    x0 = np.array([-2., 2.])    
    sol, e, it, ea = gauss_seidel(A, b, x0, tol, kmax)
    print('\n Gauss-Seidel \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))

    x0 = np.array([-2., 2.])
    sol, e, it, ea = sor(A, b, x0, tol, kmax, w)
    print('\n SOR \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))
    
    # Método Steepest descend
    x0 = np.array([-2., 2.])
    solGrad, rGrad, itGrad, rlistGrad  = steepest(A, b, x0, tol, kmax)
    print('\n SteepestDescent \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(solGrad, rGrad, itGrad))

    # Método CGM
    x0 = np.array([-2., 2.])
    solCGM, rCGM, itCGM, rlistCGM = conjugateGradient(A, b, x0, tol, kmax)
    print('\n CGM \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(solCGM, rCGM, itCGM))

