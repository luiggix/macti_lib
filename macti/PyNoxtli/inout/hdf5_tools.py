#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Luis M. de la Cruz [Updated on jue abr 16 13:59:24 CDT 2020].
"""

#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
sys.path.insert(0, os.path.abspath('..'))
#-----------------------------------------------------------

import h5py

class HDF5_info():
    
    def __init__(self, filename, verb = False):
        self.__groups = []
        self.__groups_names = []
        self.__datasets = []
        self.__datasets_names = []
        self.__attr = []
        self.__attr_names = []
        self.__leading = '  '
        self.__verb = verb

        if verb:
            line = '-' * 80
            print('.'+ line + '.')   

#        with h5py.File(filename, 'r') as file:
#            print('|{:<80}|'.format(str(file)))
#            print('|{:<80}|'.format(' '))
#            self.travel_object(file)
 
        self.__fh5 = h5py.File(filename, 'r')
        
        if verb:
            print('|{:<80}|'.format(str(self.__fh5)))
            print('|{:<80}|'.format(' '))
            
        self.travel_object(self.__fh5)

        if verb:    
            print('.'+ line + '.')            
   
    def file(self):
        return self.__fh5
    
    def close(self):
        self.__fh5.close()
        
#    def __del__(self):
#        print('Que onda')
#        self.__f_h5.close()
#        print('HDF5 file closed')
        
    def travel_object(self, item):
        for key in item:

            count = -1
            for c in str(item[key].name):
                if c == '/':
                    count += 1
            
            space = self.__leading * count + '=> '
            
            if self.__verb:
                print('|{:<80}|'.format(space + str(item[key])))

            if isinstance(item[key], h5py.Group):
                self.__groups.append(item[key])
                self.__groups_names.append(key)
                
                if self.__verb:
                    attr_list = item[key].attrs
                    space = self.__leading * count + '-->'
                    if len(attr_list):
                        for a in attr_list:
                            print('|{0:} attr : {1:10} value : {2:10} dtype : {3:}'.format(space,a,str(attr_list[a]),str(type(attr_list[a]))))
                    else:
                        print('|{:<80}|'.format(space + ' No attributes in this object'))
                    
                    
                self.travel_object(item[key])
                
            elif isinstance(item[key], h5py.Dataset):
                self.__datasets.append(item[key])
                self.__datasets_names.append(key)


            if self.__verb:    
                print('|{:<80}|'.format(' '))

    
    @property
    def groups(self):
        return self.__groups
    
    @property
    def groups_names(self):
        return self.__groups_names
    
    @property
    def datasets(self):
        return self.__datasets
    
    @property
    def datasets_names(self):
        return self.__datasets_names

if __name__ == '__main__':

    from macti.PyNoxtli.utils.displayInfo import printData
    import macti.PyNoxtli.vis.flowix as flx

    archivo = 'test.h5'

    printData(archivo = archivo,
              test = "'h5_info = HDF5_info(archivo, verb=True)'")
    h5_info = HDF5_info(archivo, verb=True)
    h5_info.close()
    
    input('Next test <press enter>')

    printData(archivo = archivo,
              test = 'h5_info = HDF5_info(archivo)')    
    h5_info = HDF5_info(archivo)

    printData(grupos = len(h5_info.groups))
    print('nombres (grupos): ', h5_info.groups_names)
        
    for g in h5_info.groups:
        print('\n grupo  : ', g)
        for a in g.attrs:
            print('\t',a, g.attrs[a])


    printData(datasets = len(h5_info.datasets))
    print('nombres (datasets) :', h5_info.datasets_names)
    
    for d in h5_info.datasets:
        print('\n dataset :', d)
        print('\t   name: ', d.name)
        print('\t  shape: ', d.shape)
        print('\t  dtype: ', d.dtype)
        print('\t parent: ', d.parent)
        print('\t   file: ', d.file)
            
    input('Plot datasets : <press enter>')

    f = h5_info.file()
    print(f['mesh'].attrs['NX'])

    from macti.PyNoxtli.geo.mesh import Mesh
    
    malla = Mesh(nx = f['mesh'].attrs['NX'], 
                 lx = f['mesh'].attrs['WX'], 
                 ny = f['mesh'].attrs['NY'],
                 ly = f['mesh'].attrs['WY'])

    x, y, _ = malla.constructMeshFVM()    
    axis_par = [{'aspect':'equal','title':'Malla', 'xlabel':'x', 'ylabel':'y'},
                {'aspect':'equal','title':h5_info.datasets_names[0], 'xlabel':'x', 'ylabel':'y'}]   
    v = flx.Plotter(1,2,axis_par)
    v.plot_mesh(1, malla, vol='', nod='')

    con = v.contourf(2,x,y,h5_info.datasets[0],{'cmap':'cool', 'levels':20})
    v.contour(2,x,y,h5_info.datasets[0],{'levels':10})
#    v.colorbar(2, con)
    v.show()
    
#array = h5_info.datasets[0]
#print(array[:])

#print(h5_info.groups)
#print(h5_info.datasets)

    h5_info.close()
