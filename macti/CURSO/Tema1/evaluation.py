"""
@author: Luis M. de la Cruz [Updated on Sat Apr 15 16:09:15 2023].
"""

# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
from nose.tools import assert_equal
import numpy as np
import pandas as pd
import sympy as sy
import os, sys, platform

import pkg_resources
from IPython.display import display, Latex

class Quizz():

    def __init__(self,
                 qnum,
                 course = '', 
                 topic = '', 
                 server = 'hub'):
        """
        Clase para la creación de ejercicios.
        
        Parameters
        ----------
        qnum: string
        Número de Quizz del Tema (topic).
        
        course: string
        Nombre o identificador del curso.
        
        topic: string
        Tema del curso en el que se aplica el ejercicio.
        
        server: string
        'local' cuando los datos se instalan en una computadora local.
        'hub' cuando los datos se instalan en el Hub.
        'macti' cuando los datos se instalan junto con la biblioteca.
        """
        self.__server = server
        self.__platform = platform.system()
        self.__course_path = ''
        self.__course = course
        
        sep = '\\' if self.__platform == 'Windows' else '/'
        if server == 'local':
            # Obtención del directorio del curso
            abs_path = os.getcwd().split(sep = sep)
            index_co = abs_path.index(self.__course)
            for i in abs_path[0:index_co+1]:
                self.__course_path += i + sep

        self.__course += sep  # Curso/
        self.__topic = topic + sep   # Topico/
        self.__u_a = 'utils' + sep + '.ans' + sep # utils/.ans/
        self.__qnum = qnum # Número del quizz
            
    @property
    def server(self):
        return self.__server
    
    @server.setter
    def server(self, server):
        self.__server = server
        
    def read(self, qnum, enum, name = '.__ans_'):
        filename = name + qnum

        if self.__server == 'local':
            path = self.__course_path + self.__u_a + self.__topic
            stream = path + filename
        elif self.__server == 'hub': # Linux
            # '/usr/local/share/nbgrader/exchange/'
            path = '/srv/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
            stream = path + filename 
        elif self.__server == 'macti':
            path = '/data/' + self.__topic
            stream = pkg_resources.resource_stream('macti', path + filename)
        else:
            print('Invalid option: {}'.format(self.__server))

