import numpy as np
import matplotlib.pyplot as plt
from macti import visual

ax = -3.0
bx = 3.0
ay = -3.0
by = 3.0
Nx = 21
Ny = 21
    
x = np.linspace(ax,bx,Nx+2)
y = np.linspace(ay,by,Ny+2)
visual.plotGrid(x,y)
plt.show()


