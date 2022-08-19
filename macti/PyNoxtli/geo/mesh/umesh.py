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

class uMesh(Mesh):
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
    
    def __init__(self, 
                 nx = None, ny = None, nz = None,
                 vx = None, vy = None, vz = None,
                 lx = None, ly = None, lz = None):
        super().__init__(nx, ny, nz, vx, vy, vz, lx, ly, lz)

#        print('uMesh')
        self.__calcDeltas()

    def coordinatesMeshFVM(self):
        """
        Construye las coordenadas de los volúmenes.

        Returns
        -------
        x, y, z : array-like
        Coordenadas de los puntos de la malla.

        """
        x = []
        y = []
        z = []
        
        if self.vx != None:
            first_volume = self.dx / 2
            final_volume = self.lx - first_volume
            x = np.zeros(self.vx + 2) # Se agregan dos espacios para las fronteras
            # Se crean los volúmenes en el interior:
            x[1:-1] = np.linspace(first_volume, final_volume, self.vx) 
            x[-1] = self.lx # Se agrega punto final la malla.
            
        if self.vy != None:
            first_volume = self.dy / 2
            final_volume = self.ly - first_volume
            y = np.zeros(self.vy + 2) # Se agregan dos espacios para las fronteras
            # Se crean los volúmenes en el interior:
            y[1:-1] = np.linspace(first_volume, final_volume, self.vy)
            y[-1] = self.ly  # Se agrega punto final la malla.

        if self.vz != None:
            first_volume = self.dz / 2
            final_volume = self.lz - first_volume
            z = np.zeros(self.vz + 2) # Se agregan dos espacios para las fronteras
            # Se crean los volúmenes en el interior:
            z[1:-1] = np.linspace(first_volume, final_volume, self.vz)
            x[-1] = self.lz # Se agrega punto final la malla.
           
        return x, y, z
            
    def coordinatesMeshFDM(self):
        """
        Construyelas coordenadas de los nodos.

        Returns
        -------
        x, y, z : array-like
        Coordenadas de los nodos de la malla, estos arreglos son atributos de la malla.
        
        """
        if self.nx != None:
            self.x = np.linspace(0, self.lx, self.nx)
        if self.ny != None:
            self.y = np.linspace(0, self.ly, self.ny)
        if self.nz != None:
            self.z = np.linspace(0, self.lz, self.nz)
            
        return self.x, self.y, self.z

    def setNodes(self, nx = None, ny = None, nz = None):
        """
        Establece el número de nodos en cada dirección.

        Parameters
        ----------
        nx : int
            Número de nodos en la dirección x. El valor por omisión es None.
        ny : int
            Número de nodos en la dirección y. El valor por omisión es None.
        nz : int
            Número de nodos en la dirección z. El valor por omisión es None.

        Notes
        -----
        Cuando el número de nodos es establecido por el usuario, los volúmenes
        son ajustados e inmediatamente se calculan las deltas.

        """
        self.nx = nx
        self.ny = ny
        self.nz = nz
        
        self._adjustVolumes()
        self.__calcDeltas()
        
    def setVolumes(self, vx = None, vy = None, vz = None):
        """
        Establece el número de nodos en cada dirección.

        Parameters
        ----------
        vx : int
            Número de volúmenes en la dirección x. El valor por omisión es None.
        vy : int
            Número de volúmenes en la dirección y. El valor por omisión es None.
        vz : int
            Número de volúmenes en la dirección z. El valor por omisión es None.

        Notes
        -----
        Cuando el número de volúmenes es establecido por el usuario, los nodos
        son ajustados e inmediatamente se calculan las deltas.
        
        """
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self._adjustNodes()
        self.__calcDeltas()
        
    def __calcDeltas(self):
        """
        Calcula el tamaño de las celdas de la malla cuando es uniforme.

        Notes
        -----
                   dx
                |-------|
                v       v
        +---o---+---o---+---o---+---o---+---o---+

        """
        if self.lx != None:
            self.dx = self.lx / self.vx
        if self.ly != None:
            self.dy = self.ly / self.vy            
        if self.lz != None:
            self.dz = self.lz / self.vz

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

    m1 = uMesh()
    printInfo(Test = 'uMesh()', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
    
    m1.setNodes(nx = 21)
    printInfo(Test = 'm1.setNodes(nx = 21)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
    
    m1.setVolumes(vx = 12)
    printInfo(Test = 'm1.setVolumes(nx = 12)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
    
    m1 = uMesh(nx = 5)
    printInfo(Test = 'uMesh(nx = 5)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
   
    m1 = uMesh(vx = 8)
    printInfo(Test = 'uMesh(vx = 8)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)

    m1 = uMesh(nx = 5, lx = 5)
    printInfo(Test = 'uMesh(nx = 5, lx = 5)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)    
    
    m1 = uMesh(vx = 10, lx = 5)
    printInfo(Test = 'uMesh(vx = 10, lx = 5)', 
              nx = m1.nx, 
              vx = m1.vx,
              lx = m1.lx,
              dx = m1.dx,
              dim = m1.dim) 

    m1.setNodes(nx = 21)
    printInfo(Descr = 'Create a uMesh object then change nx',
              Test = 'm1.setNodes(nx = 21)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)

    m1.setVolumes(vx = 10)
    printInfo(Descr = 'Create a uMesh object then change vx',
              Test = 'm1.setVolumes(vx = 10)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
    
    m2 = uMesh(nx = 5, lx = 1, ny = 21, ly = 10)
    printInfo(Test = 'uMesh(nx = 5, lx = 1, ny = 21, ly = 10)', 
              nx = m2.nx, 
              ny = m2.ny, 
              vx = m2.vx,
              vy = m2.vy,
              lx = m2.lx,
              ly = m2.ly,
              dx = m2.dx,
              dy = m2.dy,
              dim = m2.dim)     

    m3 = uMesh(nx = 3, lx = 2, 
              ny = 5, ly = 10,
              nz = 2, lz = 5)
    printInfo(Test = 'uMesh(nx = 3, lx = 2,',
              con1 = '     ny = 5, ly = 10,', 
              con2 = '     nz = 2, lz = 5)',
              nx_ny_nz  = m3.nodes(), 
              vx = m3.vx,
              vy = m3.vy,
              vz = m3.vz,
              lx  = m3.lx,
              ly  = m3.ly,
              lz  = m3.lz,
              dx_dy_dz   = m3.deltas(),
              dim = m3.dim)

    input('Presione <enter> para graficar las mallas:')
    
    mesh1D = uMesh(nx = 11, lx = 1)
    printInfo(Descr = 'Plot a 1D mesh',
              Test = 'uMesh(nx = 11, lx = 1)', 
              nx = mesh1D.nx, 
              vx = mesh1D.vx,
              lx = mesh1D.lx,
              dx = mesh1D.dx,
              dim = mesh1D.dim) 
    
    par = [{'title':'Mesh %s' % mesh1D.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    v = vis.Plotter(1,1, par)
    v.plot_mesh(1, mesh1D)
        
    mesh2D = uMesh(nx = 5, lx = 2, ny = 6, ly = 1)
    printInfo(Descr = 'Plot a 2D Mesh',
              Test = 'uMesh(nx = 5, lx = 2, ny = 6, ly = 1)', 
              nx   = mesh2D.nx, 
              ny   = mesh2D.ny, 
              vx = mesh2D.vx,
              vy = mesh2D.vy,
              lx  = mesh2D.lx,
              ly  = mesh2D.ly,
              dx   = mesh2D.dx,
              dy   = mesh2D.dy,
              dim = mesh2D.dim) 
    
    par = [{'title':'Mesh %s' % mesh2D.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    v = vis.Plotter(1,1, par)
    v.plot_mesh(1, mesh2D, label=True)
    v.legend()
    v.show()
#----------------------- TEST OF THE MODULE ----------------------------------   
