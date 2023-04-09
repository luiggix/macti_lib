"""
@author: Luis M. de la Cruz [Updated on mié 18 ene 2023 14:07:31 CST].
"""

# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
from nose.tools import assert_equal
import numpy as np
import pandas as pd
import os, sys, platform

import pkg_resources
from IPython.display import display, Latex

class Quizz():

    def __init__(self, 
                 course = '', 
                 topic = '', 
                 server = 'hub'):
        self.__course = course
        self.__topic = topic
        self.__server = server
        self.__platform = platform.system()
        self.__dirsep = '/'
        if self.__platform == 'Windows':
            self.__dirsep = '\\'

    @property
    def course(self):
        return self.__course
    
    @course.setter
    def course(self, course):
        self.__course = course
        
    @property
    def topic(self):
        return self.__topic
    
    @topic.setter
    def topic(self, topic):
        self.__topic = topic

    @property
    def server(self):
        return self.__server
    
    @server.setter
    def server(self, server):
        self.__server = server
        
    def read(self, qnum, enum):
        sep = self.__dirsep
        filename = '.__ans_' + qnum
        co = self.__course + sep
        to = self.__topic + sep
        u_d = 'utils' + sep + 'data' + sep
        print(self.__platform, self.__dirsep, u_d)
        
        abs_path = os.getcwd().split(sep = sep)
        print(abs_path)
        index_co = abs_path.index(self.__course)
        course_path = ''
        for i in abs_path[0:index_co+1]:
            course_path += i + sep

        print(course_path)
        
        if self.__server == 'local':
            path = '../' + u_d
            stream = path + filename
        elif self.__server == 'hub':
            path = '/srv/nbgrader/exchange/' + co + u_d + to
            stream = path + filename 
        elif self.__server == 'macti':
            path = '/data/' + to
            stream = path + filename
#            stream = pkg_resources.resource_stream('macti', path + filename)
        else:
            print('Invalid option: {}'.format(self.__server))
            
        print(stream)
        
#        return(pd.read_parquet(stream, columns=[enum]))
       
    def responde(self, qnum, enum, ans):
        answers = self.read(qnum, enum)
                                
#        if f:
#            text = display(Latex(f'${f}$ = '))
#        else:
#            text = "="
#        ans = input(text)
        ans = ans.replace(" ","")
        correcta = ans in answers[enum][0]

        if correcta:
            print(Fore.GREEN + '¡Tu respuesta es correcta!')
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Cuidado: ocurrió un error en tus cálculos y/o en tu respuesta.')
            print(Fore.RESET + 80*'-')  
            
    def verifica(self, qnum, enum, x):
        value = self.read(qnum, enum)
        
        x = np.array(x)
        y = value[enum][0]

        try:
            assert_equal(list(x.flatten()), list(y.flatten()))
        except AssertionError as info:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Cuidado: ocurrió un error en tus cálculos: \n {}'.format(info))
            print(Fore.RESET + 80*'-')
            raise AssertionError
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

    q = Quizz('macti_lib', server = 'local')
    q.topic = 'derivada'
    q.read('1','1')

    q.server = 'hub'
    q.read('1','1')

    q.server = 'macti'
    q.read('1','1')    
"""
    e = Ejercicio('example', local=True)
    e.respuesta('1a')
    
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

