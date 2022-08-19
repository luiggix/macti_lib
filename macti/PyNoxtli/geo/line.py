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

from macti.PyNoxtli.geo.domain import Domain
from macti.PyNoxtli.geo.mesh.umesh import uMesh as Mesh
import macti.PyNoxtli.vis.flowix as vis

class Line(Domain):
    """
    Define un dominio en una dimensión.

    Attributes
    ----------
    length : float
        Longitud del dominio.
       
    """
    
    def __init__(self, length):
        super().__init__('1D')
        self.length = length
       
    def constructMesh(self, N):
        """
        Construye la malla del dominio.
        
        Parameters
        ----------
        N : int
            Número de nodos para la malla.
            
        Returns
        -------
        Mesh
            Objeto de tipo Mesh que representa la malla del dominio.
            
        Notes
        -----
        Observe que la malla se construye en la clase padre: Domain.
        
        """
        Domain.mesh = Mesh(nx = N, lx = self.length)
        
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

    from utils.displayInfo import printInfo

# Crea una línea de longitud = 8,
    linea = Line(8)
    printInfo(Length = linea.length)

# Construye la malla de la línea con 5 nodos.    
    linea.constructMesh(5)
    mesh = linea.mesh
    printInfo(Descr = 'Construcción de una malla en 1D',
              Code = 'Mesh(nodes_x = {}, length_x = {})'.format(mesh.nx, mesh.lx), 
              nodos_x = mesh.nx, 
              volumes_x = mesh.vx,
              length_x = mesh.lx,
              delta_x = mesh.dx)

# Se pueden agregar condiciones de frontera a la línea:          
    linea.boundaryConditions(dirichlet = {'LEFT':20, 'RIGHT':10})
    printInfo(Descr = 'Condiciones de frontera en la línea',
              BC_Dirichlet = linea.dirichlet,
              BC_Neumman = linea.neumman,
              Dim = linea.dim)

    input('\n Presiona <enter> para graficar la malla.')    

    par = [{'title':'Malla %s' % mesh.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    v = vis.Plotter(1,1, par)
    v.plot_mesh(1, mesh, label=True)
    v.legend()
    v.show()    
#----------------------- TEST OF THE MODULE ----------------------------------   
