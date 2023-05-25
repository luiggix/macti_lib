#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 17:15:18 2018

@author: luiggi
"""

import numpy as np

def steepestDescent(A,b,x0,tol,kmax): 
    r = b.T - A @ x0
    k = 0
    res = np.linalg.norm(r)
    res_array = np.zeros(kmax)
#    print(k, res)
    while(res > tol and k < kmax):
        alpha = float(r.T @ r) / float(r.T @ A @ r)
        x0 = x0 + alpha * r
        r = b.T - A @ x0
        res = np.linalg.norm(r)
        res_array[k] = res
        k += 1
#        print(k, res)
    return x0, res, k, res_array

def conjugateGradient(A,b,x0,tol,kmax):
    r = b.T - A @ x0
    d = r
    rk_norm = r.T @ r
    res = np.linalg.norm(rk_norm)
    res_array = np.zeros(kmax)
    k = 0
#    print(k, res)
    while(res > tol and k < kmax):
        alpha = float(rk_norm) / float(d.T @ A @ d)
        x0 = x0 + alpha * d
#        r = b - A * x
        r = r - alpha * A @ d
        res = np.linalg.norm(r)
        res_array[k] = res
        rk_old = rk_norm
        rk_norm = r.T @ r
        beta = float(rk_norm) / float(rk_old)
        d = r + beta * d
        k += 1
#        print(k, res)
    return x0, res, k, res_array

    
if __name__ == '__main__':

    tol = 1e-6
    max_iter = 100
    A = np.matrix([[3, 2],[2,6]] )
    b = np.matrix([[2],[-8]])
    x0 = np.matrix([[-2],[-2]])
    
    sol, res, it, ra = steepestDescent(A,b,x0,tol,max_iter)
    print('\n Steepest Descent \n Solucion: {} \n Residual : {} \n Iteraciones : {}'.format(sol.flatten(), res, it))

    x0 = np.matrix([[-2],[-2]])
    sol, res, it, ra = conjugateGradient(A,b,x0,tol,max_iter)
    print('\n Conjugate Gradient \n Solucion: {} \n Residual : {} \n Iteraciones : {}'.format(sol.flatten(), res, it))
    