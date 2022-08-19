#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on vie mar 27 14:10:38 CST 2020]
"""

#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../'))
#-----------------------------------------------------------

from macti.PyNoxtli.geo.domain import Domain
from macti.PyNoxtli.geo.mesh.umesh import uMesh as Mesh
import macti.PyNoxtli.vis.flowix as vis

class Rectangle(Domain):
    """
    Define un dominio rectangular en 2D.
    
    Attributes
    ----------
    length_x : float
        Longitud del dominio en el eje x.    
    length_y : float
        Longitud del dominio en el eje y. 
        
    """
    
    def __init__(self, length_x, length_y):
        super().__init__('2D')
        self.length_x = length_x     
        self.length_y = length_y   
       
    def constructMesh(self, nodes_x, nodes_y):
        """
        Construye la malla del dominio.
        
        Parameters
        ----------
        nodes_x : int
            Número de nodos para la malla en el eje x.
        nodes_y : int
            Número de nodos para la malla en el eje y.
            
        Returns
        -------
        Mesh
            Objeto de tipo Mesh que representa la malla del dominio.
            
        Notes
        -----
        Observe que la malla se construye en la clase padre: Domain.
        
        """
        Domain.mesh = Mesh(nx = nodes_x, lx = self.length_x,
                           ny = nodes_y, ly = self.length_y)                           

        return Domain.mesh
    
    def boundaryConditions(self, dirichlet = None, neumman = None):
        """
        Define las condiciones de frontera.
        
        Parameters
        ----------
        dirichlet : dict
            Diccionario que define las condiciones de frontera de tipo Dirichlet
            en los extremos de la línea.
        neumman : dict
            Diccionario que define las condiciones de frontera de tipo Neumman
            en los extremos de la línea        
        """
        if dirichlet == None:
            dirichlet = { }
        if neumman == None:
            neumman = { }
            
        Domain.dirichlet = dirichlet
        Domain.neumman = neumman

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from macti.PyNoxtli.utils.displayInfo import printInfo
    
    cuadro = Rectangle(5,4)
    printInfo(Length_x = cuadro.length_x, Length_y = cuadro.length_y)    
    cuadro.constructMesh(6,5)
    mesh = cuadro.mesh
    
    printInfo(Descr = 'Construcción de la malla en 2D',
              nodes_x = mesh.nx,
              nodes_y = mesh.ny,               
              volumes_x = mesh.vx,
              volumes_y = mesh.vy,
              length_x = mesh.lx,
              length_y = mesh.ly,
              delta_x = mesh.dx,
              delta_y = mesh.dy) 

# Se pueden agregar condiciones de frontera al dominio:          
    cuadro.boundaryConditions(dirichlet = {'LEFT':20, 'RIGHT':10},
                              neumman = {'TOP':4, 'BOTTOM':89})
    printInfo(Descr = 'Condiciones de frontera en el dominio 2D',
              BC_Dirichlet = cuadro.dirichlet,
              BC_Neumman = cuadro.neumman,
              Dim = cuadro.dim)

    input('\n Presiona <enter> para graficar la malla.')    

    par = [{'title':'Mesh %s' % mesh.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    v = vis.Plotter(1,1, par)
    v.plot_mesh(1, mesh, label = True)
    v.legend()
    v.show()    
#----------------------- TEST OF THE MODULE ----------------------------------   
