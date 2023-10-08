"""
@author: Luis M. de la Cruz [Updated on mié 18 ene 2023 14:07:31 CST].
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cycler import cycler

# Personalización de las gráficas
#-----------------------------------------
grey_label_color = 75/255
grey_title_color = 25/255
label_color = [grey_label_color, grey_label_color, grey_label_color]
title_color = [grey_title_color, grey_title_color, grey_title_color]

mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['figure.figsize'] = (6.4, 4.8)
mpl.rcParams['font.weight'] = 'light'
mpl.rcParams['font.size'] = 12
mpl.rcParams['axes.facecolor'] = 'whitesmoke'
mpl.rcParams['axes.edgecolor'] = 'gray'   # axes edge color
mpl.rcParams['axes.linewidth'] = 0.8     # edge line width
mpl.rcParams['axes.labelcolor'] = label_color
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['axes.spines.left'] = True  # display axis spines
mpl.rcParams['axes.spines.bottom'] = True
mpl.rcParams['axes.spines.top'] =   False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.titlelocation'] = 'left'
mpl.rcParams['axes.titlesize'] = 14
mpl.rcParams['axes.titlecolor'] = title_color
mpl.rcParams['axes.titley'] = 1.02
colors = [[25/255, 118/255, 210/255], # blue
          [245/255, 124/255, 0/255],  # orange
          [56/255, 142/255, 60/255],  # green
          [194/255, 24/255, 91/255],  # red
          [123/255, 31/255, 162/255], # purple
          [161/255, 136/255, 127/255],   # brown
          [240/255, 98/255, 146/255], # pink
          [97/255, 97/255, 97/255  ], # gray
          [175/255, 180/255, 43/255], # olive
          [79/255, 195/255, 247/255], # cyan  
        ]
mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)
mpl.rcParams['lines.linewidth'] = 1.5
#-----------------------------------------

class Plotter():
    """
    Gestor de figuras y despliegue.
    
    Crea una figura de matplotlib y en ella agrega subplots ordenados en un
    arreglo de tamaño rows x cols.
    
    Attributes
    ----------
    __fig : Figure
        La figura 
    __ax : Axes list
        Lista de ejes de cada subplot.
    __nfigs : int
        Número total de subplots.
    
    Methods
    -------
    colorbar()
        Crea una barra de color.
    plot()
        Crea gráficas XY.
    scatter()
        Despliega puntos dispersos.
    imshow()
        Despliega un mapa de color.
    contour()
        Despliega líneas de contornos.
    contourf()
        Despliega contornos llenos.
    streamplot()
        Despliega líneas de corriente.
    quiver()
        Despliega flechas de un campo vectorial.
    plot_mesh()
        Despliega una malla en 1D y 2D.
    animate()
        Realiza animaciones.
    
    """
    
    def __init__(self, rows = 1, cols = 1, 
                 axis_par = None, 
                 fig_par={}, 
                 title_par={}, title = ''):
        """
        Crea e inicializa una figura de matplotlib.

        Parameters
        ----------
        rows : int, opcional
            Número de renglones del arreglo de subplots. The default is 1.
        cols : int, opcional
            Número de columnas del arreglo de subplots. The default is 1.
        axis_par : list of dicts, opcional
            Lista de diccionarios; cada diccionario define los parámetros que 
            se usarán decorar los `Axes` de cada subplot. The default is None.
        fig_par : dict, opcional
            Diccionario con los parámetros para decorar la figura. 
            The default is {}.
        title_par: dict, opcional
        Diccionario con los parámetros para el título de la figura.

        """
        self.__fig = plt.figure(**fig_par)        
        self.__fig.suptitle(title, **title_par)
        self.__nfigs =  rows * cols

        # Parametros para cada conjunto de ejes
        if axis_par != None:
            # Cuando se pasan parámetros para los ejes, checamos
            # cuántos son y determinamos los que faltan (Nfill)
            Nfill = self.__nfigs - len(axis_par)
        else:
            # Cuando no se pasan parámetros solo tenemos una lista vacía.
            Nfill = self.__nfigs
            axis_par = [ ]
            
        # Al final de la lista axis_par agregamos los diccionarios que
        # faltan (Nfill).
        [axis_par.append({}) for n in range(Nfill)]
            
        # Generamos las subgráficas con sus parámetros correspondientes.
        self.__ax = [plt.subplot(rows, cols, n, **axis_par[n-1]) for n in range(1,self.__nfigs + 1)]
        
        plt.tight_layout()
 
    @property
    def fig(self):
        """
        Regresa un objeto de tipo `Figure`.
        
        Returns
        -------
        Figure
            La figura gestionada por el objeto de tipo Plotter.
            
        """
        return self.__fig
    
    def figtitle(self, title, title_par = {}):
        """
        Agrega un título para toda la figura.
        
        Parameters
        ----------
        title: string
        Cadena del título.
        
        title_par: dict
        Parámetros para el texto del título.
        """
        self.__fig.suptitle(title, **title_par)

    
    def axes(self, n = 1):
        """
        Regresa un objeto de tipo `Axes` que son los ejes del subplot[n].

        Parameters
        ----------
        n : int, opcional
            Número del subplot que se desea obtener (1, nfigs). The default is 1.

        Returns
        -------
        Axes
            Los ejes del subplot[n].

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.axes(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        return self.__ax[n-1]   
    
    def set_canvas(self, n, Lx, Ly, par=None):
        """
        Configura un lienzo para hacer las gráficas más estéticas.

        Parameters
        ----------
        ax: axis
        Son los ejes que se van a configurar.

        Lx: float
        Tamaño del dominio en dirección x.

        Ly: float
        Tamaño del dominio en dirección y.

        Returns
        -------
        cax: axis
        Eje donde se dibuja el mapa de color.
        """
        ax = self.__ax[n-1]
        
        lmax = max(Lx,Ly)
        offx = lmax * 0.010
        offy = lmax * 0.010
        ax.set_xlim(-offx, Lx+offx)
        ax.set_ylim(-offy, Ly+offy)
        ax.grid(False)
        ax.spines[:].set_visible(False)

        facecolor = self.__fig.get_facecolor()
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        cax.set_xticks([])
        cax.set_yticks([])
        cax.spines['bottom'].set_visible(False)
        cax.spines['left'].set_visible(False)
        cax.set_facecolor(facecolor)
    
        return cax

    def format_func(self, value, tick_number):
        # find number of multiples of pi/2
        N = int(np.round(2 * value / np.pi))
        if N == 0:
            return "0"
        elif N == 1:
            return r"$\frac{\pi}{2}$"
        elif N == 2:
            return r"$\pi$"
        elif N % 2 > 0:
            if N == -1:
                return r"$-\frac{\pi}{2}$"
            elif N == 1:
                return r"$-\frac{\pi}{2}$"
            else:
                return r"${}$".format(N) + r"$\frac{\pi}{2}$"
        else:          
            return r"${}$".format(N // 2) + r"$\pi$"

    def set_ticks(self, ax, xticks = [], yticks = [], trig = False):
        if trig:
            ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
            ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
            ax.xaxis.set_major_formatter(plt.FuncFormatter(self.format_func))
        else:        
            if len(xticks) != 0:
                ax.set_xticks(xticks)
            if len(yticks) != 0:
                ax.set_yticks(yticks)
            
    def set_coordsys(self, n = 1, 
                     xlabel='$x$', ylabel='$y$',
                     xlabelsize=8, ylabelsize=8,
#                     xtuple = None, ytuple = None,
                     trig = False):
        ax = self.__ax[n-1]
        # Move the left and bottom spines to x = 0 and y = 0, respectively.
        ax.spines[["left", "bottom"]].set_position(("data", 0))
        # Hide the top and right spines.
        ax.spines[["top", "right"]].set_visible(False)

        # Draw arrows (as black triangles: ">k"/"^k") at the end of the axes.  In each
        # case, one of the coordinates (0) is a data coordinate (i.e., y = 0 or x = 0,
        # respectively) and the other one (1) is an axes coordinate (i.e., at the very
        # right/top of the axes).  Also, disable clipping (clip_on=False) as the marker
        # actually spills out of the axes.
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        ax.set_xlabel(xlabel, rotation=0, labelpad=-35.0, x = 0.98)
        ax.set_ylabel(ylabel, loc = 'top', rotation=0, labelpad=-45.0)
        ax.xaxis.set_tick_params(labelsize=xlabelsize)
        ax.yaxis.set_tick_params(labelsize=ylabelsize)
        
#        if isinstance(xtuple, tuple) and isinstance(ytuple, tuple):
#            xticks = np.linspace(xtuple[0],xtuple[1],xtuple[2]) 
#            yticks = np.linspace(ytuple[0],ytuple[1],ytuple[2]) 
#        else:
#            xticks = ax.get_xticks()
#            yticks = ax.get_yticks()
#        self.set_ticks(ax, xticks, yticks, trig)
        
    
#
#----------------------- Methods applied to all subplots  ----------------------------   
#
    def tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None):
        """
        Ejecuta la función matplotlib.pyplot.tight_layout.

        See Also
        --------
        matplotlib.pyplot.tight_layout().

        """
        plt.tight_layout()#pad, h_pad, w_pad, rect = None)
        
    def show(self):
        """
        Muestra las gráficas de cada subplot.
        
        See Also
        --------
        matplotlib.pyplot.show().
        
        """
        plt.show()
    
        
    def grid(self, nlist = [], par = None):
        """
        Despliega el grid de uno o todos los subplots.

        Parameters
        ----------
        nlist : list, opcional
            Si no se define, entonces se muestran los grids de todos los 
            subplots. Si se da una lista, sus valores deben estar en (1,nfigs) y
            se mostrará el grid de cada subplot[n].
        par : dict, opcional
            Diccionario con los parámetros para decorar el grid. The default is None.

        See Also
        --------
        matplotlib.axes.Axes.grid().

        """
        if len(nlist):
            for n in nlist:
                assert (n >= 1 and n <= self.__nfigs), \
                "Plotter.grid(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
                if par != None:
                    self.__ax[n-1].grid(**par)
                else:
                    self.__ax[n-1].grid()
        else:
            if par != None:
                [self.__ax[n].grid(**par) for n in range(0,self.__nfigs)]
            else:
                [self.__ax[n].grid() for n in range(0,self.__nfigs)]
                
    def legend(self, nlist = [], **par):
        """
        Muestra las leyendas de todos los subplots, si están definidos.

        Parameters
        ----------
        nlist : list, opcional
            Si no se define, entonces se muestran las leyendas de todos los 
            subplots. Si se da una lista, sus valores deben estar en (1,nfigs) y
            se mostrarán las leyendas de cada subplot[n].        
        par : dict, opcional
            Diccionario con los parámetros para decorar las leyendas. 
            The default is None.

        Returns
        -------
        None.
        
        See Also
        --------
        matplotlib.axes.Axes.legend().

        """
        if len(nlist) > 0:
            for n in nlist:
                assert (n >= 1 and n <= self.__nfigs), \
                "Plotter.legend(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
                if par != None:
                    self.__ax[n-1].legend(**par)
                else:
                    self.__ax[n-1].legend()
        else:
            [self.__ax[n].legend(**par) for n in range(0,self.__nfigs)]        
            
#
#----------------------- Methods to draw a specific kind of plot -------------   
#        
    def plot(self, n, data1, data2, **par):
        """
        Dibuja una línea que pasa a través de un conjunto de puntos en 2D.

        Los puntos se pueden presentar conectados en la gráfica usando 
        diferentes tipos de línea o se pueden mostrar solo los puntos. Esta
        función no permite cambiar el tamaño de los puntos.
        
        Parameters
        ----------
        n : int
            Subplot donde se dibujará la línea.
        data1 : array-like
            Coordenadas x.
        data2 : array-like
            Coordenadas y.
        **par : opcional
            Parámetros para decorar la línea.

        Returns
        -------
        out : list of Linea2D
            Lista de objetos de tipo `Line2D` que representan la línea.

        See Also
        --------
        matplotlib.axes.Axes.plot().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
        out = self.__ax[n-1].plot(data1, data2, **par)
          
        return out

    def scatter(self, n, data1, data2, **par):
        """
        Dibuja puntos dispersos, no conectados.
        
        Los puntos se dibujan sin conexión entre ellos y es posible modificar
        el tamaño de los marcadores de cada punto.

        Parameters
        ----------
        n : int
            Subplot donde se dibujará los puntos.
        data1 : array-like
            Coordenadas x.
        data2 : array-like
            Coordenadas y.
        par : opcional
            Parámetros para decorar los puntos. 

        Returns
        -------
        out : PathCollection
        
        See Also
        --------
        matplotlib.axes.Axes.scatter().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.scatter(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
        out = self.__ax[n-1].scatter(data1, data2, **par)
        
        return out

    def draw_domain(self, n, xg, yg, lw = 0.5, color = 'k', fontsize=10):
        """
        Dibuja el recuadro de la malla.

        Parameters
        ---------
        ax: axis
        Son los ejes donde se dibujará la malla.

        xn: np.array
        Coordenadas en x de la malla.

        yn: np.array
        Coordenadas en y de la malla.
        """
        ax = self.__ax[n-1]

        xn = xg[:,0]
        yn = yg[0,:]

        self.plot_frame(n, xg, yg, lw = 0.5, color = 'k')
            
        Lx = xn[-1] - xn[0]
        Ly = yn[-1] - yn[0]
        xoffset = Lx * 0.2
        yoffset = Ly * 0.2  
        offset = min(xoffset, yoffset)
        
        ax.text(xn[-1] * 0.5, 1.25 * offset, '$Lx$', fontsize=fontsize) 
        ax.text(1.25 * offset, yn[-1] * 0.5, '$Ly$', fontsize=fontsize) 
        
        ax.annotate('', xy=(0,offset), xytext=(Lx,offset),
                     arrowprops=dict(arrowstyle='<->'))
        ax.annotate('', xy=(offset,0), xytext=(offset,Ly),
                     arrowprops=dict(arrowstyle='<->'))
        
    def plot_frame(self, n, xg, yg, lw = 0.5, color = 'k', ticks=True, fontsize=10):
        """
        Dibuja el recuadro de la malla.

        Paramters
        ---------
        ax: axis
        Son los ejes donde se dibujará la malla.

        xn: np.array
        Coordenadas en x de la malla.

        yn: np.array
        Coordenadas en y de la malla.
        """
        ax = self.__ax[n-1]
        
        xn = xg[:,0]
        yn = yg[0,:]

        if ticks:
            ax.set_xticks([xn[0],xn[-1]], labels=[xn[0],xn[-1]], fontsize=fontsize)
            ax.set_yticks([yn[0],yn[-1]], labels=[yn[0],yn[-1]], fontsize=fontsize)
        
        # Dibujamos dos líneas verticales
        ax.vlines(xn[0], ymin=yn[0], ymax=yn[-1], lw = lw, color=color)
        ax.vlines(xn[-1], ymin=yn[0], ymax=yn[-1], lw = lw, color=color)

        # Dibujamos dos líneas horizontales
        ax.hlines(yn[0], xmin=xn[0], xmax=xn[-1], lw = lw, color=color)
        ax.hlines(yn[-1], xmin=xn[0], xmax=xn[-1], lw = lw, color=color)
    
    def plot_mesh2D(self, n, xg, yg, meshon = True, nodeson = False):
        """
        Dibuja la malla del dominio.
    
        Parameters
        ---------
        ax: axis
        Son los ejes donde se dibujará la malla.
    
        xn: np.array
        Coordenadas en x de la malla.
    
        yn: np.array
        Coordenadas en y de la malla.
        """
        ax = self.__ax[n-1]

        xn = xg[:,0]
        yn = yg[0,:]

        ax.set_xticks([])
        ax.set_yticks([])
        
        if meshon:
            # Dibujamos todas las líneas verticales de la malla
            for xi in xn:
                ax.vlines(xi, ymin=yn[0], ymax=yn[-1], lw=0.5, color='darkgray')

            # Dibujamos todas las líneas horizontales de la malla
            for yi in yn:
                ax.hlines(yi, xmin=xn[0], xmax=xn[-1], lw=0.5, color='darkgray')

        if nodeson:
            # Dibujamos un punto en cada nodo de la malla
            ax.scatter(xg, yg, marker='.', color='darkgray')
                    
    def imshow(self, n, dat, **par):
        """
        Despliega datos usando un mapa de color.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará la imagen.
        dat : array-like
            Conjunto de datos 2D que serán desplegados.
        par : dict, optional
            Parámetros para decorar la imagen. The default is None.

        Returns
        -------
        out : AxesImage

        See Also
        --------
        matplotlib.axes.Axes.imshow().
        
        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.imshow(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
        out = self.__ax[n-1].imshow(dat, **par)

        return out

    def colorbar(self, n, objeto, **par):
        """
        Agrega una barra de color al subplot[n].

        Parameters
        ----------
        n : int
            El número del subplot donde se agregará la barra de color.
        objeto : TYPE
            Objeto usado para crear el mapa de color (`ScalarMappable`).

        See Also
        --------
        matplotlib.pyplot.colorbar().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.colorbar(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
#        axins = inset_axes(self.__ax[n-1],
#                   width="5%",  # width = 5% of parent_bbox width
#                   height="50%",  # height : 50%
#                   loc='lower left',
#                   bbox_to_anchor=(1.05, 0., 1, 1),
#                   bbox_transform=self.__ax[n-1].transAxes,
#                   borderpad=0,
#                   )

#        self.__fig.colorbar(objeto, ax=axins)

        cbar = self.__fig.colorbar(objeto, ax=self.__ax[n-1], **par)
        
        return cbar
        
    def contour(self, n, xg, yg, dat, **par):
        """
        Dibuja líneas que representan valores constantes de una variable.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará la imagen.
        xg, yg : array-like
            Arreglo 2D con las coordenadas (x,y) donde se tiene un valor.
        dat : array-like
            Valores usados para calcular los contornos.
        par : optional
            Parámetros para decorar los contornos.

        Returns
        -------
        out : QuadContourSet.
        
        See Also
        --------
        matplotlib.axes.Axes.contour().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.contour(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        ax = self.__ax[n-1]
        ax.set_xticks([])
        ax.set_yticks([])
        
        out = self.__ax[n-1].contour(xg, yg, dat, **par)

        return out        
 
    def contourf(self, n, xg, yg, dat, **par):
        """
        Dibuja zonas de color basadas en contornos.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará la imagen.
        xg, yg : array-like
            Arreglo 2D con las coordenadas (x,y) donde se tiene un valor.
        dat : array-like
            Valores usados para calcular los contornos.
        par : optional
            Parámetros para decorar las zonas de color.

        Returns
        -------
        out : QuadContourSet.
        
        See Also
        --------
        matplotlib.axes.Axes.contourf().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.contourf(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        ax = self.__ax[n-1]
        ax.set_xticks([])
        ax.set_yticks([])
        
        out = ax.contourf(xg, yg, dat, **par)

        return out  

    def streamplot(self, n, x, y, u, v, **par):
        """
        Dibuja líneas de corriente de un campo vectorial en 2D.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará las líneas de corriente.
        x, y : array-like
            Coordenadas de la malla donde se tiene definido el campo vectorial 2D.
        u : array-like
            Arreglos 2D con los valores de la velocidad en dirección x.
        v : array-like
            Arreglos 2D con los valores de la velocidad en dirección y.
        par : optional
            Parámetros para decorar las líneas de corriente.

        Returns
        -------
        out : StreamplotSet

        See Also
        --------
        matplotlib.axes.Axes.streamplot().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.streamplot(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        ax = self.__ax[n-1]
        ax.set_xticks([])
        ax.set_yticks([])
        
        out = ax.streamplot(x.T, y.T, u.T, v.T, **par)

        return out
    
    def quiver(self, n, x, y, u, v, **par):
        """
        Dibuja flecha para representar un campo vectorial en 2D.
        
        Parameters
        ----------
        n : int
            Subplot donde se desplegarán las flechas.
        x, y : array-like
            Coordenadas de la malla donde se tiene definido el campo vectorial 2D.
        u : array-like
            Arreglos 2D con los valores de la velocidad en dirección x.
        v : array-like
            Arreglos 2D con los valores de la velocidad en dirección y.
        par : optional
            Parámetros para decorar las flechas.

        See Also
        --------
        matplotlib.axes.Axes.quiver().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.quiver(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        ax = self.__ax[n-1]
        ax.set_xticks([])
        ax.set_yticks([])
        
        out = ax.quiver(x, y, u, v, **par)

        return out

    def plot_surface(self, n, x, y, z, **par):
        """
        Dibuja una superficie.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará la superficie.
        x, y, z : array-like
            Coordenadas de la superficie, arreglos 2D. z representa las alturas.
        par : optional
            Parámetros para decorar la superficie.

        See Also
        --------
        mpl_toolkits.mplot3d.axes3d.plot_surface().
        
        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot_surface(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
        self.__ax[n-1].plot_surface(x, y, z, **par)


    def plot_mesh(self, n, mesh, vol='o', nod='P', label=False):
        """
        Dibuja la malla de un dominio donde se resolverá una EDP.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará la superficie.
        mesh : Mesh
            Malla con la información necesaria para hacer el dibujo.
        vol : str, optional
            Tipo de marcador para los centros de los volúmenes. The default is 'o'.
        nod : TYPE, optional
            Tipo de marcador para los nodos de la malla. The default is 'x'.
            
        See Also
        --------
        Esta función es similar a Mesh.plot().

        """
        if mesh.dim == '1D':
            
            # Construye los nodos para la malla de FDM
            mesh.coordinatesMeshFDM() 
            yg = np.zeros(mesh.nx)

            #print(mesh.x, yg)
            # Visualiza las líneas de la malla de FDM.
            self.__ax[n-1].plot(mesh.x, yg, **{'color':'k', 'ls':'-', 'lw':1.5})
            # Grafica los nodos de la malla de FDM
            if label:
                par = {'s':30, 'marker':nod, 'color':'k', 'label':'FDM nodes'}
            else:
                par = {'s':30, 'marker':nod, 'color':'k'}
            self.__ax[n-1].scatter(mesh.x, yg, **par)

            # Construye los nodos para la malla de FVM
            x, _, _ = mesh.coordinatesMeshFVM()
            yg = np.zeros(mesh.vx)
            # Grafica los nodos de la malla de FVM 
            if label:
                par = {'s':30, 'marker':vol, 'color':'darkblue', 'label':'FVM nodes'}
            else:
                par = {'s':30, 'marker':vol, 'color':'darkblue'}
            self.__ax[n-1].scatter(x[1:-1], yg, **par)

            ylim = 1.0
            self.__ax[n-1].set_ylim(-ylim, ylim)  
            self.__ax[n-1].set_xlim(-mesh.lx * 0.05, mesh.lx * 1.05)  

        if mesh.dim == '2D':

            # Construye los nodos para la malla de FDM
            mesh.coordinatesMeshFDM() 

            # Visualiza las líneas de la malla de FDM.
            for yv in mesh.y:
                ym = np.zeros(mesh.nx)
                ym[:] = yv
                self.__ax[n-1].plot(mesh.x, ym, **{'color':'k','ls':'-', 'lw':1.5})
            for xv in mesh.x:
                xm = np.zeros(mesh.ny)
                xm[:] = xv
                self.__ax[n-1].plot(xm, mesh.y, **{'color':'k','ls':'-', 'lw':1.5})

            # Visualiza los nodos de la malla de FDM.
            xg_d, yg_d = np.meshgrid(mesh.x, mesh.y)            
            
            # Grafica los nodos de la malla de FDM       
            if label:
                par = {'s':30, 'marker':nod, 'color':'k', 'label':'FDM nodes'}
            else:
                par = {'s':30, 'marker':nod, 'color':'k'}                
            self.__ax[n-1].scatter(xg_d, yg_d, **par)
            
            # Construye los nodos para la malla de FVM
            x, y, _ = mesh.coordinatesMeshFVM() 
            xg_v, yg_v = np.meshgrid(x[1:-1], y[1:-1]) 
            # Grafica los nodos de la malla de FVM
            if label:               
                par = {'s':30, 'marker':vol, 'c':'darkblue', 'label':'FVM nodes'}
            else:
                par = {'s':30, 'marker':vol, 'c':'darkblue'}               
            self.__ax[n-1].scatter(xg_v, yg_v, **par)
            
            self.__ax[n-1].set_xlim(-mesh.lx * 0.05, mesh.lx * 1.05)
            self.__ax[n-1].set_ylim(-mesh.ly * 0.05, mesh.ly * 1.05)   

#        self.__ax[n-1].legend(**{'loc':'upper center', 'ncol':2})
        self.__ax[n-1].grid(linestyle='--', linewidth=0.5)

    def animate(self, function, N, interval = 500):
        """
        Realiza una animación de una serie de tiempo.

        Parameters
        ----------
        function : funct
            Función que cambia los datos que se van desplegar.
        N : int
            Número de cuadros de la animación.
        interval : int, optional
            Intervalo de tiempo entre cuadros, en milisegundos. The default is 500.

        See Also
        --------
        matplotlib.animation.FuncAnimation()

        """
        anim = FuncAnimation(self.__fig,            # La figura
                             function, # la función que cambia los datos
                             interval=interval,     # Intervalo entre cuadros en milisegundos
                             frames=N+1,   # Cuadros
                             repeat=True)   # Permite poner la animación en un ciclo        
        
        return anim


    def plot_vectors(self, n, vecs, lvecs = None, baseline = [], w = 0.01, aspect='equal', limit=True, ofx = 0.0):
        """
        Dibuja vectores en el plano cartesiano.

        Parameters
        ----------
        vecs: list
        Lista de np.arrays de dimensión 2.

        lvecs: list
        Lista de etiquetas (str) para distinguir cada vector.

        baseline: list
        Lista de np.arrays para definir el inicio de cada vector.

        w: float
        Ancho de la línea de los vectores.

        aspect: str
        El aspecto del gráfico.

        limit: bool
        Se limita el máximo y mínimo de la gráfica.

        Returns
        -------
        """
        xmax, xmin = 0, 0
        ymax, ymin = 0, 0
        vxm, vym = [], []
        
        for i, x in enumerate(vecs):
            color = 'C' + str(i)
                        
            if len(baseline) == 0:
                x0, y0 = 0, 0
            else:
                x0 = baseline[i][0]
                y0 = baseline[i][1]
            
            vxm.append(x0); vxm.append(x[0] + x0)
            vym.append(y0); vym.append(x[1] + y0)
            
            if lvecs != None:
                self.__ax[n-1].quiver(x0, y0, x[0], x[1], angles='xy', scale_units='xy', scale=1, width=w, color=color, label=lvecs[i])
            else:
                self.__ax[n-1].quiver(x0, y0, x[0], x[1], angles='xy', scale_units='xy', scale=1, width=w, color=color)
    
        xmax = np.array(vxm).max()
        xmin = np.array(vxm).min()
        ymax = np.array(vym).max()
        ymin = np.array(vym).min()
    
        if limit:
            xoff = np.fabs(xmax - xmin) * 0.1
            yoff = np.fabs(ymax - ymin) * 0.1
            self.__ax[n-1].set_xlim(xmin-xoff, xmax+xoff)
            self.__ax[n-1].set_ylim(ymin-yoff, ymax+yoff)

        self.__ax[n-1].set_aspect(aspect)

        if lvecs != None:
            self.__ax[n-1].legend(ncol = 1, loc = 'best', bbox_to_anchor=(1.0+ofx, 0.5, 0.5, 0.5))
        
            
    def plot_vectors_sum(self, n, vecs, lvecs = None, baseline = [], w = 0.01, aspect='equal', limit=True, ofx=0.0):
        suma = np.array([0.0, 0.0])
        lsuma = ''
        for vi, li in zip(vecs, lvecs):
#            suma += vi
            suma = np.add(suma, vi, out=suma, casting="unsafe")
#            print('vi = {} \t suma = {}'.format(vi, suma))
            lsuma += li if li[0] == '-' else '+'+li

        lsuma = lsuma[1:] if lsuma[0] == '+' else lsuma
        vecs.append(suma)
        lvecs.append(lsuma)
        self.plot_vectors(n, vecs, lvecs, baseline, w, aspect, limit, ofx)
        if len(vecs) == 3:
            self.__ax[n-1].plot([vecs[0][0], suma[0]], [vecs[0][1], suma[1]], lw=0.75, ls='--', c='dimgrey')
            self.__ax[n-1].plot([vecs[1][0], suma[0]], [vecs[1][1], suma[1]], lw=0.75, ls='--', c='dimgrey')

if __name__ == '__main__':

    v = Plotter()
    x = np.linspace(0,2*np.pi)
    for i in range(10):
        y = np.cos(x+i*np.pi*0.1)
        v.plot(1, x,y,label='{}'.format(i))
        
    v.legend()
    v.show()
    
    v = Plotter(1,2)
    x = np.array([1,2,3])
    y = np.array([1,2.718281828459045,3.141592653589793])

    # Las funciones de graficación son un subconjunto de las de matplotlib
    v.plot(1, x, y)

    # Se usan los mismos parámetros de las funciones de matplotlib, 
    v.scatter(2, x, y, fc = 'blue', ec = 'gray')

    # Puedo agregar un título a toda la gráfica.
    v.figtitle('Hello')
    # Se activa la grid en todas las subgráficas
    v.grid()
    v.show()
    
    
    # Parámetros para la figura
    fig_par ={'figsize':(8,5)}

    # Parámetros para las subgráficas (lista de diccionarios)
    ejes_par = [
        # Subgráfica 1
        {'title':'plot(x,y,par)', 'xlabel':'x', 'ylabel':'y'},
        # Sibgráfica 2
        {'title':'$Exponencial$', 'yscale':'log', 'xlabel':'$x$', 'ylabel':'$y$ [log]'},
        # Subgráfica 3
        dict(title='Random points', xlabel='n')]

    # Parámetros para el título
    titulo_par = dict(color='blue', fontsize=20)

    # Se define un arreglo de (2 x 2) subgráficas
    v = Plotter(2, 2, ejes_par, fig_par, titulo_par, "Probando visual")

    x = np.linspace(0, 2 * np.pi, 50)
    y = np.sin(x)
    r = 0.9 * np.random.rand(len(x))

    # Primera subgráfica
    v.plot(1, x, y, marker = 'x', color='green', ls='--', label='y = sin(x)')

    # Segunda subgráfica
    v.plot(2, x, np.exp(x), ls='--', lw=3.0, label='$e^x$')
    v.plot(2, x, np.exp(y), lw=2.0, label = '$e^y$')

    # Tercera subgráfica
    v.scatter(3, x, r, marker='.', label='random points')

    # Cuarta subgráfica
    v.scatter(4, x, r, s = x*5, c = y)
    v.plot(4, x, y*y, color = 'r', ls = '-.', lw = 0.80, label = '$sin^2(x)$')

    # Acciones sobre subconjuntos de subgráficas
    v.grid([2,4]) # se activa la rejilla en las subgráficas 2 y 4
    v.legend(frameon=True) # se activan las leyendas en todas las subgráficas
    v.show() # similar a plt.show()
    
    
    
    v = Plotter(1,1)
    x = np.linspace(-10.5, 10.5, 200)
    v.plot(1, x, np.sin(x))

    trig = True

    ejes = True

    if ejes:
        v.set_coordsys(1, trig=trig)
    else:
        ax = v.axes(1)
        xticks = ax.get_xticks()
        yticks = ax.get_yticks()
        v.set_ticks(ax, xticks, yticks, trig=trig)

    v.grid()
    v.show()
    
### Modelación computacional

    # Tamaño del dominio
    Lx = 2.0
    Ly = 1.0

    # Número de nodos en cada eje
    Nx = 15
    Ny = 8

    # Tamaño de la malla en cada dirección
    hx = Lx / (Nx+1)
    hy = Ly / (Ny+1)

    #print('hx = {}, hy = {}'.format(hx, hy))

    # Número total de nodos incluyendo las fronteras
    NxT = Nx + 2
    NyT = Ny + 2

    # Coordenadas de la malla
    xn = np.linspace(0,Lx,NxT)
    yn = np.linspace(0,Ly,NyT)
    xg, yg = np.meshgrid(xn, yn, indexing='ij')

    # Definición de un campo escalar en cada punto de la malla
    T = np.zeros((NxT, NyT))

    # Asignamos un valor a cada entrada del arreglo
    for i in range(NxT):
        for j in range(NyT):
            T[i,j] = np.sin(np.pi*i/8) * np.cos(np.pi*j/8)

    A = 1.0
    alpha = 1.25
    U = -A * np.cos(np.pi * alpha * yg) * np.sin(np.pi * alpha * xg)
    V =  A * np.sin(np.pi * alpha * yg) * np.cos(np.pi * alpha * xg)

    a_p = dict(aspect = 'equal')
    axis_par = [a_p for i in range(0,6)]
    #axis_par.append(dict(projection='3d', aspect='equal'))

    v = Plotter(3,2, axis_par, dict(figsize=(8,6)))

    v.set_canvas(1, Lx, Ly)
    v.draw_domain(1, xg, yg)
    v.axes(1).set_title('Dominio de estudio', fontsize=10)

    v.set_canvas(2, Lx, Ly)
    v.plot_mesh2D(2, xg, yg, nodeson = True)
    v.plot_frame(2, xg, yg, ticks=False)
    v.axes(2).set_title('Malla del dominio', fontsize=10)

    cax = v.set_canvas(3, Lx, Ly)
    c = v.contourf(3, xg, yg, T, levels = 50, cmap = 'gist_earth')
    v.fig.colorbar(c, cax=cax, ticks = [T.min(), T.max()], shrink=0.5, orientation='vertical')
    v.plot_frame(3, xg, yg, ticks=False)
    v.axes(3).set_title('Campo escalar', fontsize=10)

    v.set_canvas(4, Lx, Ly)
    v.quiver(4, xg, yg, U, V)
    v.plot_frame(4, xg, yg, ticks=False)
    v.axes(4).set_title('Campo vectorial', fontsize=10)

    cax = v.set_canvas(5, Lx, Ly)

    v.plot_frame(5, xg, yg, ticks=False)

    c = v.contour(5, xg, yg, T, levels = 10, cmap = 'Greys')
    v.fig.colorbar(c, cax=cax, ticks = [], shrink=0.5, orientation='vertical')
    v.axes(3).set_title('Campo escalar', fontsize=10)

    v.set_canvas(6, Lx, Ly)
    v.streamplot(6, xg, yg, U, V)
    v.plot_frame(6, xg, yg, ticks=False)
    v.axes(6).set_title('Campo vectorial', fontsize=10)

    v.fig.tight_layout(h_pad=0.5, w_pad=2.0)
    v.show()

### Modelación computacional, gráficos en 3D

    # Tamaño del dominio
    Lx = 1.0
    Ly = 1.0

    # Número de nodos en cada eje
    Nx = 15
    Ny = 8

    # Tamaño de la malla en cada dirección
    hx = Lx / (Nx+1)
    hy = Ly / (Ny+1)

    #print('hx = {}, hy = {}'.format(hx, hy))

    # Número total de nodos incluyendo las fronteras
    NxT = Nx + 2
    NyT = Ny + 2

    # Coordenadas de la malla
    xn = np.linspace(0,Lx,NxT)
    yn = np.linspace(0,Ly,NyT)
    xg, yg = np.meshgrid(xn, yn, indexing='ij')

    # Definición de un campo escalar en cada punto de la malla
    T = np.zeros((NxT, NyT))

    # Asignamos un valor a cada entrada del arreglo
    for i in range(NxT):
        for j in range(NyT):
            T[i,j] = np.sin(np.pi*i/8) * np.cos(np.pi*j/8)

    A = 1.0
    alpha = 2.0
    U = -A * np.cos(np.pi * alpha * yg) * np.sin(np.pi * alpha * xg)
    V =  A * np.sin(np.pi * alpha * yg) * np.cos(np.pi * alpha * xg)

    axis_par = [dict(aspect = 'equal'), dict(projection='3d', aspect='auto')]
    v = Plotter(1,2, axis_par, dict(figsize=(8,6)))

    cax = v.set_canvas(1, Lx, Ly)
    c = v.contourf(1, xg, yg, U, levels = 100, cmap='viridis')
    v.contour(1, xg, yg, U, levels=10, cmap='Greys')
    v.fig.colorbar(c, cax=cax, ticks = [], shrink=0.5, orientation='vertical')
    v.plot_frame(1, xg, yg, ticks=False)
    v.axes(1).set_title('Campo escalar', fontsize=10)

    v.plot_surface(2, xg, yg, U, cmap='viridis')
    v.axes(2).set_title('Campo escalar', fontsize=10)

    v.fig.tight_layout(h_pad=0.5, w_pad=2.0)
    v.show()
