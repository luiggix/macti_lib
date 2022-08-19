#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 15:07:51 2019

@author: luiggi
"""

def decorate(f):
    def nicePrint(**kargs):
        line = '-' * 80
        print('.'+ line + '.')
        print('|{:^80}|'.format('NoNacos : Numerical Objects for Natural Convection Systems'))
        print('.'+ line + '.')
        print('|{:^80}|'.format(' Ver. 0.1, Author LMCS, 2019, [GNU GPL License V3]'))
        print('.'+ line + '.')
        f(**kargs)
        print('.'+ line + '.')
    return nicePrint

def testDecorate(f):
    def nicePrint(**kargs):
        line = '-' * 80
        print('.'+ line + '.')
        f(**kargs)
        print('.'+ line + '.')
    return nicePrint
 
@decorate
def printData(**kargs):
    for (key,value) in kargs.items():
        if (type(value) == str):
            print('|{:<80}|'.format('{0:>15s} = {1:<30s}'.format(key, value)))
        elif (type(value) == int):
            print('|{:<80}|'.format('{0:>15s} = {1:<30d}'.format(key, value)))
        elif (value == None):
            print('|{:<80}|'.format('{0:>15s} = None'.format(key)))   
        elif (type(value) == tuple):
            if (type(value[0]) == int):
                print('|{:<80}|'.format('{0:>15s} = ({1:^10d}, {2:^10d})'.format(key,value[0],value[1])))   
            else:
                print('|{:<80}|'.format('{0:>15s} = ({1:^10e}, {2:^10e})'.format(key,value[0],value[1])))
        elif (type(value) == dict):
            for k in value:
                print('|{:<80}|'.format('{0:>15s} = {1:^10s} : {2:^10s}'.format(key,k,str(value[k]))))
        else:
            print('|{:<80}|'.format('{0:>15s} = {1:<30.15e}'.format(key, value)))
            
@testDecorate
def printTest(**kargs):
    for (key,value) in kargs.items():
        if (type(value) == str):
            print('|{:<80}|'.format('{0:>15s} = {1:<30s}'.format(key, value)))
        elif (type(value) == int):
            print('|{:<80}|'.format('{0:>15s} = {1:<30d}'.format(key, value)))
        elif (value == None):
            print('|{:<80}|'.format('{0:>15s} = None'.format(key)))
        else:
            print('|{:<80}|'.format('{0:>15s} = {1:<30.15e}'.format(key, value)))            

if __name__ == '__main__':
    
    printData(Name='Laplace', nvx = 5, nx = 6, longitud = 1.3123213, kk = None)

    printTest(Name='Laplace', nvx = 5, nx = 6, longitud = 1.3123213, kk = None)
   

    
    