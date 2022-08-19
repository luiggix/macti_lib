#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Luis M. de la Cruz [Updated on jue abr  2 10:45:02 CST 2020].

Ejemplo 4.1 de (Versteeg & Malalasekera, 2007) 

Referencia:
@book{versteeg2007introduction,
  title={An Introduction to Computational Fluid Dynamics: The Finite Volume Method},
  author={Versteeg, H.K. and Malalasekera, W.},
  isbn={9780131274983},
  lccn={95006736},
  url={https://books.google.com.mx/books?id=RvBZ-UMpGzIC},
  year={2007},
  publisher={Pearson Education Limited}

}
"""
#-----------------------------------------------------------
# PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
#import os, sys
#if not("/base" in sys.path[0][-5:]):
#    sys.path.insert(0, os.path.abspath('../../base'))
#-----------------------------------------------------------

import numpy as np
#
# Importar módulos de pynoxtli
#
from macti.PyNoxtli.geo.line import Line
from macti.PyNoxtli.fvm.sDiffusion import sDiffusion1D
from macti.PyNoxtli.fvm.pde import PDE
from macti.PyNoxtli.utils.displayInfo import printInfo
import macti.PyNoxtli.vis.flowix as flx
#
# Datos del problema
#
longitud = 0.5 # metros
TA = 100       # °C 
TB = 500       # °C 
k  = 1000      # W/m.K
N  = 6         # Número de nodos
#
# Definición del dominio y condiciones de frontera
#
barra = Line(longitud)
barra.boundaryConditions(dirichlet = {'LEFT':TA, 'RIGHT':TB})
#
# Creamos la malla y obtenemos datos importantes
#
malla     = barra.constructMesh(N) # Se construye el objeto para la malla
ivx, _, _ = malla.bounds(bi = 1, ei = N-1) # Grados de libertad
nx        = malla.nx    # Número de nodos
nvx       = malla.vx    # Número de volúmenes
delta     = malla.dx    # Tamaño de los volúmenes
#
# Se construye el arreglo donde se guardará la solución
#
T = np.zeros(nvx+2) # El arreglo contiene ceros inicialmente
T[0]  = TA          # Condición de frontera izquierda
T[-1] = TB          # Condición de frontera derecha
#
# Imprimimos los datos del problema
#
printInfo(Longitud = longitud,
          Temperatura_A = TA,
          Temperatura_B = TB,
          Conductividad = k,
          Nodos = nx, 
          Volúmenes = nvx,
          Delta = delta)
#
# Definimos la fuente 
#
S = np.zeros(ivx)  # Por ahora no hay fuente.
#
# Definimos el esquema de disccretización
#
dif_scheme = sDiffusion1D(malla, S, k)
#
# Definimos la ecuación a resolver
#
laplace = PDE(barra, T)
#
# Creamos el sistema lineal y lo resolvemos
#
laplace.setNumericalScheme(dif_scheme)
laplace.solve()
print(T)
#
# Solución analítica
#
x, _, _ = malla.coordinatesMeshFVM()
Ta = 800 * x + 100
#
# Visualización
#
# Parámetros para los ejes. Se van a definir 3 cojuntos de ejes (Axes) y cada
# uno de ellos tiene parámetros diferentes. 
#
axis_par = [{'title':'Numérica', 'xlabel':'x [m]', 'ylabel':'T [$^o$C]'},
            {'title':'Exacta', 'xlabel':'x [m]', 'ylabel':'T [$^o$C]'},
            {'title':'Malla 1D'}]
#
# Definición de un canvas para graficar los resultados
# 
v = flx.Plotter(3,1,axis_par) # Son 3 renglones y una columna de ejes (Axes).
#
# En los primeros ejes graficamos la solución numérica.
#
v.plot(1,x,T, {'marker':'o', 'ls':'-', 'label':'Numérica'})
#
# En los segundos ejes graficamos la solución exacta para comparación.
#
v.plot(2,x,Ta, {'marker':'s', 'ls':'-', 'color':'orange', 'label':'Exacta'})
#
# En los terceros ejes graficamos la malla del dominio.
#
v.plot_mesh(3, malla, label=True)
#
# Si hubiera leyendas en las graicas, se despliegan con la siguiente instrucción.
#
v.legend([1,2,3], par={'ncol':2})
#
# Se muestran las gráficas.
#
v.show()
