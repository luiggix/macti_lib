2 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on mar mar 31 10:58:20 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../')) 
#-----------------------------------------------------------

from macti.PyNoxtli.la.csr_fvm_ijk_1D import CSR_FVM_ijk_1D
from macti.PyNoxtli.la.csr_fvm_ijk_2D import CSR_FVM_ijk_2D

from scipy.sparse import csr_matrix

class LinearSystem():
    """
    Sistema lineal generado por la discretización de una EDP.
    
    Attributes
    ---------
    A 
        Matriz del sistema lineal generada a partir de la discretización de la EDP.
    RHS : array-like
        Lado derecho del sistema lineal.
    scheme
        Esquema numérico utilizado en la discretización de la EDP.
    __dim : str
        Dimensión del problema: '1D' o '2D'.
    
    """
    A      = None 
    RHS    = None 
    scheme = None 
    dim    = None 
    
    def __init__(self, mesh, scheme):
        """
        Inicialización de la dimensión, esquema numérico y la matriz del sistema lineal.

        Parameters
        ----------
        mesh : Mesh
            Malla del dominio donde se discretiza la EDP.
        scheme 
            Esquema numérico usado en la discretización de la EDP.

        """
        LinearSystem.scheme = scheme
        LinearSystem.dim = mesh.dim
        
        #
        # Se utiliza el almacenamiento de tipo CSR para la matriz del sistema.
        #
        if LinearSystem.dim == '1D':
            LinearSystem.A = CSR_FVM_ijk_1D(mesh.bi, mesh.ei)

        if LinearSystem.dim == '2D':
            LinearSystem.A = CSR_FVM_ijk_2D(mesh.bi, mesh.ei, 
                                            mesh.bj, mesh.ej)      
        
    @staticmethod
    def constructMat():
        """
        Construye la matriz del sistema lineal.

        Notes
        -----
        Se ejecuta la función construct() del objeto __A que representa a la
        matriz del sistema lineal. Esta función debe estar definida en la clase
        que se encarga de gestionar el almacenamiento de la matriz, en este 
        caso CSR.

        """
        LinearSystem.A.construct(LinearSystem.scheme)

    @staticmethod
    def correctMat():
        """
        Corrige algunos valores en el arreglo AA.
        
        Es usada para las pruebas en este archivo. No es usada en producción.

        """
        LinearSystem.A.correct()
        
    @staticmethod
    def constructRHS(phi):
        """
        Construye el lado derecho del sistema lineal.

        Parameters
        ----------
        phi : array-like
            Arreglo donde se almacena la solución del problema.
            
        Notes
        -----
        El RHS depende del tipo de esquema numérico que se use en la 
        discretización, por esa razón se utiliza el objeto `__scheme` para 
        obtener el RHS (a través de la función source()).

        """
        LinearSystem.RHS = LinearSystem.scheme.source(phi)
        
    # @staticmethod
    # def getMat():
    #     return LinearSystem.A

    # @staticmethod
    # def getRHS():
    #     return LinearSystem.RHS
    
    @staticmethod
    def getCSR():
        """
        Obtiene la matriz en formato CSR.
        
        Esta matriz se obtiene de la conversión de los arreglos AA, JA e IA
        al tipo csr_matrix de scipy.sparse.

        """
        return csr_matrix((LinearSystem.A.AA,  
                           LinearSystem.A.JA, 
                           LinearSystem.A.IA))
        
    # @staticmethod
    # def getScheme():
    #     return LinearSystem.__scheme

    @staticmethod
    def printMat(nice):
        """
        Despliegua la matriz.

        Parameters
        ----------
        nice : bool
            Determina la forma en que se va a desplegar la matriz.

        """
        return LinearSystem.A.printMat(nice=nice)

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from geo.mesh.umesh import uMesh
    from utils.displayInfo import printInfo
    import numpy as np

    class Test():
    
        def __init__(self):
            self.__name = 'Test'
        
        def source(self, phi):
            return phi * 1
        
        def calc(self, i):
            print('Test calc()', i)
            return -1, 2, -1
    

    Nx = 10
