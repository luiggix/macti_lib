#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on jue abr  2 11:10:28 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../')) 
#-----------------------------------------------------------

import numpy as np
from macti.PyNoxtli.fvm.numScheme import NumericalScheme

class tDiffusion1D(NumericalScheme):
    
    def __init__(self, mesh, Su, dt = 1.0, Gamma = 1.0, rho = 1.0):
        super().__init__(mesh, Su, dt = dt)
        self.__Sp    = 0
        self.__rho   = rho        
        self.__Gamma = Gamma
        
    @property
    def Gamma(self):
        return self.__Gamma
    
    @Gamma.setter
    def Gamma(self, gamma):
        self.__Gamma = gamma

    @property
    def rho(self):
        return self.__rho
    
    @rho.setter
    def rho(self, rho):
        self.__rho = rho
        
    def Sp(self, Sp):
        self.__Sp = Sp * self.dx
       
    def source(self, phi):
        return self.Su * self.dx + phi[1:-1] * self.dx / self.dt
    
    def calc(self, i):
        dE = self.__Gamma / self.dx
        dW = self.__Gamma / self.dx
        dP = dE + dW - self.__Sp + self.__rho * self.dx / self.dt
        return np.array([-dW, dP, -dE])

class tDiffusion2D(NumericalScheme):
    
    def __init__(self, mesh, Su, dt = 1.0, Gamma = 1.0, rho = 1.0):
        super().__init__(mesh, Su, dt = dt)
        self.__Sp    = 0
        self.__rho   = rho        
        self.__Gamma = Gamma
        self.__ivx = mesh.ivx
        self.__ivy = mesh.ivy
        
    @property
    def Gamma(self):
        return self.__Gamma
    
    @Gamma.setter
    def Gamma(self, gamma):
        self.__Gamma = gamma

    @property
    def rho(self):
        return self.__rho
    
    @rho.setter
    def rho(self, rho):
        self.__rho = rho
        
    def Sp(self, Sp):
        self.__Sp = Sp * self.dx * self.dy

    def source(self, phi):
        self.Su.shape = self.__ivx * self.__ivy
        phi = np.copy(phi[1:-1,1:-1])
        phi.shape = self.__ivx * self.__ivy
        return self.Su * self.dx * self.dy + phi * self.dx * self.dy / self.dt
        
    def calc(self, i, j):
        dE = self.__Gamma * self.dy / self.dx
        dW = self.__Gamma * self.dy / self.dx
        dN = self.__Gamma * self.dx / self.dy
        dS = self.__Gamma * self.dx / self.dy  
        dP = dE + dW + dN + dS - self.__Sp + self.__rho * self.dx * self.dy / self.dt
        
        return np.array([-dS, -dW, dP, -dE, -dN])

#----------------------- TEST OF THE MODULE ----------------------------------       
if __name__ == '__main__':

    from utils.displayInfo import printInfo        
    from geo.line import Line 
    from geo.rectangle import Rectangle
    
    N = 6

    rod = Line(1.0)
    dt = 0.1
    malla = rod.constructMesh(N)
    ivx, _, _ = malla.bounds(bi = 1, ei = N-1)
    su = np.ones(ivx)
    laplace = tDiffusion1D(malla, su, Gamma = 3.4, dt = dt)    
    u = np.ones(malla.vx+2)
    printInfo(Descr = 'Testing tDiffusion1D', 
              dx = laplace.dx, 
              vx = malla.vx,
              ivx = malla.ivx,
              dt = laplace.dt)    
    print(laplace.calc(3))
    print(laplace.source(u))

    cuadro = Rectangle(1,1)
    malla2 = cuadro.constructMesh(N,N)
    ivx, ivy, _ = malla2.bounds(bi = 1, ei = N-1,bj = 1, ej = N-1)
    su = np.ones((ivy, ivx))
    laplace2 = tDiffusion2D(malla2, su, Gamma=5, dt = dt) 
    u = np.ones((malla2.vy+2, malla2.vx+2))
    printInfo(Descr = 'Testing Diffusion2D', 
              dx = laplace2.dx, 
              dy = laplace2.dy,
              vx = malla2.vx,
              vy = malla2.vy,
              ivx_ivy = (malla2.ivx, malla2.ivy),
              dt = laplace2.dt)    
    print(laplace2.calc(3,4))
    print(laplace2.source(u))  
#----------------------- TEST OF THE MODULE ----------------------------------
   