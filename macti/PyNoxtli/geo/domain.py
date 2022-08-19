#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on jue mar 26 18:42:46 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../'))
#-----------------------------------------------------------

class Domain():
    """
    Define el dominio de solución.

    Attributes
    ----------
    mesh
        Malla del dominio.
    dirichlet : dict
        Condiciones de frontera tipo Dirichlet. 
    neumman : dict
        Condiciones de frontera tipo Neumman
    dim : str
        Dimensión del dominio, que puede ser: '1D', '2D' o '3D'
    
    Notes
    -----
    El keyword del diccionario usado para las condiciones de frontera 
    indica el lugar donde se aplica, mientras que el value proporciona 
    el valor de la condición.
        
    Esta es una clase base abstracta de la cual heredan otras clases más
    especializadas como Line() o Rectangle().
    """
    
    mesh = None
    dirichlet = {'None':0}
    neumman = {'None':0}
    dim = None
    
    def __init__(self, dim):
        Domain.dim = dim
        
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from macti.PyNoxtli.utils.displayInfo import printInfo

    class MyDomain(Domain):
        """
        Ejemplo de clase que hereda de Domain.
        
        """
        
        def __init__(self, a, b):
            super().__init__('1D') # Execute the constructor of base class (Domain)
            self.__a = a
            self.__b = b
            print('MyDomain.__init__(%f, %f)' % (a,b))
            
        def longitud(self):
            """
            Ejemplo de un método de la clase.
            
            """
            longitud = self.__b - self.__a
            
            return longitud    

# Crea una clase de tipo Domain e imprime sus atributos
    dom = Domain('3D')
    printInfo(Mesh = dom.mesh,
              Dirichlet = dom.dirichlet,
              Neumman  = dom.neumman,
              Dim = dom.dim)
    
# Crea una clase de tipo MyDomain e imprime sus atributos
    t = MyDomain(b=1.2342,a=2.00123)
    t.mesh = "hola" 
    t.dirichlet = {'RIGHT':10, 'LEFT':5}    
    t.neumman = {'RIGHT_WALL':'D', 'LEFT_WALL':'D'}
    t.dim = '1D'
    printInfo(Mesh = t.mesh,
              Dirichlet = t.dirichlet,
              Neumman  = t.neumman,
              Dim = t.dim,
              Longitud = t.longitud())
#----------------------- TEST OF THE MODULE ----------------------------------   