#
# Create a mesh 
#        
    malla = uMesh(nx  = Nx, lx = 1)
    ivx, _, _ = malla.bounds(bi = 1, ei = Nx - 1)
    printInfo(Descr = 'Malla de prueba',
              Test = 'Mesh(nodes_x = %d, length_x = %f)' % (malla.nx, malla.lx), 
              nodes_x   = malla.nx, 
              volumes_x = malla.vx,
              length_x  = malla.lx,
              delta_x   = malla.dx,
              ivx = ivx)
#
# Create a test scheme to try a LinearSystem
#    
    scheme_test =  Test()
    
    u = np.zeros(malla.vx+2)
#
# Create a LinearSystem
#
    LinearSystem(malla, scheme_test)
    LinearSystem.constructMat()

    LinearSystem.correctMat() # Esta función se usa para corregir algunos valores
                # En las aplicaciones esta función es sustitutida por aquella que
                # calcula las condiciones de frontera.
    
    LinearSystem.constructRHS(u[1:-1])
    LinearSystem.printMat(nice=True)
    A = LinearSystem.getCSR()
    b = np.ones(Nx-1)
    b[0] = 0
    b[-1] = 0
    print(b)
    print(A)
#
# Solve the LinearSystem using CG from sparse.linalg
#
    import scipy.sparse.linalg as spla
    sol = spla.cg(A,b)[0]   

    print(sol)
    x = np.linspace(0,1,malla.vx)
    import matplotlib.pyplot as plt    
    plt.plot(x,sol,'o-', label='Test solution')
    plt.legend()
    plt.show()
    
#----------------------------------
    
    class Test2():
    
        def __init__(self):
            self.__name = 'Test'
        
        def source(self, phi):
            return phi * 1
        
        def calc(self, i, j):
            print('Test calc()', i, j)
            return -1, -1, 4, -1, -1
    
    Nx = 10
    Ny = 10
#
# Create a mesh 
#        
    malla = uMesh(nx  = Nx, lx = 1, ny = Ny, ly = 1)
    ivx, ivy, _ = malla.bounds(bi = 1, ei = Nx - 1,
                             bj = 1, ej = Ny - 1)
    printInfo(Descr = 'Malla de prueba',
              Test = 'Mesh(nodes_x = %d, length_x = %f)' % (malla.nx, malla.lx), 
              nx_ny   = (malla.nx, malla.ny), 
              vx_vy = (malla.vx, malla.vy),
              lx_ly  = (malla.lx, malla.lx),
              dx_dy   = (malla.dx, malla.dy),
              ivx_ivy = (ivx, ivy))
    vx = malla.vx
    vy = malla.vy
#
# Create a test scheme to try a LinearSystem
#    
    scheme_test =  Test2()
    
    u = np.zeros((malla.vx+2, malla.vy+2))
#
# Create a LinearSystem
#
    LinearSystem(malla, scheme_test)
    LinearSystem.constructMat()
    
    LinearSystem.correctMat() # Esta función se usa para corregir algunos valores
                # En las aplicaciones esta función es sustitutida por aquella que
                # calcula las condiciones de frontera.
    
    LinearSystem.constructRHS(u[1:-1, 1:-1])
#    LinearSystem.printMat(nice=True)
    A = LinearSystem.getCSR()
    b = np.ones(vx * vy)
    
    print(b)
#    print(A)
#
# Solve the LinearSystem using CG from sparse.linalg
#
    import scipy.sparse.linalg as spla
    sol = spla.cg(A,b)[0]   

    print(sol)
    
    x, y = np.meshgrid(np.linspace(0,1,vx), np.linspace(0,1,vy))
    sol.shape = (vx,vy)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    surf = ax.plot_surface(x,y,sol, cmap='coolwarm')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show() 
#----------------------- TEST OF THE MODULE ----------------------------------   
      
