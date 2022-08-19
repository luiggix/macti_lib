#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on mar mar 31 11:02:43 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../')) 
#-----------------------------------------------------------

import numpy as np

class CSR_FVM_ijk_1D():
    """A matriz stored in CSR (Compressed Sparse Row) format.
    
    Attributes
    ----------
    __bi : int
        Índice sobre la malla donde inician los cálculos.
    __ei : int
        Índice sobre la malla donde terminan los cálculos.
    __NTx : int
        Número total de incógnitas en el eje x.
    __Nd : int
        Número de diagonales en la matriz.
    __Nzeros : int
        Número total (aproximado) de elementos diferentes de cero en la matriz.
    __AA : array-like
        Arreglo que contiene los valores distintos de cero del formato CSR.
    __JA : array-like
        Arreglo que indica la columna del valor distinto de cero del formato CSR.
    __IA : array-like
        Arreglo que indica el inicio de cada renglón dentro del arreglo JA del formato CSR.
    
    """
    
    def __init__(self, bi, ei):
        """
        Inicializa los atributos para el almacenamiento en el formato CSR.

        Parameters
        ----------
        bi : int
            Índice sobre la malla donde inician los cálculos.
        ei : int
            Índice sobre la malla donde terminan los cálculos.

        Notes
        -----
        Relación entre la Mesh y la Matrix:
            
        Boundary                                 Boundary     
           |                                       |
           +---o---+---o---+---o---+---o---+---o---+
               1       2       3       4       5
              bi                              ei
            
        En este ejemplo bi = 1, ei = 5.
        
                                      1 2 3 4 5
                                    +-----------
                                  1 | * * 0 0 0  
                                  2 | * * * 0 0  
        Matrix N x N (5 x 5) -->  3 | 0 * * * 0  
                                  4 | 0 0 * * * 
                                  5 | 0 0 0 * * 
                                  
        NTx = 5 - 1 + 1 = 5
        Nzeros = Nd * NTx = 3 * 5 = 15
        
        * | * * 0 0 0 | 
          | * * * 0 0 | 
          | 0 * * * 0 |   Transformed into --> AA
          | 0 0 * * * |                      
          | 0 0 0 * * | *                   
                                              
        --> AA = [ * * * |  * * * | * * * | * * * | * * * |] 
                                  
        """
        self.__bi = bi
        self.__ei = ei
        self.__NTx = ei - bi + 1
        self.__Nd = 3
        self.__Nzeros = self.__Nd * self.__NTx
        self.__AA = np.zeros(self.__Nzeros)
        self.__JA = np.zeros(self.__Nzeros, dtype=int)
        self.__IA = np.zeros(self.__NTx + 1, dtype=int)
        

    @property
    def AA(self):
        """Regresa el arreglo de valores diferentes de cero de la matriz."""
        return self.__AA

    # @AA.setter
    # def AA(self, AA):
    #     self.__AA = AA
        
    @property    
    def JA(self):
        """Regresa el arreglo con los índices de las columnas de los valores no cero."""
        return self.__JA

    # @JA.setter
    # def JA(self, JA):
    #     self.__JA = JA
        
    @property    
    def IA(self):
        """Regresa el arreglo con los índices de las renglones."""
        return self.__IA

    # @IA.setter    
    # def IA(self, IA):
    #     self.__IA = IA
    
    def construct(self, scheme):
        """
        Calcula los coeficientes de la matriz y los almacena en formato CSR.
        
        Note
        ----
        Esta función no toma en cuenta las condiciones de frontera, por lo
        tanto, algunos valores en los arreglos AA y JA pueden no ser correctos.
        Estas condiciones dependen del dominio y el esquema de discretización,
        por lo que serán otras clases encargadas de corregir esto. Mientras
        tanto, solo se agregan ceros en los lugares donde estas condiciones de
        frontera deben ir.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
            
        """
        bi = self.__bi
        ei = self.__ei
        AA = self.__AA
        JA = self.__JA
        IA = self.__IA
#
# Compressed Sparse Row (CSR) or Compressed Row Storage (CRS)
#
        I = 0
        irow = 0
        IA[irow] = I
