#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on mié abr  1 18:58:39 CST 2020].
"""

#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../')) 
#-----------------------------------------------------------

class NumericalScheme():
    
    def __init__(self, mesh, Su, dt=1.0):
        self.dx = mesh.dx
        self.dy = mesh.dy
        self.dz = mesh.dz
        self.dt = dt
        self.Su = Su
            
#    @property
#    def Su(self):
#        return self.__Su
#
#    @Su.setter    
#    def Su(self, Su):
#        self.__Su = Su

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from utils.displayInfo import printInfo
    from geo.line import Line
    import numpy as np
    rod = Line(0.5)
    malla = rod.constructMesh(5)
    ivx,_,_ = malla.bounds(bi = 1, ei = 4)   

    su = np.ones(ivx)
    u = np.ones(malla.vx)
    
    ns = NumericalScheme(malla, su, dt = 4.4)
#    ns = NumericalScheme(dx = 1.0, dy = 2.3, dz = 3.4, dt 0.9)
    
    printInfo(Descripcion = 'Prueba de NumericalScheme()',
              dx = ns.dx,
              dy = ns.dy,
              dz = ns.dz,
              dt = ns.dt)

    class nsTest(NumericalScheme):
        
        def __init__(self, mesh, Su, gamma=1.0):
            super().__init__(mesh, Su)
            self.__Gamma = gamma  
          
        def calc(self, i):
            print('i:',i,'dx = ', self.dx)
    
    ns_test = nsTest(malla, su)
    
    printInfo(Descripcion = 'Prueba de nsTest()',
              dx = ns_test.dx,
              dy = ns_test.dy,
              dz = ns_test.dz,
              vx = malla.vx,
              dt = ns_test.dt)
    
    ns_test.calc(21)
    
    ns_test.Su = su
    print(ns_test.Su)
    su[2] = 90
    print(ns_test.Su)
    
    class nsTest2(NumericalScheme):
        
        def __init__(self, mesh, Su, gamma=1.0, dt=1.0):
            super().__init__(mesh, dt)
            self.__Gamma = gamma  
        
        def calcSource(self, su):
            self.__Su = su * self.dx
            
        def calc(self, i):
            print('i:',i,'hx = ', self.dx)
            print('i:',i,'ht = ', self.dt)
            print('i:',i,'Gamma = ', self.__Gamma)
    
    ns_test2 = nsTest2(malla, Su = su, dt = 0.89, gamma = 35)
    
    printInfo(Descripcion = 'Prueba de nsTest2()',
              dx = ns_test2.dx,
              dy = ns_test2.dy,
              dz = ns_test2.dz,
              dt = ns_test2.dt)
    
    ns_test2.calc(22)    
#----------------------- TEST OF THE MODULE ----------------------------------   

    