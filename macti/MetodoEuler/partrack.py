#-----------------------------------------------------------
# Ruta biblioteca macti
#
#import os, sys
#sys.path.insert(0, os.path.abspath('../../'))
#print(sys.path)
#-----------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from macti.visual import plotFlujo

def solveFlujo(Nt, ht, rango, w, dTray=True):
    # Campo de velocidad
    u = lambda x,r: 0.298*(0.5**2 - r**2)/(4*3.0*1.05e-3)  # Flujo de Poiseuille
    v = lambda x,r: np.sin(x*w)                      # La velocidad en dirección y es cero.

    # Número de partículas
    Np = 7

    # Coordenadas iniciales de las partículas
    px = np.zeros(Np)
    py = np.linspace(rango[0], rango[1], Np) # Equiespaciadas en dirección y

    t = np.zeros((Np, Nt,2))

    for j in range(0, Np):
        t[j, 0, :] = (px[j], py[j]) 

    for j in range(0,Np):
        (xi, yi) = t[j, 0, :] # Posición inicial de la trayectoria j
        for n in range(1, Nt): # Ciclo para calcular las posiciones
            ### BEGIN SOLUTION
            xf = xi + ht * u(xi,yi)
            yf = yi + ht * v(xi,yi)
            t[j, n, :] = (xf, yf)   # Agregamos (xf, yf) a la lista de posiciones
            (xi, yi) = (xf, yf)     # Actualizamos (xi, yi)
            ### END SOLUTION

    if dTray:
        for j in range(Np):
            plt.scatter([t[j,0,0], t[j,-1,0]], [t[j,0,1], t[j,-1,1]],  ec='k', s=50, alpha=0.75, zorder=5)
            plt.plot(t[j,:,0], t[j,:,1],'-', lw=2.0)
        plt.plot(t[:,:,0], t[:,:,1], '--k', lw=.5)
    
    L = 3.0     # Longitud del tubo
    R = 0.5     # Radio del tubo
    x = np.linspace(0,L,20)
    r = np.linspace(-R,R,20)
    xg, yg = np.meshgrid(x, r, indexing='ij', sparse=False)
    
    if w == 0.0:
        plotFlujo(xg, yg, u, v, 'quiver', '')
    else:
        plotFlujo(xg, yg, u, v, 'stream', '')

if __name__ == '__main__':

    solveFlujo(50, 0.01, [-0.3,-0.2], 5.0, True)
    plt.show()
