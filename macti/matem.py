import numpy as np

def eigen_land(Mat):
    # Cálculo de eigenvectores
    w, v = np.linalg.eig(Mat)  # w: eigenvalues, v: eigenvectors

    # Impresión de los eigenvalores y eigenvectores
    print('eigenvalores = {}'.format(w))
    print('eigenvectores:\n {} \n {}'.format(v[:,0], v[:,1]))

    # Cálculo del ángulo entre los vectores.
    e0 = v[:,0] / np.linalg.norm(v[:,0])
    e1 = v[:,1] / np.linalg.norm(v[:,1])
    angulo = np.arccos(np.dot(e0, e1)) * 180 / np.pi
    print('ángulo entre eigenvectores = {}'.format(angulo)) 
    
    return w, v

def print_Aulu(A, w, v):
    for i, l in enumerate(w):
        print(chr(119860) + chr(119906) + ' = {}'.format(A @ v[:,i]))
        print(chr(120582) + chr(119906) + ' = {}'.format(l * v[:,i]))
        print()