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

class Mesh():
    """
    Malla general para dominios rectangulares en 1D, 2D y 3D.
    
    Attributes
    ----------
    nx, ny, nz : int
        Número de nodos en los ejes x, y y z.
    vx, vy, vz : int
        Número de volúmenes en los ejes x, y y z.
    lx, ly, lz : float
        Longitudes del dominio en los ejes x, y  y z.
    dx, dy, dz : float or numpy array
        Tamaño de las celdas en los ejes x, y y z.
    dfacex, dfacey, dfacez : float or numpy array
        Tamaño de las caras de los volúmenes en los ejes x, y y z.
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
        
        self.nx = nx
        self.ny = ny
        self.nz = nz

        self.vx = vx
        self.vy = vy
        self.vz = vz

        self.ivx = 1
        self.ivy = 1
        self.ivz = 1

        self.lx = lx     
        self.ly = ly   
        self.lz = lz     

        self.dx = None
        self.dy = None
        self.dz = None

        self.dfacex = None
        self.dfacey = None
        self.dfacez = None
        
        self.x = None
        self.y = None
        self.z = None

        self.bi = 0
        self.ei = 1
        self.bj = 0
        self.ej = 1
        self.bk = 0
        self.ek = 1   
        
        self._adjustVolumes()
        self._adjustNodes()
        
        self.dim = '1D'
        
        if self.ny != None:
            self.dim = '2D'
        if self.nz != None:
            self.dim = '3D'

    def nodes(self):
        """
        Regresa una tupla con el número de nodos en cada dirección.
        
        Returns
        -------
        int, int, int
            Numéro de nodos en las direcciones x, y y z.

        """
        return (self.nx, self.ny, self.nz)

    def volumes(self):
        """
        Regresa una tupla con el número de volúmenes en cada dirección.
        
        Returns
        -------
        int, int, int
            Numéro de volúmenes en las direcciones x, y y z.

        """
        return (self.vx, self.vy, self.vz)

    def lengths(self):
        """
        Regresa una tupla con las longitudes del dominio en cada dirección.

        Returns
        -------
        float, float, float
            Logitudes del dominio en cada dirección.
            
        """
        return (self.lx, self.ly, self.lz)

    def deltas(self):
        """
        Regresa una tupla con las deltas de la malla en cada dirección.
        
        Returns
        -------
        dx, dy, dz
            Deltas de la malla en cada dirección.

        """
        return (self.dx, self.dy, self.dz)

    def dfaces(self):
        """
        Regresa una tupla con las deltas de la malla en cada dirección.
        
        Returns
        -------
        dfacex, dfacey, dfacez
            Deltas de la malla en cada dirección.

        """
        return (self.dfacex, self.dfacey, self.dfacez)

    def bounds(self, bi = 0, ei = 1, bj = 0, ej = 1, bk = 0, ek = 1):
        """
        Determina el inicio y el final de los cálculos numéricos sobre la malla.

        Parameters
        ----------
        bi : int
            Índice inicial de los cálculos numéricos sobre la malla en el 
            eje x. Por omisión es  0.
        ei : int
            Índice final de los cálculos numéricos sobre la malla en el 
            eje x. Por omisión es  0.
        bj : int
            Índice inicial de los cálculos numéricos sobre la malla en el 
            eje y. Por omisión es  0.
        ej : int
            Índice final de los cálculos numéricos sobre la malla en el 
            eje y. Por omisión es  0.
        bk : int
            Índice inicial de los cálculos numéricos sobre la malla en el 
            eje z. Por omisión es  0.
        ek : int
            Índice final de los cálculos numéricos sobre la malla en el 
            eje z. Por omisión es  0.
            
        Returns
        -------
        ivx, ivy, ivz
            Número de volúmenes de la malla sobre los que harán los cálculos numéricos.

        """
        self.bi = bi
        self.ei = ei
        self.bj = bj
        self.ej = ej
        self.bk = bk
        self.ek = ek
        self.ivx = ei - bi + 1
        self.ivy = ej - bj + 1
        self.ivz = ek - bk + 1 
        return (self.ivx, self.ivy, self.ivz)
    
    def _adjustVolumes(self):
        """
        Ajusta los volúmenes cuando los nodos están bien definidos.
        
        Notes
        -----
        El número de nodos en la figura de abajo es de 6 (marcados con +).
        El número de volúmenes en la misma figura es de 5 (marcados con o).
        
        1       2       3       4       5       6
        +---o---+---o---+---o---+---o---+---o---+
            1       2       3       4       5
        
        Por lo tanto el, si el número de nodos es nx, entonces el número de 
        volúmenes será nx - 1.

        """
        if self.nx != None:
            self.vx = self.nx - 1
        if self.ny != None:
            self.vy = self.ny - 1
        if self.nz != None:
            self.vz = self.nz - 1
 
    def _adjustNodes(self):
        """
        Ajusta los nodos cuando los volúmenes están bien definidos.
        
        Notes
        -----
        El número de nodos en la figura de abajo es de 6 (marcados con +).
        El número de volúmenes en la misma figura es de 5 (marcados con o).
        
        1       2       3       4       5       6
        +---o---+---o---+---o---+---o---+---o---+
            1       2       3       4       5
        
        Por lo tanto el, si el número de volúmenes es vx, entonces el número 
        de nodos será vx + 1.

        """
        if self.vx != None:
            self.nx = self.vx + 1        
        if self.vy != None:
            self.ny = self.vy + 1  
        if self.vz != None:
            self.nz = self.vz + 1  

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

    from utils.displayInfo import printInfo #pynoxtli_license_path
    
    m1 = Mesh()           
    printInfo(Test = 'Mesh()', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
    
    m1 = Mesh(nx = 5)
    printInfo(Test = 'Mesh(nx = 5)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)
   
    m1 = Mesh(vx = 8)
    printInfo(Test = 'Mesh(vx = 8)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)

    m1 = Mesh(nx = 5, lx = 5)
    printInfo(Test = 'Mesh(nx = 5, lx = 5)', 
              nx = m1.nodes(), 
              vx = m1.volumes(),
              lx = m1.lengths(),
              dx = m1.deltas(),
              dim = m1.dim)    
    
    m1 = Mesh(vx = 10, lx = 5)
    printInfo(Test = 'Mesh(vx = 10, lx = 5)', 
              nx = m1.nx, 
              vx = m1.vx,
              lx = m1.lx,
              dx = m1.dx,
              dim = m1.dim) 
    
    m2 = Mesh(nx = 5, lx = 1, ny = 21, ly = 10)
    printInfo(Test = 'Mesh(nx = 5, lx = 1, ny = 21, ly = 10)', 
              nx = m2.nx, 
              ny = m2.ny, 
              vx = m2.vx,
              vy = m2.vy,
              lx = m2.lx,
              ly = m2.ly,
              dx = m2.dx,
              dy = m2.dy,
              dim = m2.dim)     

    m3 = Mesh(nx = 3, lx = 2, 
              ny = 5, ly = 10,
              nz = 2, lz = 5)
    printInfo(Test = 'Mesh(nx = 3, lx = 2,',
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

#----------------------- TEST OF THE MODULE ----------------------------------   


# Cuando las variables tengan que convertirse en privadas podría usar
# el siguiente código.

    # @property
    # def nx(self):
    #     return self.nx

    # @property
    # def ny(self):
    #     return self.ny

    # @property
    # def nz(self):
    #     return self.nz
    
    # @property
    # def vx(self):
    #     return self.vx
    
    # @property
    # def vy(self):
    #     return self.vy
    
    # @property
    # def vz(self):
    #     return self.vz    
    
    # @property
    # def ivx(self):
    #     return self.ivx
    
    # @property
    # def ivy(self):
    #     return self.ivy
    
    # @property
    # def ivz(self):
    #     return self.ivz       
    
    # @property
    # def lx(self):
    #     return self.lx

    # @property
    # def ly(self):
    #     return self.ly

    # @property
    # def lz(self):
    #     return self.lz
    
    # @property
    # def hx(self):
    #     return self.dx

    # @property
    # def hy(self):
    #     return self.dy

    # @property
    # def hz(self):
    #     return self.dz

    # @property
    # def bi(self):
    #     return self.bi

    # @property
    # def ei(self):
    #     return self.ei

    # @property
    # def bj(self):
    #     return self.bj

    # @property
    # def ej(self):
    #     return self.ej
    
    # @property
    # def bk(self):
    #     return self.bk

    # @property
    # def ek(self):
    #     return self.ek
    
    # @property
    # def x(self):
    #     return self.x
    
    # @property
    # def y(self):
    #     return self.y
    
    # @property
    # def z(self):
    #     return self.z
    
    # @property
    # def dim(self):
    #     return self.dim