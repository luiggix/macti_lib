#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 14:03:51 2020

@author: luiggi
"""
#-----------------------------------------------------------
# PARA DEFINIR EL PATH ABSOLUTO DE LOS MÓDULOS DE PYNOXTLI
#
import os, sys
if not("/base" in sys.path[0][-5:]):
    sys.path.insert(0, os.path.abspath('../'))   
#-----------------------------------------------------------

def decorate(f):
    """
    Decorador que agrega información de la versión de PyNoxtli.
    
    Parameters
    ----------
    f : 
        Función a decorar.

    Returns
    -------
    nicePrint : func
        Función decoradora.

    """
    def nicePrint(**kargs):
        """
        Función que agrega la información de la versión de PyNoxtli.

        Parameters
        ----------
        **kargs : dict
            argumentos de la función a decorar.

        """
        license_file = sys.path[0] + '/utils/license.txt'
        pynoxtli_license = 'PyNoxtli : Ver. 1.0, LMCS-2021, [GNU GPL License V3]'
#open(license_file).readline()
        line = '-' * 80
        print('.'+ line + '.')
        print('|{:^80}|'.format(pynoxtli_license))
        print('.'+ line + '.')
        f(**kargs)
        print('.'+ line + '.')
        
    return nicePrint

@decorate
def printInfo(**kargs):
    """
    Imprime el nombre del parámetro y su valor.

    Parameters
    ----------
    **kargs : dict
        Diccionario de parámetros a imprimir.

    """
    for (key,value) in kargs.items():
        #
        # Impresión de cadenas
        #
        if (type(value) == float):
            print('|{:<80}|'.format('{0:>15s} = {1:<20.15e}'.format(key, value)))
        else:
            print('|{:<80}|'.format('{0:>15s} = {1:^10s}'.format(key,str(value))))


        # if (type(value) == str):
        #     print('|{:<80}|'.format('{0:>15s} = {1:<30s}'.format(key, value)))
        # elif (type(value) == int):
        #     print('|{:<80}|'.format('{0:>15s} = {1:<30d}'.format(key, value)))
        # elif (value == None):
        #     print('|{:<80}|'.format('{0:>15s} = None'.format(key)))   
        # elif (type(value) == tuple):
        #     if (type(value[0]) == int):
        #         print('|{:<80}|'.format('{0:>15s} = ({1:^10d}, {2:^10d})'.format(key,value[0],value[1])))   
        #     else:
        #         print('|{:<80}|'.format('{0:>15s} = ({1:^10e}, {2:^10e})'.format(key,value[0],value[1]))) 
        # elif (type(value) == dict):
        #     for k in value:
        #         print('|{:<80}|'.format('{0:>15s} = {1:^10s} : {2:^10s}'.format(key,k,str(value[k]))))
        # else:
        #     print('|{:<80}|'.format('{0:>15s} = {1:<30.15e}'.format(key, value)))


if __name__ == '__main__':
    
    printInfo(Name='Laplace', nvx = 5, nx = 6, longitud = 1.3123213, kk = None)
    printInfo(Name='texto', tupla = (5,6), lista = [1,2,3,'a'], dicc = {'a':1, 'b':2})
