"""
@author: Luis M. de la Cruz [Updated on mié 18 ene 2023 14:07:31 CST].
"""

# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
from nose.tools import assert_equal
import numpy as np
import pandas as pd
import os

import pkg_resources
from IPython.display import display, Latex

class Ejercicio():

    def __init__(self, topic, local=False):
        self.__topic = topic
        self.local = local
    
    @property
    def topic(self):
        return self.__topic
    
    def read(self, num):
        if self.local: 
            pwd = os.getcwd()
            pwd_list = pwd.split(sep='/')
            path = ''
            for i in pwd_list[1:]:
                path += '/'
                if i != self.__topic:
                    path += i
                else:
                    break
            path = pd.read_parquet(path + '.__p')['p'][0]            
            filename = path + '/data/' + self.__topic + '/.__ans'
            stream = filename
            
        else:
            filename = '/data/' + self.__topic + '/.__ans'
            stream = pkg_resources.resource_stream('macti', filename) 

        return(pd.read_parquet(stream, columns=[num]))
       
    def responde(self, num, f = None):
        answers = self.read(num)
                                
        if f:
            text = display(Latex(f'${f}$ = '))
        else:
            text = "="
        ans = input(text)
        ans = ans.replace(" ","")
        correcta = ans in answers[num][0]

        if correcta:
            print(Fore.GREEN + '¡Tu respuesta es correcta!')
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Cuidado: ocurrió un error en tus cálculos y/o en tu respuesta.')
            print(Fore.RESET + 80*'-')  
            
    def verifica(self, num, x):
        value = self.read(num)
        
        x = np.array(x)
        y = value[num][0]

        try:
            assert_equal(list(x.flatten()), list(y.flatten()))
        except AssertionError as info:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Cuidado: ocurrió un error en tus cálculos: \n {}'.format(info))
            print(Fore.RESET + 80*'-')
        else:
            print(Fore.GREEN + '¡Tu resultado es correcto!')
            
class Evalua():
    def __init__(self, topic, local=False):
        self.topic = topic
        self.local = local 

    def verifica(self, x, i):
        """
        Permite comparar el contenido de x con el de y. Si se encuentra una diferencia entonces emite una alerta.
        """

        if self.local:
            stream = self.topic + '/sol{:02d}.npy'.format(i)
        else:
            filename = 'data/' + self.topic + '/sol{:02d}.npy'.format(i)
            stream = pkg_resources.resource_stream('macti', filename)
        y = np.load(stream)
    
        try:
            assert_equal(list(x.flatten()), list(y.flatten()))
        except AssertionError as info:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Cuidado: ocurrió un error en tus cálculos: \n {}'.format(info))
            print(Fore.RESET + 80*'-')
        else:
            print(Fore.GREEN + '¡Tu resultado es correcto!')
          
            
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
    
    e = Ejercicio('example', local=True)
    e.respuesta('1a')
    
"""
    x = np.linspace(0,1500,10)
    PA = 0.10 * x + 200
    PB = 0.35 * x + 20

    print('\n Global data')
    d = Evalua('SistemasLineales')     
    d.verifica(PA, 1)
    d.verifica(PB, 2)
    
    print('Test')
    np.save('sol01.npy', np.array(['4x^3','b',343.34]))
    e = EvaluaEjercicio('',local=True)
    e.ejercicio(1)
    

    print('\n Local data')
    f = Evalua('./data/SistemasLineales/', local=True)
    f.verifica(PA, 1)
    f.verifica(PB, 2)
"""