#        return stream
        return(pd.read_parquet(stream, columns=[enum]))
            
    def eval_option(self, enum, ans):
        """
        Evalúa la respuesta entre varias opciones. Cuando la respuesta es incorrecta lanza un excepción.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        answer = self.read(self.__qnum, enum)
        ans = ans.replace(" ","")
        
        correcta = ans.lower() == answer[enum][0].lower()
        
        if correcta:
            print(Fore.RESET + 80*'-')
            print(Fore.GREEN + 'Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.GREEN + ', es correcta.')
            print(Fore.RESET + 80*'-')
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.RED + ', es INCORRECTA.') 
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Hint:', end = ' ')
            feedback = self.read(self.__qnum, enum, '.__fee_')
            if feedback[enum][0] != None:
                print(Fore.RED + feedback[enum][0])
            else: 
                print()
            print(Fore.RESET + 80*'-')
            
            raise AssertionError

    def eval_expression(self, enum, ans):
        """
        Evalúa una expresión simbólica escrita en formato Python.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        value = self.read(self.__qnum, enum)
        problema = sy.sympify(value[enum][0])
        if problema.equals(ans):
            print(Fore.RESET + 80*'-')
            print(Fore.GREEN + 'Tu respuesta:')
            display(ans)
            print(Fore.GREEN + 'es correcta.')
            print(Fore.RESET + 80*'-')
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Tu respuesta:')
            display(ans)
            print(Fore.RED + 'NO es correcta.')
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Hint:', end = ' ')
            feedback = self.read(self.__qnum, enum, '.__fee_')            
            if feedback[enum][0] != None:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()
            print(Fore.RESET + 80*'-')
            
            raise AssertionError
            
    def eval_numeric(self, enum, ans):
        """
        Evalúa una respuesta numérica que puede estar dada en un arreglo de numpy.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        value = self.read(self.__qnum, enum)        
        correct = value[enum][0]

        try:
            if isinstance(ans, np.ndarray):
                assert_equal(list(ans.flatten()), list(correct))
            else:
                assert_equal(ans, correct)
                
        except AssertionError as info:
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Ocurrió un error en tus cálculos.')
            print(Fore.RESET + 80*'-')
            print(Fore.RED + 'Hint:', end = ' ')
            feedback = self.read(self.__qnum, enum, '.__fee_')            
            if feedback[enum][0] != None:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()            
            print(Fore.RESET + 80*'-')
            
            raise AssertionError            
        else:
            print(Fore.RESET + 80*'-')
            print(Fore.GREEN + 'Tu resultado es correcto.')
            print(Fore.RESET + 80*'-')            


class FileAnswer():
    def __init__(self, 
                 course = '', 
                 topic = '', 
                 server = 'hub'):
    
        self.__server = server
        self.__platform = platform.system()
        self.__course_path = ''
        self.__course = course # Curso/
        
        sep = '\\' if self.__platform == 'Windows' else '/'
        if server == 'local':
            # Obtención del directorio del curso
            abs_path = os.getcwd().split(sep = sep)
            index_co = abs_path.index(self.__course)
            for i in abs_path[0:index_co+1]:
                self.__course_path += i + sep

        self.__course += sep  # Curso/
        self.__topic = topic + sep   # Topico/
        self.__u_a = 'utils' + sep + '.ans' + sep # utils/.ans/

        self.__exernum = []
        self.__answers = []
        self.__feedback = []
        self.__server = server
        
    def write(self, enum, ans, feed=None):
        # Sustitución de una respuesta y de su retroalimentación
        if enum in self.__exernum: # checamos si ya existe el número de ejercicio
            index = self.__exernum.index(enum) # obtenemos el índice en la lista
            if isinstance(ans, np.ndarray):
                self.__answers[index] = ans.flatten() # almacenamos los arreglos de numpy en 1D
            else:
                self.__answers[index] = ans
                
            self.__feedback[index] = feed 
            
        else: # Si el ejercicio es nuevo, lo agregamos
            # Todos los arreglos de numpy se deben almacenar en formato unidimensional
            if isinstance(ans, np.ndarray):
                self.__answers.append(ans.flatten()) # almacenamos los arreglos de numpy en 1D
            else:
                self.__answers.append(ans)
        
            self.__exernum.append(enum)
            self.__feedback.append(feed)
    
    def to_file(self, qnum):
        ans_df = pd.DataFrame([self.__answers], columns=self.__exernum)
        feed_df = pd.DataFrame([self.__feedback], columns=self.__exernum) 

        filename = '.__ans_' + qnum

        if self.__server == 'local':
            path = self.__course_path + self.__u_a + self.__topic
        elif self.__server == 'hub': # Linux
            # '/usr/local/share/nbgrader/exchange/'
            path = '/srv/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
        else:
            print('Invalid option: {}'.format(self.__server))
        
        if not os.path.exists(path):
            print('Creando el directorio :{}'.format(path))
            os.makedirs(path, exist_ok=True)
        
        ans_df.to_parquet(path + '.__ans_' + qnum, compression='gzip')
        feed_df.to_parquet(path + '.__fee_' + qnum, compression='gzip')
        print('Respuestas y retroalimentación almacenadas.'
        
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

#    q = Quizz('macti_lib', 'Derivada', server = 'local')
#    print(q.read('1','1'))

    f = FileAnswer('CURSO', 'Tema1', server = 'local')
    f.write('1',3.141592,'Pi')
    f.write('2a','C', 'La respuesta correcta es C')
    f.write('2b',np.ones(5), 'El arreglo es de 5 unos')
    f.to_file('1')
    
#    q.server = 'hub'
#    q.read('1','1')

#    q.server = 'macti'
#    q.read('1','1')    
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

