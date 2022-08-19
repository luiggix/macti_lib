#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:23:18 2020

@author: luiggi
"""

class Mesh():
    
    def __init__(self, nx, nvx):
        self.__nx = nx
        self.nvx = nvx
        
        # print(type(self.__nx))
        # print(id(self.__nx))

        # print(type(self.nvx))
        # print(id(self.nvx))
        
    @property
    def nx(self):
        print('funcion getter nx()')
        return self.__nx
    
    @nx.setter
    def nx(self, val):
        print('funcion setter nx()')
        self.__nx = val

    def printNx(self):
        print(id(self.__nx))

    def printNvx(self):
        print(id(self.nvx))
        
malla = Mesh(5, 10)

print('+' + '-' * 30)

print(type(malla.nx))
print(id(malla.nx))

print('+' + '-' * 30)

nodos = malla.nx

for i in range(10):
    a = nodos * 30 + 50
    print(id(nodos))

print('+' + '-' * 30)

for i in range(10):
    a = malla.nx * 30 + 50
    print(id(malla.nx))
    
print('+' + '-' * 30)

for i in range(10):
    malla.nx = nodos * 30 +50
    print(malla.nx, nodos, id(malla.nx), id(nodos))

malla.printNx()

print('+' + '-' * 30)

print(type(malla.nvx))
print(id(malla.nvx))

print('+' + '-' * 30)

nodos = malla.nvx

for i in range(10):
    a = nodos * 30 + 50
    print(id(nodos))

print('+' + '-' * 30)

for i in range(10):
    a = malla.nvx * 30 + 50
    print(id(malla.nvx))
    
print('+' + '-' * 30)

for i in range(10):
    malla.nvx = nodos * 30 +50
    print(malla.nvx, nodos, id(malla.nvx), id(nodos))

malla.printNvx()

print(malla.nvx, nodos)