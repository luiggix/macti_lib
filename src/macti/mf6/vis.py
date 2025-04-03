import numpy as np # Manejo de arreglos numéricos multidimensionales
import matplotlib.pyplot as plt # Graficación

# Biblioteca y módulos de flopy
from flopy.plot.styles import styles

def plot(ax, x, y, **par):
    with styles.USGSPlot():
        plt.rcParams['font.family'] = 'DeJavu Sans'
        ax.plot(x, y, **par)

def scatter(ax, x, y, **par):
    with styles.USGSPlot():
        plt.rcParams['font.family'] = 'DeJavu Sans'
        ax.scatter(x, y, **par)

if __name__ == '__main__':
    x = np.linspace(0,2*np.pi,100)
    y = np.sin(4*x)
    plt.figure(figsize=(10, 3))
    plot1D(plt.gca(), x, y)

    

