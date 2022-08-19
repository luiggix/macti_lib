#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:57:25 2020

@author: luiggi
"""

import numpy as np

def imprime(x, N, Nd):
    for n in range(N):
        print()
        for I in range(Nd):
            idx = n * Nd + I
            print(x[idx], end = ' ')
        
Nd = 5
NTx = 4
NTy = 3
N = NTx * NTy
Nz = Nd * N
x = np.ones(Nz)

imprime(x, N, Nd)

print()
OFFSET_X = Nd * NTx
for j in range(NTy):
    I = j * OFFSET_X
    x[I+1] = 0 # aW
    I += OFFSET_X
    x[I-2] = 0 # aE

OFFSET_Y = (NTx * (NTy - 1) + 1) * Nd
for i in range(NTx):
    I = i * Nd
    x[I] = 0 # aS
    I += OFFSET_Y
    x[I-1] = 0 # aN
    
imprime(x, N, Nd)


Su = np.ones((NTy, NTx))

print()

count = 0
for j in range(NTy):
    for i in range(NTx):
        Su[j,i] = count
        count += 1
print(Su)

Su.shape = NTy *  NTx
print(Su)