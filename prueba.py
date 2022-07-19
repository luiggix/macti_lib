from macti import evaluacion
import numpy as np
import sys
[print(i) for i in sys.path]

x = np.linspace(0,1500,10)
PA = 0.10 * x + 200
PB = 0.35 * x + 20

ruta = 'SistemasLineales'
d = evaluacion.Evalua(ruta)
d.verifica(PA, 1)
d.verifica(PB, 2)

