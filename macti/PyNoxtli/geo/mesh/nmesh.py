#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on vie mar 27 14:28:57 CST 2020].
"""

#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../../')) 
#-----------------------------------------------------------

import numpy as np
from macti.PyNoxtli.geo.mesh.basemesh import Mesh
import macti.PyNoxtli.vis.flowix as vis

class nMesh(Mesh):
    """
    Malla uniforme para dominios rectangulares en 1D, 2D y 3D.
    
    Attributes
    ----------
    nx, ny, nz : int
        Número de nodos en los ejes x, y y z.
    vx, vy, vz : int
        Número de volúmenes en los ejes x, y y z.
    lx, ly, lz : float
        Longitudes del dominio en los ejes x, y  y z.
    dx, dy, dz : float
        Tamaño de las celdas en los ejes x, y y z.
    bi, bj, bk : int
        Inicio (en la malla) desde donde se hacen los cálculos numéricos.
    ei, ej, bk : int
        Final (en la malla) donde terminan los cálculos numéricos.
    x, y, z: numpy array
        Arreglos con las coordenadas de los puntos de la malla.
    dim : str
        Dimensión de la malla, puede ser '1D', '2D' o '3D'.
    ivx, ivy, ivz : int
        
    """
    
    def __init__(self, x, y = np.zeros(1), z = np.zeros(1)):
        nny = None
        nnz = None
        
        if len(y) > 1:
            nny = len(y)
        if len(z) > 1:
            nnz = len(z)
            
        super().__init__(nx = len(x), ny = nny, nz = nnz, 
                         lx = x[-1],  ly = y[-1],  lz = z[-1])
       
        self.x = x
        self.y = y
        self.z = z
        
        self.xvols = None
        self.yvols = None
        self.zvols = None

        if self.vx != None:
            self.xvols = np.zeros(self.vx + 2)            
            self.xvols[0] = self.x[0]
            for i in range(1, self.vx + 1):
                self.xvols[i] = (self.x[i-1] + self.x[i]) / 2
            self.xvols[self.vx + 1] = self.x[-1]
            
        if self.vy != None:
            self.yvols = np.zeros(self.vy + 2)
            self.yvols[0] = self.y[0]
            for i in range(1, self.vy + 1):
                self.yvols[i] = (self.y[i-1] + self.y[i]) / 2
            self.yvols[self.vy + 1] = self.y[-1]            
            
        if self.vz != None:
            self.zvols = np.zeros(self.vz + 2)
            self.zvols[0] = self.y[0]
            for i in range(1, self.vz + 1):
                self.zvols[i] = (self.z[i-1] + self.z[i]) / 2
            self.zvols[self.vz + 1] = self.z[-1] 
            
        
    def coordinatesMeshFVM(self):
        """
        Construye las coordenadas de los volúmenes.

        Returns
        -------
        x, y, z : array-like
        Coordenadas de los puntos de la malla.

        """           
        return self.xvols, self.yvols, self.zvols
            
    def coordinatesMeshFDM(self):
        """
        Construyelas coordenadas de los nodos.

        Returns
        -------
        x, y, z : array-like
        Coordenadas de los nodos de la malla, estos arreglos son atributos de la malla.
        
        """
        return self.x, self.y, self.z
        
    def setCells(self, dx = None, dy = None, dz = None):
        """
        Calcula el tamaño de las celdas de la malla cuando es uniforme.

        Notes
        -----
                   dx
                |-------|
                v       v
        +---o---+---o---+---o---+---o---+---o---+

        """
        if self.dx != None:
            self.dx = dx
        if self.dy != None:
            self.dy = dy            
        if self.dz != None:
            self.dz = dz

    def setFaces(self, dfacex = None, dfacey = None, dfacez = None):
        """
        Calcula el tamaño de las celdas de la malla cuando es uniforme.

        Notes
        -----
                   dx
                |-------|
                v       v
        +---o---+---o---+---o---+---o---+---o---+

        """
        if self.dfacex != None:
            self.dfacex = dfacex
        if self.dfacey != None:
            self.dfacey = dfacey            
        if self.dfacez != None:
            self.dfacez = dfacez

    def __del__(self):
        """
        Nothing to do.
        
        Returns
        -------
        None.

        """
        pass
        

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from utils.displayInfo import printInfo

    x = np.linspace(0, 1, 11)
    y = np.linspace(0, 2, 5)
    z = np.linspace(0, 3, 9)
    mesh1D = nMesh(x)
    printInfo(Descr = 'Plot a 1D mesh',
              Test = 'nMesh(x)', 
              nx = mesh1D.nx, 
              vx = mesh1D.vx,
              lx = mesh1D.lx,
              x = mesh1D.x,
              dim = mesh1D.dim) 

    mesh2D = nMesh(x, y)
    printInfo(Descr = 'Plot a 2D mesh',
              Test = 'nMesh(x, y)', 
              nx_ny = (mesh2D.nx, mesh2D.ny), 
              vx_vy = (mesh2D.vx, mesh2D.vy),
              lx_ly = (mesh2D.lx, mesh2D.ly),
              x = mesh2D.x,
              y = mesh2D.y,
              dim = mesh2D.dim) 

    mesh3D = nMesh(x, y, z)
    printInfo(Descr = 'Plot a 3D mesh',
              Test = 'nMesh(x, y, z)', 
              nx_ny_nz = (mesh3D.nx, mesh3D.ny, mesh3D.nz), 
              vx_vy_vz = (mesh3D.vx, mesh3D.vy, mesh3D.vz),
              lx_ly_lz = (mesh3D.lx, mesh3D.ly, mesh3D.lz),
              x = mesh3D.x,
              y = mesh3D.y,
              z = mesh3D.z,
              dim = mesh3D.dim) 
    
    x = np.array([ 0, 0.307917, 0.767275, 1.45256, 2.47488, 4, 
                  5.52512, 6.54744, 7.23272, 7.69208, 8 ])

    y = np.array([ 0, 0.307917, 0.767275, 1.45256, 2.47488, 4, 
                  5.52512, 6.54744, 7.23272, 7.69208, 8 ])

    input('Presione <enter> para graficar las mallas:')
    
    malla1D = nMesh(x)
    printInfo(Descr = 'Plot a 1D mesh',
              Test = 'nMesh(x)', 
              nx = malla1D.nx, 
              vx = malla1D.vx,
              lx = malla1D.lx,
              x  = malla1D.x,
              dim = malla1D.dim) 
    
    par = [{'title':'Mesh %s' % malla1D.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    v = vis.Plotter(1,1, par)
    v.plot_mesh(1, malla1D, nod='|', vol='.')
        
    malla2D = nMesh(x, y)
    printInfo(Descr = 'Plot a 2D mesh',
              Test = 'nMesh(x, y)', 
              nx_ny = (malla2D.nx, malla2D.ny), 
              vx_vy = (malla2D.vx, malla2D.vy),
              lx_ly = (malla2D.lx, malla2D.ly),
              x = malla2D.x,
              y = malla2D.y,
              dim = malla2D.dim) 
    
    par = [{'title':'Mesh %s' % malla2D.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    v = vis.Plotter(1,1, par)
    v.plot_mesh(1, malla2D, vol='.', label=True)
    v.legend()
    v.show()
    
#----------------------- TEST OF THE MODULE ----------------------------------   
