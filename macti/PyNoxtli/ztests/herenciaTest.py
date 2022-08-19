# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 15:10:39 2019

@author: luiggi
"""

#import numpy as np

class LinearSystem():
    
    def __init__(self, b):
        self.__b = b
        print('LinearSystem.__b = ', b)
        
    def calc(self, i):
        print('LinearSystem.calc(%d)' % i)

class PDE():
    
    __LS = None
    
    def __init__(self, a, ls):
        self.__a = a
        LinearSystem.__LS = ls
        
        print('PDE.__a = ', a)
    
    def bc(self, v):
        print('PDE.bc(%d)' % v)
        
    def calc(self, i):
        print('PDE.calc(%d)' % i)
        LinearSystem.__LS.calc(i)

    @staticmethod
    def LS():
        return LinearSystem.__LS
       
class Diffusion(PDE):
    
    def __init__(self, a, ls, c):
        super().__init__(a, ls)
        self.__c = c
        self.__ls = ls
        print('Diffusion.__c = ', c)
        
    def calc (self, i):        
        print('Diffusion.calc(%d)' % i)
        ls = PDE.LS()
        ls.calc(i)

ls = LinearSystem(5)

df = Diffusion(1, ls, 2)
df.bc(4)
df.calc(3)

pde = PDE(8, ls)  
pde.bc(9)  
pde.calc(19)      