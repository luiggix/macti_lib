#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on mié abr  1 16:23:55 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../')) 
#-----------------------------------------------------------

from macti.PyNoxtli.la.linsys import LinearSystem
import scipy.sparse.linalg as spla
import numpy as np

class PDE():
    """
    Clase para aproximar la solución de una EDP numéricamente.
    
    Attributes
    ----------
    domain : Domain
        Dominio donde se resuelve la EDP.
    linsys : LinearSystem
        Sistema lineal generado por el método numérico.
    dim : int
        Dimensión del problema.
        
    __phi : Array-like.
        Campo escalar donde se almacena la solución aproximada de la EDP.
    scheme
        Esquema numérico para calcular los coeficientes del sistema lineal.       

    """
    domain = None
    linsys = None
    dim = None
    
    def __init__(self, domain, phi):# ht = 1.0):
        """
        Inicializa algunos atributos de la EDP.
        
        Parameters
        ----------
        domain : Domain
            Dominio donde se resuelve la EDP.
        phi : Array-like
            Campo escalar donde se almacena la solución aproximada de la EDP.
            (Variable dependiente, Variable primaria.)
        """
        PDE.domain = domain
        PDE.dim = PDE.domain.dim
        self.__phi = phi
        self.scheme = None

    def setNumericalScheme(self, scheme):
        """
        Inicializa el objeto `linsys` que representa el sistema lineal.

        Parameters
        ----------
        scheme 
            Esquema numérico para calcular los coeficientes del sistema lineal.

        """
        PDE.linsys = LinearSystem(PDE.domain.mesh, scheme)
        self.scheme = scheme

    def solve(self, sym=True):
        """
        Resuelve la EDP numéricamente.

        Parameters
        ----------
        opt : bool, optional
            Optimización ¿?. The default is False.
        sym : bool, optional
            Determina si la matriz es simétrica o no. The default is True.
            
        Returns
        -------
        __phi : Array-like
            Solución aproximada de la EDP.
            
        """
        PDE.linsys.constructMat()
        PDE.linsys.constructRHS(self.__phi)
                        
        self.__applyBoundaryConditions()

        if sym:
            sol, info = spla.cg(PDE.linsys.getCSR(),
                                PDE.linsys.RHS)#,
                                # tol=1e-08,
                                # maxiter= 100)
        else:
            sol, info = spla.bicgstab(PDE.linsys.getCSR(),
                                      PDE.linsys.RHS,
                                      tol=1e-08,
                                      maxiter= 100)
        self.__update(sol)
        
        return self.__phi 

    def printMat(self, nice):
        """
        Imprime la matriz del sistema.

        Parameters
        ----------
        nice : bool
            Forma de impresión de la matriz.

        """
        return PDE.linsys.printMat(nice=nice)

    def printRHS(self):
        """Imprime el lado derecho del sistema."""
        print(PDE.linsys.RHS)
        
    def __applyBoundaryConditions(self):
        """
        Ejecuta las condiciones de frontera.

        Esta tarea se realiza dependiendo de la dimensión del problema y de
        las condiciones definidas en el dominio de estudio.

        """
        if PDE.dim == '1D':
            for wall, value in PDE.domain.dirichlet.items():
                self.__bcDirichlet1D(wall, value)
        
            for wall, flux in PDE.domain.neumman.items():
                self.__bcNeumman1D(wall, flux)

        if PDE.dim == '2D':
            for wall, value in PDE.domain.dirichlet.items():
                self.__bcDirichlet2D(wall, value)
        
            for wall, flux in PDE.domain.neumman.items():
                self.__bcNeumman2D(wall, flux)                

    def __bcDirichlet1D(self, wall, value):
        """
        Aplica las condiciones de tipo Dirichlet en 1D.

        Parameters
        ----------
        wall : string
            Describe la frontera donde se aplicará la condición de frontera.
        value : float
            Valor que se aplica en la frontera.

        """      
        A  = PDE.linsys.A
        Su = PDE.linsys.RHS       
        AA = A.AA
        
        if wall == 'LEFT':
            # Recuerda que: AA[0], AA[1], AA[2] <=> -aW, aP, -aE
            aW = -AA[0]
            AA[1] += aW # aP* = (aP + aW)
            AA[0]  = 0  # aW* = 0
            Su[0] += 2 * aW * value
            
        if wall == 'RIGHT':
            # Recuerda que: AA[-3], AA[-2], AA[-1] <=> -aW, aP, -aE
            aE = -AA[-1]            
            AA[-2] += aE # aP* = (aP + aE)
            AA[-1]  = 0  # aE* = 0  
            Su[-1] += 2 * aE * value

    def __bcDirichlet2D(self, wall, value):
        """
        Aplica las condiciones de tipo Dirichlet en 2D.

        Parameters
        ----------
        wall : string
            Describe la frontera donde se aplicará la condición de frontera.
        value : float
            Valor que se aplica en la frontera.

        """     
        A  = PDE.linsys.A
        Su = PDE.linsys.RHS
        AA = A.AA
        IA = A.IA
        
        NTx = A.NTx
        NTy = A.NTy
        OFFSET = (NTy - 1) * NTx

        if wall == 'LEFT':
