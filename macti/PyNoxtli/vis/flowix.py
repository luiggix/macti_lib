  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on lun mar 30 12:29:10 CST 2020].
"""

#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../'))
#-----------------------------------------------------------

import numpy as np
#from mpl_toolkits.mplot3d import Axes3D
#from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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
    
    def __init__(self, rows = 1, cols = 1, par = None, par_fig={}, title=''):
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

        """
        self.__fig = plt.figure(**par_fig)
        self.__fig.suptitle(title, fontweight='light', fontsize='12', color='blue')
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
        plt.tight_layout(pad, h_pad, w_pad, rect = None)
        
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
        
        if par != None:
            out = self.__ax[n-1].contourf(xg, yg, dat, **par)
        else:
            out = self.__ax[n-1].contourf(xg, yg, dat)
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
        
        if par != None:
            out = self.__ax[n-1].streamplot(x, y, u, v, **par)
        else:
            out = self.__ax[n-1].streamplot(x, y, u, v)
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
        
        if par != None:
            self.__ax[n-1].quiver(x, y, u, v, **par)
        else:
            self.__ax[n-1].quiver(x, y, u, v)

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
    

#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
#
# Ejemplo de construcción de varios tipos de figuras XY
#
    fig_par ={'figsize':(10,5)}
    axis_par1 = [{'title':'plot(x,y,par)', 'xlabel':'x', 'ylabel':'y'},
                {'title':'$Exponencial$', 'yscale':'log', 'xlabel':'$x$', 'ylabel':'$y$ [log]'},
                {'title':'Random points', 'xlabel':'n'}]
    vis1 = Plotter(2, 2, axis_par1, fig_par, 'Testing: plot() & scatter()')
    
    x = np.linspace(0, 2 * np.pi, 50)
    y = np.sin(x)
    r = 0.9 * np.random.rand(len(x))
    
    plot_par = {'marker':'x', 'color':'green', 'ls':'-','label':'y = sin(x)'}
    vis1.plot(1, x, y, plot_par)
    vis1.plot(2, x, np.exp(x), {'ls':'--', 'lw':3.0, 'label':'$e^x$'})
    vis1.plot(2, x, np.exp(y), {'lw':2.0, 'label':'$e^y$'})
    vis1.scatter(3, x, r, {'marker':'.', 'label':'rp'})
    vis1.scatter(4, x, r, {'s':x*5, 'c':y, 'label':'rp'})
    vis1.plot(4, x, y*y, {'color':'r', 'ls':'-.', 'lw':0.80, 'label':'$sin^2(x)$'})
    
    vis1.grid([2,4])
    vis1.legend()
    vis1.show()
#
# Ejemplos de construcción de una malla, contornos, campos vectorial,
# streamlines, colorbar,
#   
#    import geo.mesh_test.umesh as mayas
    from macti.PyNoxtli.geo.mesh.umesh import uMesh

    umalla = uMesh(nx = 9, ny = 5, lx = 2.0, ly = 1.0)
    
    xg, yg = np.meshgrid(np.linspace(0, umalla.lx, umalla.nx*4),
                          np.linspace(0, umalla.ly, umalla.ny*4))    
    A = 1.0
    alpha = 1.25
    u = -A * np.cos(np.pi * alpha * yg) * np.sin(np.pi * alpha * xg)
    v =  A * np.sin(np.pi * alpha * yg) * np.cos(np.pi * alpha * xg)
    
    axis_par2 = [{},
                  {},
                  {},
                  {}]
    vis2 = Plotter(2, 2, axis_par2, fig_par, 'Funcionalidades sofisticadas')
    objeto = vis2.imshow(1, v, {'cmap':'gist_rainbow'})
    vis2.colorbar(1, objeto)
    vis2.plot_mesh(2, umalla, vol = 's')
    vis2.quiver(3, xg, yg, u, v)
    vis2.streamplot(3, xg, yg, u, v)    
    vis2.contourf(4, xg, yg, u, {'levels':50, 'cmap':'gist_earth'})
    vis2.contour(4, xg, yg, u, {'levels':10, 'colors':'k'})
    vis2.show()

# Non-Uniform Mesh
    
    x = np.array([ 0, 0.307917, 0.767275, 1.45256, 2.47488, 4, 
                  5.52512, 6.54744, 7.23272, 7.69208, 8 ])

    y = np.array([ 0, 0.307917, 0.767275, 1.45256, 2.47488, 4, 
                  5.52512, 6.54744, 7.23272, 7.69208, 8 ])

    from geo.mesh.nmesh import nMesh
    malla2D = nMesh(x, y)
    
    par = [{'title':'Mesh %s' % malla2D.dim, 
            'aspect':'auto',
            'xlabel':'x', 'ylabel':'y'}]    
    vis3 = Plotter(1,1, par)
    vis3.plot_mesh(1, malla2D, vol='.', label=True)
    vis3.legend()
    vis3.show()
    