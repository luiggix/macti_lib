#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on jue abr  2 13:13:45 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("pynoxtli/base" in sys.path[0][-13:]):
    sys.path.insert(0, os.path.abspath('../../../base'))
#-----------------------------------------------------------

import numpy as np
from fvm.numScheme import NumericalScheme

class tDiffusion1D(NumericalScheme):
    
    def __init__(self, mesh, Su, dt = 1.0, Gamma = 1.0, rho = 1.0):
        super().__init__(mesh, Su, dt = dt)
        self.__Sp    = 0
        self.__rho   = rho        
#        self.__Gamma = Gamma
        self.__z, _, _ = mesh.coordinatesMeshFVM()
        self.__vx = mesh.vx

    def calcConductivity(self):
        z = self.__z
        vx = self.__vx
        self.__Gamma = np.zeros((vx+2))
#        ht = self.__ht
#        hx2 = self.__hx * self.__hx

### k     - Thermal conductivity (W/m-K), 
### cp    - specific heat capacity (J/kg-K), 
### rho   - mass density (kg/m^3), 
### Gamma - thermal diffusivity (m^2/s)
### 0 to 100 m:
        k_1 = 1.84; cp_1 = 840.0; rho_1 = 2120.0; Gamma_1 = k_1/(rho_1*cp_1);
### 100 to 330 m:
        k_2 = 1.41; cp_2 = 840.0; rho_2 = 2340.0; Gamma_2 = k_2/(rho_2*cp_2);
### 330 to 500 m:
        k_3 = 1.36; cp_3 = 840.0; rho_3 = 2300.0; Gamma_3 = k_3/(rho_3*cp_3); 
### 500 to 600 m:
        k_4 = 1.44; cp_4 = 840.0; rho_4 = 2300.0; Gamma_4 = k_4/(rho_4*cp_4); 
### 600 to 850 m:
        k_5 = 1.46; cp_5 = 840.0; rho_5 = 2290.0; Gamma_5 = k_5/(rho_5*cp_5); 
### 850 to 1000 m:
        k_6 = 1.68; cp_6 = 840.0; rho_6 = 2700.0; Gamma_6 = k_6/(rho_6*cp_6); 
### 1000 to 1520 m:
        k_7 = 1.84; cp_7 = 890.0; rho_7 = 2700.0; Gamma_7 = k_7/(rho_7*cp_7); 
### 1520 to 1820 m:
        k_8 = 1.66; cp_8 = 890.0; rho_8 = 2360.0; Gamma_8 = k_8/(rho_8*cp_8); 
### > 1820 m :
        k_9 = 2.1; cp_9 = 950.0; rho_9 = 2760.0; Gamma_9 = k_9/(rho_9*cp_9); 

### Vector of lumped temperature independent material properties to be used 
### to solve the heat balance equation at different depths over time.
        for k in range(0, vx):
            if (z[k] <= 50.0):
                self.__Gamma[k] = Gamma_1 * 1.0
            elif ((z[k] > 50.0) and (z[k] <= 250.0)):
                self.__Gamma[k] = Gamma_2 * 1.0
            elif ((z[k] > 250.0) and (z[k] <= 400.0)):
                self.__Gamma[k] = Gamma_3 * 1.0
            elif ((z[k] > 400.0) and (z[k] <= 600.0)):
                self.__Gamma[k] = Gamma_4 * 1.0
            elif ((z[k] > 600.0) and (z[k] <= 800.0)):
                self.__Gamma[k] = Gamma_5 * 1.0
            elif ((z[k] > 800.0) and (z[k] <= 1000.0)):
                self.__Gamma[k] = Gamma_6 * 1.0
            elif ((z[k] > 1000.0) and (z[k] <= 1500.0)):
                self.__Gamma[k] = Gamma_7 * 1.0
            elif ((z[k] > 1500.0) and (z[k] <= 1900.0)):
                self.__Gamma[k] = Gamma_8 * 1.0
            else:
                self.__Gamma[k] = Gamma_9 * 1.0

#        self.__Gamma *= 1.0 * ht / hx2
#        self.__Gamma[:] = Gamma_9 * ht / hx2
#        print(Gamma)
#        print('\n z',z.shape)
#        print(z)
       
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
        self.__Sp = Sp * self.__dx

    def source(self, phi):
        return self.Su * self.dx + phi[1:-1] * self.dx / self.dt
    
    def calc(self, i):
#        print('Diff calc', i)
        dt = self.dt
        dx = self.dx
        Gamma_w = 0.5 * (self.__Gamma[i] + self.__Gamma[i-1])
        Gamma_e = 0.5 * (self.__Gamma[i] + self.__Gamma[i+1])
        dE = Gamma_e / dx
        dW = Gamma_w / dx
 #       dE = Gamma_e
 #       dW = Gamma_w
        dP = dE + dW + dx / dt
        return np.array((-dW, dP, -dE))
        
if __name__ == '__main__':
        
    from geo.line import Line
#
# Create a domain with its mesh
#    
    N = 101
    rod = Line(4000)
    malla = rod.constructMesh(N)
    ivx, _, _ = malla.bounds(bi = 1, ei = N-1)    
#    malla.coordinatesMeshFVM()
#
# Scalar field for the solution
#
    T = np.zeros(malla.vx+2)
    T[0] = 15
    T[-1] = 750
#
# Definitions of boundary conditions
#
    rod.boundaryConditions({'RIGHT':'D', 'LEFT':'D'})
#
# Create an scheme
#
    dt = 3600*24*365
    Su = np.zeros(ivx)
    laplace = tDiffusion1D(malla, Su, dt = dt)    
    laplace.calcConductivity()
    print('GAMMA : \n', laplace.Gamma)
   