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
plt.style.use('seaborn-ticks')
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
mpl.rcParams['axes.grid'] = True
mpl.rcParams['axes.titlelocation'] = 'left'
mpl.rcParams['axes.titlesize'] = 14
mpl.rcParams['axes.titlecolor'] = title_color
mpl.rcParams['axes.titley'] = 1.02
colors = [[0,0,0], 
          [230/255,159/255,0],
          [86/255,180/255,233/255], 
          [0,158/255,115/255],
          [240/255,228/255,66/255], 
          [0,114/255,178/255],
          [213/255,94/255,0], 
          [204/255,121/255,167/255]
        ]
mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)
mpl.rcParams['lines.linewidth'] = 2
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
    
    def __init__(self, rows = 1, cols = 1, par = None, par_fig={}, title='', par_title={}):
        """
        Crea e inicializa una figura de matplotlib.

        Parameters
        ----------
        rows : int, opcional
            Número de renglones del arreglo de subplots. The default is 1.
        cols : int, opcional
            Número de columnas del arreglo de subplots. The default is 1.
        par : list of dicts, opcional
            Lista de diccionarios; cada diccionario define los parámetros que 
            se usarán decorar los `Axes` de cada subplot. The default is None.
        par_fig : dict, opcional
            Diccionario con los parámetros para decorar la figura. 
            The default is {}.
        title: dict, opcional
        Diccionario con los parámetros para el título de la figura.

        """
        self.__fig = plt.figure(**par_fig)
        self.__fig.suptitle(title, **par_title)
        self.__nfigs =  rows *  cols

        if par != None:
            Nfill = self.__nfigs - len(par)
        else:
            Nfill = self.__nfigs
            par = [ ]
            
        [par.append({}) for n in range(Nfill)]
            
        self.__ax = [plt.subplot(rows, cols, n, **par[n-1]) for n in range(1,self.__nfigs + 1)]
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
        offx = lmax * 0.01
        offy = lmax * 0.01
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
                
    def legend(self, nlist = [], par=None):
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
            if par != None:   
                [self.__ax[n].legend(**par) for n in range(0,self.__nfigs)]        
            else:
                [self.__ax[n].legend() for n in range(0,self.__nfigs)]        
