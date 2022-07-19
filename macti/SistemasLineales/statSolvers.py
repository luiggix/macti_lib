#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 11:26:55 2018

@author: luiggi
"""
import numpy as np
import matplotlib.pyplot as plt

def jacobi(A,b,tol,kmax):
    N = len(b)
    xnew = np.zeros(N)
    xold = np.zeros(N)
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
#        print(k, error)
    return xnew, error, k, error_array


def gauss_seidel(A,b,tol,kmax):
    N = len(b)
    xnew = np.zeros(N)
    xold = np.zeros(N)
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
#        print(k, error)
    return xnew, error, k, error_array

def sor(A,b,tol,kmax,w):
    N = len(b)
    xnew = np.zeros(N)
    xold = np.zeros(N)
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
#        print(k, error)
    return xnew, error, k, error_array




if __name__ == '__main__':

    A = np.matrix([[3, 2],[2,6]] )
    b = np.array([2,-8])
    
    sol, e, it, ea = jacobi(A,b,1e-5,100)
    print('\n Jacobi \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))
    
    sol, e, it, ea = gauss_seidel(A,b,1e-5,100)
    print('\n Gauss-Seidel \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))
    
    sol, e, it, ea = sor(A,b,1e-5,100,0.5)
    print('\n SOR \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))

