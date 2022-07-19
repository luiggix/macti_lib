import sys
[print(i) for i in sys.path]

import numpy as np
import matplotlib.pyplot as plt
from macti.SistemasLineales import statSolvers

A = np.matrix([[3, 2],[2,6]] )
b = np.array([2,-8])
    
sol, e, it, ea = statSolvers.jacobi(A,b,1e-5,100)
print('\n Jacobi \n Solucion: {} \n Error : {} \n Iteraciones : {}'.format(sol, e, it))
