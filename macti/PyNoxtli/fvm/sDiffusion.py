#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on jue abr  2 09:31:01 CST 2020]
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

class sDiffusion1D(NumericalScheme):
    r"""
    Discretización del término de difusión de una EDP en 1D.
    
    Attributes
    ----------
    __Gamma : float
        Coeficiente de difusión.
        
    Notes
    -----
    Usando el método de FVM, se discretiza el término de difusión en 1D:
        
        .. math:: \frac{d}{d x} \left(\Gamma \frac{d u}{d x} )
    """
    
    def __init__(self, mesh, Su, Gamma = 1.0):
        super().__init__(mesh, Su)
        self.__Sp = 0            
        self.__Gamma = Gamma
        
    @property
    def Gamma(self):
        r"""Regresa el valor de :math:`\Gamma`."""
        return self.__Gamma
    
    @Gamma.setter
    def Gamma(self, gamma):
        self.__Gamma = gamma
    
    def Sp(self, Sp):
        """Por definir."""
        self.__Sp = Sp * self.dx
    
    def source(self, phi):
        """Calcula el término fuente."""
        return self.Su * self.dx # You need to create a new array!! the mult create the new array
    
    def calc(self, i):
        r"""
        Definición del esquema numérico.

        Parameters
        ----------
        i : int
            Índice de la malla donde se hará el cálculo de los coeficientes.

        Returns
        -------
        np.array
            Regresa los coeficientes :math: `a_w(i), a_P(i), a_E(i)` 

        """
        dE = self.__Gamma / self.dx
        dW = self.__Gamma / self.dx
        dP = dE + dW - self.__Sp

        return np.array([-dW, dP, -dE])

class sDiffusion2D(NumericalScheme):
    r"""
    Discretización del término de difusión de una EDP en 2D.
    
    Attributes
    ----------
    __Gamma : float
        Coeficiente de difusión.
        
    Notes
    -----
    Usando el método de FVM, se discretiza el término de difusión en 2D:
        
        .. math:: 
            \frac{d}{d x} \left(\Gamma \frac{d u}{d x} ) +
            \frac{d}{d y} \left(\Gamma \frac{d u}{d y} ) +        
    """
    
    def __init__(self, mesh, Su, Gamma = 1.0):
        super().__init__(mesh, Su)
        self.__Sp = 0            
        self.__Gamma = Gamma
        
    @property
    def Gamma(self):
        r"""Regresa el valor de :math:`\Gamma`."""
        return self.__Gamma
    
    @Gamma.setter
    def Gamma(self, gamma):
        self.__Gamma = gamma
    
    def Sp(self, Sp):
        """Por definir."""
        self.__Sp = Sp * self.dx * self.dy
    
    def source(self, phi):
        """Calcula el término fuente."""
        return self.Su * self.dx * self.dy
    
    def calc(self, i, j):
        r"""
        Definición del esquema numérico.

        Parameters
        ----------
        i, j : int
            Índices de la malla donde se hará el cálculo de los coeficientes.

        Returns
        -------
        np.array
            Regresa los coeficientes 
            :math: `a_S(i,j), a_W(i,j), a_P(i,j), a_E(i,j), a_N(i,j)` 

        """        
        dE = self.__Gamma * self.dy / self.dx
        dW = self.__Gamma * self.dy / self.dx
        dN = self.__Gamma * self.dx / self.dy
        dS = self.__Gamma * self.dx / self.dy                
        dP = dE + dW + dN + dS #- self.__Sp

        return np.array([-dS, -dW, dP, -dE, -dN])
    
#----------------------- TEST OF THE MODULE ----------------------------------
if __name__ == '__main__':

    from utils.displayInfo import printInfo        
    from geo.line import Line
    from geo.rectangle import Rectangle

    N = 6 # Nodos
    
    barra = Line(1.0)
    malla = barra.constructMesh(N)
    ivx, _, _ = malla.bounds(bi = 1, ei = N-1)
    su = np.ones(ivx)
    laplace = sDiffusion1D(malla, su)
    laplace.Gamma = 2.0
    printInfo(Descr = 'Testing Diffusion1D', 
              dx = laplace.dx, 
              vx = malla.vx)    
    print(laplace.calc(3))
    print(laplace.source(su))
    
    cuadro = Rectangle(1,1)
    malla2 = cuadro.constructMesh(N,N)
    ivx, ivy, _ = malla2.bounds(bi = 1, ei = N-1, bj = 1, ej = N-1)
    su = np.ones((ivy, ivx))
    laplace2 = sDiffusion2D(malla2, su) 
    printInfo(Descr = 'Testing Diffusion2D', 
              dx = laplace2.dx, 
              dy = laplace2.dy,
              vx = malla.vx, 
              vy = malla.vy)    
    print(laplace2.calc(3,4))
    print(laplace2.source(su))    
#----------------------- TEST OF THE MODULE ----------------------------------
