# Desde el .[nombre del archivo] importa [lista de funciones] 
from .matem import eigen_land, print_eigen

# que nombres se exportan si se usa from macti.matem import * 
__all__ = ["eigen_land", "print_eigen"]