#
# Llena la matriz con todas las diagonales consideradas del mismo tamaño
# como se ve en el siguiente diagrama (W -> aW, P -> aP, E -> aE):
#--------+
# W P E |
# W P E |
# W P E |
# ...
# W P E |
# W P E |
#--------+
        for i in range(bi,ei+1):
            #
            # La función calc(i) regresa los coeficientes de FVM calculados
            # con base en el índice de la malla (i). Este cálculo se hace
            # usando un esquema numérico determinado (scheme).
            #
            val = scheme.calc(i) # Regresa una tupla: (aW, aP, aE)

            AA[I] = val[0] # aW(i)
            JA[I] = irow - 1
            
            I += 1 
            AA[I] = val[1] #aP(i)
            JA[I] = irow
        
            I += 1
            AA[I] = val[2] #aE(i)
            JA[I] = irow + 1
        
            # Llena el arreglo IA
            I += 1
            irow += 1
            IA[irow] = I   
#
# Lo siguiente es para evitar salirnos del rango en el primer y último renglón: 
#
        JA[ 0] = 0 # First row   
        JA[-1] = 0 # Last row
            
        return True

    def correct(self):
        """
        Corrige los índices en JA y los valores correspondientes en AA.
        
        Note
        ----
        Esta función debería ser ejecutada justo después de construct() para
        tomar en cuenta las condiciones de frontera.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
        
        """
        AA = self.__AA
        JA = self.__JA
#
# Corrige el primer y último renglón de la matriz:
#-----------
# * P E |
# W P E | ANY BLOCK
# W P * |
#-----------+
# Pone zeros en los lugares correspondientes a aW y aE.
#
# LEFT WALL
        AA[0] = 0 # W
#
# RIGTH WALL
#
        AA[-1] = 0 # E
        
        return True
    
    def printMat(self, nice = False):
        """Print the information stored in matriz format or the CSR arrays.
        
        """
        AA = self.__AA
        JA = self.__JA
        IA = self.__IA
        N = len(IA)-1
        if not(nice):
            I = 0
            print('-' * 52)
            print('|{:>3} | {:>3} | {:>5} | {:>5} {:>5} {:>5} |'.format('I','IA','','W','P','E'))
            print('-' * 52)
            for i in range(0,N):
                print('|{:>3} | {:>3} | AA -> | {:>5} {:>5} {:>5} |'.format(i, IA[i], AA[I], AA[I+1], AA[I+2]))
                print('|{:>3} | {:>3} | JA -> | {:>5} {:>5} {:>5} |'.format(i, IA[i], JA[I], JA[I+1], JA[I+2]))
                print('-' * 52)
                I += self.__Nd
        else:
            AT = np.zeros((N,N))
            for i in range(0,N):
                for j in range(IA[i],IA[i+1]):
                    AT[i,JA[j]] = AA[j]
            print(AT)

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    from macti.PyNoxtli.utils.displayInfo import printInfo

    class Test():

        def calc(self, i):
            return -1, 2, -1
    
    Nx = 5
    bi = 1
    ei = Nx
    
    test_scheme = Test()
#
# Construct a CSR_FVM_ijk matrix
#
    A = CSR_FVM_ijk_1D(bi, ei)    
    A.construct(test_scheme)
    A.correct() # Esta función se usa para corregir algunos valores
                # En las aplicaciones esta función es sustitutida por aquella que
                # calcula las condiciones de frontera.
    A.printMat(nice=False)

    printInfo(AA = A.AA,
              JA = A.JA,
              IA = A.IA)
    
    A.printMat(nice=True)
    
    from scipy.sparse import csr_matrix
#
# Construct a CSR matrix from scipy using the arrays from CSR_FVM_ijk matrix    
#
    B = csr_matrix((A.AA, A.JA, A.IA))
#    
# Now matrices A and B share the memory.
#
#    B[1,1] = 3
#    A.printMat(nice=True)
    print(B)

#    
# We can solve the system using scipy algorithms for sparse matrices
#
    import scipy.sparse.linalg as spla
#
# first we define the RHS of the system.
#
    b = np.ones(ei-bi+1)
    b[0] = 0
    b[-1] = 0
    print(b)
#    
# Now we solve the system using CG 
#
    sol = spla.cg(B,b)[0]
    
    print(sol)
    
    x = np.linspace(0,1,5)
    import matplotlib.pyplot as plt
    plt.plot(x,sol,'o-', label='Test solution')
    plt.legend()
    plt.show()
#----------------------- TEST OF THE MODULE ----------------------------------   

    
    
    
    