#            print('LEFT')
            IS = 0
            for j in range(NTy):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[NTx * j] + 2 # aP
                aW = -AA[I-1]
                AA[I] += aW # aP* = (aP + aW)
                AA[I-1] = 0 # aW* = 0
                Su[IS] += 2 * aW * value
                IS += NTx
                
        if wall == 'RIGHT': 
#            print('RIGHT')
            IS = NTx-1
            for j in range(NTy):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[NTx * (j + 1) - 1] + 2 # aP
                aE = -AA[I+1]
                AA[I] += aE # aP* = (aP + aE)
                AA[I+1] = 0 # aE* = 0
                Su[IS] += 2 * aE * value
                IS += NTx                
        
        if wall == 'BOTTOM':
#            print('BOTTOM')
            for i in range(NTx):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[i] + 2 # aP
                aS = -AA[I-2]
                AA[I] += aS # aP* = (aP + aS)
                AA[I-2] = 0 # aS* = 0
                Su[i] += 2 * aS * value
        
        if wall == 'TOP':
#            print('TOP')
            for i in range(NTx):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[i+OFFSET] + 2 # aP
                aN = -AA[I+2]
                AA[I] += aN # aP* = (aP + aN)
                AA[I+2] = 0 # aN* = 0
                Su[i+OFFSET] += 2 * aN * value                
        
    def __bcNeumman1D(self, wall, flux = 0):
        """
        Aplica las condiciones de tipo Neumman en 1D.

        Parameters
        ----------
        wall : string
            Describe la frontera donde se aplicará la condición de frontera.
        flux : float
            Valor del flujo que se aplica en la frontera.

        """
        A  = PDE.linsys.A
        Su = PDE.linsys.RHS
        mesh = PDE.domain.mesh
        AA = A.AA
        
        if wall == 'LEFT':
            # Recuerda que: AA[0], AA[1], AA[2] <=> -aW, aP, -aE            
            aW = AA[0] # aW Almacenado con el signo negativo                       
            AA[1] += aW # aP* = (aP - aW)
            AA[0]  = 0  # aW* = 0  
            Su[0] += aW * flux * mesh.dx
            
        if wall == 'RIGHT':
            # Recuerda que: AA[-3], AA[-2], AA[-1] <=> -aW, aP, -aE
            aE = AA[-1] # aW Almacenado con el signo negativo
            AA[-2] += aE # aP* = (aP - aE)
            AA[-1]  = 0  # aE* = 0
            Su[-1] -= aE * flux * mesh.dx              

    def __bcNeumman2D(self, wall, flux = 0):
        """
        Aplica las condiciones de tipo Neumman en 1D.

        Parameters
        ----------
        wall : string
            Describe la frontera donde se aplicará la condición de frontera.
        flux : float
            Valor del flujo que se aplica en la frontera.

        """   
        A  = PDE.linsys.A
        Su = PDE.linsys.RHS
        mesh = PDE.domain.mesh
        AA = A.AA
        IA = A.IA
        NTx = A.NTx
        NTy = A.NTy
        OFFSET = (NTy - 1) * NTx
        
        if wall == 'LEFT':
#            print('LEFT')
            IS = 0
            for j in range(NTy):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[NTx * j] + 2 # aP
                aW = AA[I-1] # aW Almacenado con el signo negativo
                AA[I] += aW # aP* = (aP - aW)
                AA[I-1] = 0 # aW* = 0
                Su[IS] += aW * flux * mesh.dx
                IS += NTx

        if wall == 'RIGHT': 
#            print('RIGHT')
            IS = NTx-1
            for j in range(NTy):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[NTx * (j + 1) - 1] + 2 # aP
                aE = AA[I+1] # aP Almacenado con el signo negativo
                AA[I] += aE # aP* = (aP - aE)
                AA[I+1] = 0 # aE* = 0
                Su[IS] -= aE * flux * mesh.dx
                IS += NTx  

        if wall == 'BOTTOM':
