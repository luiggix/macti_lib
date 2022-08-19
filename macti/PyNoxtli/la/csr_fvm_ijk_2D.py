#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on jue abr  2 13:58:15 CST 2020]
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../')) 
#-----------------------------------------------------------

import numpy as np

class CSR_FVM_ijk_2D():
    """A matriz stored in CSR (Compressed Sparse Row) format.
    
    Attributes
    ----------
    __bi : int
        Índice sobre la malla donde inician los cálculos en el eje x.
    __ei : int
        Índice sobre la malla donde terminan los cálculos en el eje x.
    __bj : int
        Índice sobre la malla donde inician los cálculos en el eje y.
    __ej : int
        Índice sobre la malla donde terminan los cálculos en el eje y.
    __NTx : int
        Número total de incógnitas en el eje x.
    __NTy : int
        Número total de incógnitas en el eje y.
    __NTx : int
        Número total de incógnitas en el eje x.
    __N : int
        Número total de incógnitas en todo el dominio.
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
    
    def __init__(self, bi, ei, bj, ej):
        """Inicializa los atributos para el almacenamiento en el formato CSR."""
        self.__bi = bi
        self.__ei = ei
        self.__bj = bj
        self.__ej = ej
        self.__NTx = ei - bi + 1
        self.__NTy = ej - bj + 1
        self.__Nd = 5
        self.__N = self.__NTx * self.__NTy
        self.__Nzeros = self.__Nd * self.__N
        self.__AA = np.zeros(self.__Nzeros)
        self.__JA = np.zeros(self.__Nzeros, dtype=int)
        self.__IA = np.zeros(self.__N + 1, dtype=int)
        
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
        
    @property
    def NTx(self):
        return self.__NTx

    @property
    def NTy(self):
        return self.__NTy
    
    @property
    def Nd(self):
        return self.__Nd   

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
        bj = self.__bj
        ej = self.__ej
        NTx = self.__NTx
        NTy = self.__NTy
        Nd = self.__Nd
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
# como se ve en el siguiente diagrama: 
# (S -> aS, W -> aW, P -> aP, E -> aE, N -> aN):
#-----------+
# S W P E N |
# S W P E N |
# S W P E N |
# ...       
# S W P E N |
# S W P E N |
#-----------+    
        for i in range(bi,ei+1):
            for j in range(bj,ej+1):
            #
            # La función calc(i) regresa los coeficientes de FVM calculados
            # con base en los índices de la malla (i,j). Este cálculo se hace
            # usando un esquema numérico determinado (scheme).
            #            
                val = scheme.calc(i,j)

                AA[I] = val[0] #aS(i,j)
                JA[I] = irow - NTx
                
                I += 1 
                AA[I] = val[1] #aW(i,j)
                JA[I] = irow - 1
                
                I += 1 
                AA[I] = val[2] #aP(i,j)
                JA[I] = irow
                
                I += 1
                AA[I] = val[3] #aE(i,j)
                JA[I] = irow + 1
                
                I += 1
                AA[I] = val[4] #aN(i,j)
                JA[I] = irow + NTx
        
                # Llena el arreglo IA
                I += 1
                irow += 1
                IA[irow] = I 
#
# Lo siguiente es para evitar salirnos del rango en algunos bloques: 
#
# Corregimos en aW y aE en el primer y último renglón, respectivamente,
# de cada bloque.
#
        OFFSET_X = Nd * NTx
        for j in range(NTy):
            I = j * OFFSET_X
            JA[I+1] = 0 # aW
            I += OFFSET_X
            JA[I-2] = 0 # aE
#
# Corregimos en aS y aN en cada renglón del primer y último bloque, 
# respectivamente.
#
        OFFSET_Y = (NTx * (NTy - 1) + 1) * Nd
        for i in range(NTx):
            I = i * Nd
            JA[I] = 0 # aS
            I += OFFSET_Y
            JA[I-1] = 0 # aN
            
        return True

    def correct(self):
#    
# Corrige el primer y último bloque de la matriz.
#-----------+
# 0 W P E N |
# 0 W P E N |  FIRST BLOCK
# 0 W P E N |
#-----------
# ...   
#-----------
# S W P E 0 |
# S W P E 0 |  LAST BLOCK
# S W P E 0 |
#-----------+
# Pone zeros en los lugares correspondientes a aS y aN.
#        
        AA = self.__AA
        NTx = self.__NTx
        NTy = self.__NTy
        Nd = self.__Nd

        OFFSET_X = Nd * NTx
        for j in range(NTy):
            I = j * OFFSET_X
            AA[I+1] = 0 # aW
            I += OFFSET_X
            AA[I-2] = 0 # aE
#
# Corrige el primer y último bloque de cada renglón.
#-----------
# S * P E N |
# S W P E N | ANY BLOCK
# S W P * N |
#-----------+
# Pone zeros en los lugares correspondientes a aW y aE.
#
        OFFSET_Y = (NTx * (NTy - 1) + 1) * Nd
        for i in range(NTx):
            I = i * Nd
            AA[I] = 0 # aS
            I += OFFSET_Y
            AA[I-1] = 0 # aN
    
        return True

    def printMat(self, nice = False):
        AA = self.__AA
        JA = self.__JA
        IA = self.__IA
        N = len(IA)-1
        if not(nice):
            I = 0
            print('-' * 52)
            print('|{:>3} | {:>3} | {:>5} | {:>5} {:>5} {:>5} {:>5} {:>5} |'.format('I','IA','','S','W','P','E','N'))
            print('-' * 52)
            for i in range(0,N):
                print('|{:>3} | {:>3} | AA -> | {:>5} {:>5} {:>5} {:>5} {:>5} |'.format(i, IA[i], AA[I], AA[I+1], AA[I+2], AA[I+3], AA[I+4]))
                print('|{:>3} | {:>3} | JA -> | {:>5} {:>5} {:>5} {:>5} {:>5} |'.format(i, IA[i], JA[I], JA[I+1], JA[I+2], JA[I+3], JA[I+4]))
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

    from utils.displayInfo import printInfo

    class Test():

        def calc(self, i, j):
            return -1, -1, 4, -1, -1

# --------------- TEST 1 ---------------
    Nx = 3
    Ny = 3
    bi = 1
    ei = Nx
    bj = 1
    ej = Ny
    
    test_scheme = Test()
#
# Construct a CSR_FVM_ijk matrix
#
    A = CSR_FVM_ijk_2D(bi, ei, bj, ej)    
    A.construct(test_scheme)
    A.correct() # Esta función se usa para corregir algunos valores
                # En las aplicaciones esta función es sustitutida por aquella que
                # calcula las condiciones de frontera.
    A.printMat(nice=False)

# --------------- TEST 1 ---------------

    Nx = 4
    Ny = 4
    bi = 1
    ei = Nx
    bj = 1
    ej = Ny
    
    test_scheme = Test()
#
# Construct a CSR_FVM_ijk matrix
#
    A = CSR_FVM_ijk_2D(bi, ei, bj, ej)    
    A.construct(test_scheme)
    A.correct() # Esta función se usa para corregir algunos valores
                # En las aplicaciones esta función es sustitutida por aquella que
                # calcula las condiciones de frontera.
    A.printMat(nice=True)

    from scipy.sparse import csr_matrix
#
# construct a CSR matrix from scipy using the arrays from CSR_FVM_ijk matrix    
#
#    print('IA = ', A.IA)
    B = csr_matrix((A.AA, A.JA, A.IA))
#    
# Now matrices A and B share the memory.
#
#    B[1,1] = 3
#    A.printMat(nice=True)
#    print(B)
#    
# We can solve the system using scipy algorithms for sparse matrices
#
    import scipy.sparse.linalg as spla
#
# first we define the RHS of the system.
#
    b = np.ones(Nx * Ny)
    print(b)
#    
# Now we solve the system using CG 
#
    sol = spla.cg(B,b)[0]
    
    print(sol)
    
    x, y = np.meshgrid(np.linspace(0,1,Nx), np.linspace(0,1,Ny))
    sol.shape = (Nx,Ny)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    surf = ax.plot_surface(x,y,sol, cmap='coolwarm')
    fig.colorbar(surf, shrink=0.5, aspect=5)
#    plt.legend()
    plt.show()
#----------------------- TEST OF THE MODULE ----------------------------------   

    
    
    
    