#
#----------------------- Methods to draw a specific kind of plot -------------   
#        
    def plot(self, n, data1, data2, par=None):
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
        par : dict, opcional
            Parámetros para decorar la línea. The default is None.

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
        
        if par != None:
            out = self.__ax[n-1].plot(data1, data2, **par)
        else:
            out = self.__ax[n-1].plot(data1, data2)            
        return out

    def scatter(self, n, data1, data2, par=None):
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
        par : dict, opcional
            Parámetros para decorar los puntos. The default is None.

        Returns
        -------
        out : PathCollection
        
        See Also
        --------
        matplotlib.axes.Axes.scatter().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.scatter(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
        if par != None:
            out = self.__ax[n-1].scatter(data1, data2, **par)
        else:
            out = self.__ax[n-1].scatter(data1, data2)              
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
                    
    def imshow(self, n, dat, par=None):
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
        
        if par != None:
            out = self.__ax[n-1].imshow(dat, **par)
        else:
            out = self.__ax[n-1].imshow(dat)
        return out

    def colorbar(self, n, objeto, par=None):
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
        if par != None:
            self.__fig.colorbar(objeto, ax=self.__ax[n-1], **par)
        else:
            self.__fig.colorbar(objeto, ax=self.__ax[n-1])
        
    def contour(self, n, xg, yg, dat, par=None):
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
        par : dict, optional
            Parámetros para decorar los contornos. The default is None.

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
        
        if par != None:
            out = self.__ax[n-1].contour(xg, yg, dat, **par)
        else:
            out = self.__ax[n-1].contour(xg, yg, dat)
        return out        
 
    def contourf(self, n, xg, yg, dat, par=None):
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
        par : dict, optional
            Parámetros para decorar las zonas de color. The default is None.

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
        
        if par != None:
            out = ax.contourf(xg, yg, dat, **par)
        else:
            out = ax.contourf(xg, yg, dat)
        return out  

    def streamplot(self, n, x, y, u, v, par=None):
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
        par : dict, optional
            Parámetros para decorar las líneas de corriente. The default is None.

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
        
        if par != None:
            out = ax.streamplot(x.T, y.T, u.T, v.T, **par)
        else:
            out = ax.streamplot(x.T, y.T, u.T, v.T)
        return out
    
    def quiver(self, n, x, y, u, v, par=None):
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
        par : dict, optional
            Parámetros para decorar las flechas. The default is None.

        See Also
        --------
        matplotlib.axes.Axes.quiver().

        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.quiver(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)

        ax = self.__ax[n-1]
        ax.set_xticks([])
        ax.set_yticks([])
        
        if par != None:
            ax.quiver(x, y, u, v, **par)
        else:
            ax.quiver(x, y, u, v)

    def plot_surface(self, n, x, y, z, par=None):
        """
        Dibuja una superficie.

        Parameters
        ----------
        n : int
            Subplot donde se desplegará la superficie.
        x, y, z : array-like
            Coordenadas de la superficie, arreglos 2D. z representa las alturas.
        par : dict, optional
            Parámetros para decorar la superficie. The default is None.

        See Also
        --------
        mpl_toolkits.mplot3d.axes3d.plot_surface().
        
        """
        assert (n >= 1 and n <= self.__nfigs), \
        "Plotter.plot_surface(%d) out of bounds. Valid bounds : [1,%d]" % (n,self.__nfigs)
        
        if par != None:
            self.__ax[n-1].plot_surface(x, y, z, **par)
        else:
            self.__ax[n-1].plot_surface(x, y, z)

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
            Funciónque cambia los datos que se van desplegar.
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
    

def format_func(value, tick_number):
    # find number of multiples of pi/2
    N = int(np.round(2 * value / np.pi))
    if N == 0:
        return "0"
    elif N == 1:
        return r"$\pi/2$"
    elif N == 2:
        return r"$\pi$"
    elif N % 2 > 0:
        return r"${0}\pi/2$".format(N)
    else:
        return r"${0}\pi$".format(N // 2)

def set_ticks(ax, xticks = [], yticks = [], trig = False):
    if trig:
        ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
        ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    else:        
        if len(xticks) != 0:
            ax.set_xticks(xticks)
        if len(yticks) != 0:
            ax.set_yticks(yticks)
            
def calcOffset(xg, yg):
    Lx = xg[-1,0] - xg[0,0]
    Ly = yg[0,-1] - yg[0,0]
    lmin = min(Lx, Ly)
    offx = lmin * 0.1
    offy = lmin * 0.1
    return offx, offy, xg[0,0], xg[-1,0], yg[0,0], yg[0,-1]

def plotMalla(xg, yg, title='', cbar = False, marker='.'):
    plt.scatter(xg, yg, marker=marker, c='royalblue')
    x = xg[:,0]
    y = yg[0,:]
    plt.xticks([x[0], x[-1]], labels=[x[0], x[-1]])
    plt.yticks([y[0], y[-1]], labels=[y[0], y[-1]])
    plt.xlabel(title)
    offx, offy, ax, bx, ay, by = calcOffset(xg, yg)
    plt.xlim(ax-offx, bx+offx)
    plt.ylim(ay-offy, by+offy)
    plotGrid(x, y)
    ax = plt.gca()
    ax.set_aspect('equal')
    
    if cbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        cax.set_xticks([])
        cax.set_yticks([])

def plotContornos(xg, yg, u, title='', frame = 'box', cbar = True):
    cf = plt.contourf(xg, yg, u, levels = 50, alpha=.75, cmap="YlOrRd")
    cl = plt.contour(xg, yg, u, levels = 10, colors='k', linewidths=0.5)
    plt.clabel(cl, inline=True, fontsize=10.0)

    x = xg[:,0]
    y = yg[0,:]
    plt.xticks([x[0], x[-1]], labels=[x[0], x[-1]])
    plt.yticks([y[0], y[-1]], labels=[y[0], y[-1]])
    plt.xlabel(title)
    #plt.ylabel('$y$')
    offx, offy, ax, bx, ay, by = calcOffset(xg, yg)
    plt.xlim(ax-offx, bx+offx)
    plt.ylim(ay-offy, by+offy)
    plotGrid(x, y, frame)
    ax = plt.gca()
    ax.set_aspect('equal')

    if cbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        cax.set_xticks([])
        cax.set_yticks([])
        fig = plt.gcf()
        fig.colorbar(cf, cax=cax, orientation='vertical')
    
#    plt.suptitle(title, color='blue')

def plotFlujo(xg, yg, u, v, kind='quiver', title='', frame = 'box', cbar=False):
    """
    """

    x = xg[:,0]
    y = yg[0,:]
    plt.xticks([x[0], x[-1]], labels=[x[0], x[-1]])
    plt.yticks([y[0], y[-1]], labels=[y[0], y[-1]])
    plt.xlabel(title)
    #plt.ylabel('$y$')
    offx, offy, ax, bx, ay, by = calcOffset(xg, yg)
    plt.xlim(ax-offx, bx+offx)
    plt.ylim(ay-offy, by+offy)
    
    if kind == 'quiver':
        plt.quiver(xg, yg, u(xg,yg), v(xg,yg), color='gray')
    elif kind == 'stream':
        xg, yg = np.meshgrid(x,y)
        plt.streamplot(x, y, u(xg,yg), v(xg,yg), color='gray', linewidth=0.5)
        
    plotGrid(x, y, frame) 

    ax = plt.gca()
    ax.set_aspect('equal')
    
    if cbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        cax.set_xticks([])
        cax.set_yticks([])
    
if __name__ == '__main__':

    ax = -3.0
    bx = 3.0
    ay = -3.0
    by = 3.0
    Nx = 21
    Ny = 21
    
    x = np.linspace(ax,bx,Nx+2)
    y = np.linspace(ay,by,Ny+2)
    plotGrid(x,y)
    plt.show()
    
    xg, yg = np.meshgrid(x, y, indexing='ij', sparse=False)
    plotMalla(xg, yg, 'Test ({}x{})'.format(Nx, Ny))
    plt.show()

    plotMalla(xg, yg, 'Test ({}x{})'.format(Nx, Ny), marker='')
    plt.show()
    
    z = (1 - xg/2 + xg**5 + yg**3) * np.exp(-xg**2 - yg**2)
    plotContornos(xg, yg, z, 'Hola', 'grid')
    plt.show()
    
    u = lambda x,y : 1*((-1/2 + 5*x**4) - 2*x*(1-x/2+x**5+y**3)) * np.exp(-x**2-y**2)
    v = lambda x,y : (3*y**2 - 2*x*(1-x/2+x**5+y**3)) * np.exp(-x**2-y**2)
    plotFlujo(xg, yg, u, v, 'quiver', 'flujo', 'box')
    plt.show()

    Nx = 31
    Ny = 11
    x = np.linspace(0.0,3.0,Nx+2)
    y = np.linspace(0.0,1.0,Ny+2)
    xg, yg = np.meshgrid(x, y, indexing='ij', sparse=False)
    A = 1.0
    α = 1.0
    u = lambda x, y: -A * np.cos(α * np.pi * y) * np.sin(α * np.pi * x) 
    v = lambda x, y:  A * np.sin(α * np.pi * y) * np.cos(α * np.pi * x)    
    plotFlujo(xg, yg, u, v, 'quiver', '', 'grid')
    plt.show()