#            print('BOTTOM')
            for i in range(NTx):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[i] + 2 # aP
                aS = AA[I-2] # aP Almacenado con el signo negativo
                AA[I] += aS # aP* = (aP - aS)
                AA[I-2] = 0 # aS* = 0
                Su[i] += aS * flux * mesh.dy
                
        if wall == 'TOP':
#            print('TOP')
            for i in range(NTx):
            # Recuerda que: AA[I-2], AA[I-1], AA[I], AA[I+1], AA[I+2]
            # ============>   -aS  ,  -aW   ,  aP  ,  -aE   ,  -aN
                I = IA[i+OFFSET] + 2 # aP
                aN = AA[I+2] # aP Almacenado con el signo negativo
                AA[I] += aN # aP* = (aP - aN)
                AA[I+2] = 0 # aN* = 0
                Su[i+OFFSET] -= aN * flux * mesh.dy   
        
    def __update(self, sol):
        """
        Actualiza la solución (phi) después de hacer el cálculo.

        Parameters
        ----------
        sol : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        mesh = PDE.domain.mesh
        phi = self.__phi

        if PDE.dim == '1D':
            phi[1:-1] = sol[:]
            for key, value in PDE.domain.neumman.items():
                if key == 'LEFT':
                    phi[ 0] = phi[1] - value * mesh.dx * 0.5
                elif key == 'RIGHT':
                    phi[-1] = phi[-2] + value * mesh.dx * 0.5

        if PDE.dim == '2D':
            ivx = PDE.domain.mesh.ivx
            ivy = PDE.domain.mesh.ivy
            sol.shape = (ivy, ivx)
            phi[1:-1,1:-1] = sol[:]
            for key, value in PDE.domain.neumman.items():
                if key == 'LEFT':
#                    print('LEFT')
                    phi[: , 0] = phi[: , 1] - value * mesh.dx * 0.5
                elif key == 'RIGHT':
#                    print('RIGHT')
                    phi[: ,-1] = phi[: ,-2] + value * mesh.dx * 0.5
                elif key == 'BOTTOM':
#                    print('BOTTOM')
                    phi[ 0, :] = phi[ 1, :] - value * mesh.dy * 0.5
                elif key == 'TOP':
#                    print('TOP')
                    phi[-1, :] = phi[-2, :] + value * mesh.dy * 0.5 
#
# When the problem depens on time, the RHS must be update with the new 
# solution. Next line update the RHS. 
#
#        PDE.__linsys.constructRHS(self.__Su, self.__phi) 
                    
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from fvm.numScheme import NumericalScheme
    
    class Test(NumericalScheme):
    
        def __init__(self, mesh, Su):
            super().__init__(mesh, Su)
            self.__name = 'Test'
        
        def source(self, phi):
            return self.Su * self.dx
        
        def calc(self, i):
            return 1, -2, 1
        
    from geo.line import Line
#
# Create a domain 
#
    N = 6
    rod = Line(0.5)
#
# We obtain a mesh from the domain
#
    malla = rod.constructMesh(N)
    vx = malla.vx+2
    ivx, _, _ = malla.bounds(bi = 1, ei = N-1)  
#    print(malla.hx)
#
# Create a scalar field for store the solution
#    
    T = np.zeros(vx)
    T[0] = 0
    T[-1] = 1
#
# Define the boundary conditions
# Esta función activa la corrección de los valores aW*, aP*, aE*, sp*, 
# según sea el caso.
#
    rod.boundaryConditions(dirichlet = {'RIGHT':T[-1],'LEFT':T[0]})
#
# The source (use only one of the two options)
#
    su = np.ones(ivx)
#    su = np.zeros(ivx)        
#
# Create a scheme test for testing
#
    scheme = Test(malla, su)
#
# Create a Partial Differential Equation
#    
    pde = PDE(rod, T)
#
# Define the elements of the PDE and solve it
#    
    pde.setNumericalScheme(scheme)
#    
# Durante la ejecución de la función solve(), se aplican las condiciones de
# frontera, en donde se corrigen los valores aW*, aP*, aE*, sp*, 
# de acuerdo con las BC.
#
    sol = pde.solve()
    pde.printMat(nice=True)
    pde.printRHS()
    print('su =', su)
#
# Graficamos la solución
#
    x,_,_ = malla.coordinatesMeshFVM()  
                                                  
    print(x)
    print(sol)
    import matplotlib.pyplot as plt
    plt.plot(x,sol,'o-', label='Test solution')
    plt.legend()
    plt.show()
#----------------------- TEST OF THE MODULE ----------------------------------   


    
    