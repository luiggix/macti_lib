#-----------------------------------------------------------
# Ruta biblioteca macti
#
#import os, sys
#sys.path.insert(0, os.path.abspath('../../'))
#print(sys.path)
#-----------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
 
def grafica(t,y,ye,ht,e):
    """
    Graficación del resultado de la aproximación del decaimiento radioactivo.
    """
    fig = plt.figure(figsize=(10,5))
    plt.plot(t, y, 'o-', lw=1.5, label = 'Aproximación')
    plt.plot(t, ye, '.-', label = 'Sol. analítica')
    plt.xlabel('Tiempo', fontsize=14)
    plt.ylabel('y(t)', fontsize=14)
    plt.ylim((-1,21))
    plt.title('ht = {:5.4},    ERROR = {:5.4}'.format(ht, e), loc='right', color='red', fontsize=14)
    plt.title('DECAIMIENTO RADIACTIVO'.format(e), loc='left', color='blue', fontsize=14)
    plt.legend(fontsize=14)
    plt.grid(ls='--', lw=0.5)
    ejes = plt.gca()
    ejes.spines['right'].set_visible(False)
    ejes.spines['top'].set_visible(False)
    plt.show()

def decaimiento(l = 1.5, a = 0.0, b = 10, y0 = 20.0, Nt = 10):
    """
    Cálculo del decaimiento radioactivo usando el Método de Euler hacia adelante.
    """
    λ = 1.5
    ht = (b-a) / Nt
    t = np.array([a + ht * n for n in range(0, Nt+1)])
    ye = y0 * np.exp(-l*t)
    
    # Arreglo para almacenar la solución
    y = np.zeros(Nt+1)

    # Condición inicial
    y[0] = y0

    # Función f(t,y) 
    f = lambda t, y : -λ * y 

    for n in range(0, Nt):
        y[n+1] = y[n] + ht * f(n * ht, y[n]) # Método de Euler hacia adelante

    # Calculo del error de la aproximación
    error = np.linalg.norm(y - ye, 2) / Nt
    
    grafica(t, y, ye, ht, error)

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
    decaimiento()
    print('hello')
