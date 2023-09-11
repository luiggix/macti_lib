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
        self.__line_len = 40
        
        # Cuando se usa la instalación local, se debe determinar
        # si el sistema es tipo Windows o Linux, en cada caso el
        # separador de la ruta es diferente.
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
            path = '/usr/local/share/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
#            path = '/srv/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
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
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.GREEN + 'Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.GREEN + ', es correcta.')
            print(Fore.RESET + self.__line_len*'-')
        else:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.RED + ', es INCORRECTA.') 
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Hint:', end = ' ')
            feedback = self.read(self.__qnum, enum, '.__fee_')
            if feedback[enum][0] != None:
                print(Fore.RED + feedback[enum][0])
            else: 
                print()
            print(Fore.RESET + self.__line_len*'-')
            
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
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.GREEN + 'Tu respuesta:')
            display(ans)
            print(Fore.GREEN + 'es correcta.')
            print(Fore.RESET + self.__line_len*'-')
        else:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Tu respuesta:')
            display(ans)
            print(Fore.RED + 'NO es correcta.')
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Hint:', end = ' ')
            feedback = self.read(self.__qnum, enum, '.__fee_')            
            if feedback[enum][0] != None:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()
            print(Fore.RESET + self.__line_len*'-')
            
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
                # Para comparar dos arreglos, debo hacerlo como si fueran listas
                # para que la comparación sea elemento por elemento. Recordemos que 
                # Parquet escribe listas y tuplas en forma de np.ndarray.
                if not np.allclose(ans.flatten(), correct):
                    assert_equal(list(ans.flatten()), list(correct))
            elif isinstance(ans, list):
                if not np.allclose(ans, list(correct)):
                    assert_equal(ans, list(correct))
            elif isinstance(ans, tuple):
                if not np.allclose(ans, tuple(correct)):
                    assert_equal(ans, tuple(correct))
            elif isinstance(ans, dict):
                if not np.allclose(list(np.array([list(ans.keys()), list(ans.values())]).flatten()), list(correct)):
                    assert_equal(list(np.array([list(ans.keys()), list(ans.values())]).flatten()), list(correct))
            elif isinstance(ans, set):
                if not np.allclose(list(ans), list(correct)):
                    assert_equal(ans, set(correct))
            elif isinstance(ans, complex):
                if not np.allclose([ans.real, ans.imag], list(correct)):
                    assert_equal([ans.real, ans.imag], list(correct))
            else:
                if not np.allclose(ans, correct):
                    assert_equal(ans, correct)
                
        except AssertionError as info:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Ocurrió un error en tus cálculos.')
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Hint:', end = ' ')
            feedback = self.read(self.__qnum, enum, '.__fee_')            
            if feedback[enum][0] != None:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()            
            print(Fore.RESET + self.__line_len*'-')
            
            raise AssertionError            
        else:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.GREEN + 'Tu resultado es correcto.')
            print(Fore.RESET + self.__line_len*'-')            


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

    @property
    def answers(self):
        return self.__answers
    
    @property
    def feedback(self):
        return self.__feedback
    
    def write(self, enum, ans, feed=None):
        # Sustitución de una respuesta y de su retroalimentación
        if enum in self.__exernum: # checamos si ya existe el número de ejercicio
            index = self.__exernum.index(enum) # obtenemos el índice en la lista
            if isinstance(ans, np.ndarray):
                self.__answers[index] = ans.flatten() # almacenamos los arreglos de numpy en 1D
            elif isinstance(ans, dict):
                self.__answers[index] = np.array([list(ans.keys()), list(ans.values())]).flatten()
            elif isinstance(ans, complex):
                self.__answers[index] = [ans.real, ans.imag]
            else:
                self.__answers[index] = ans
                
            self.__feedback[index] = feed 
            
        else: # Si el ejercicio es nuevo, lo agregamos
            # Todos los arreglos de numpy se deben almacenar en formato unidimensional
            if isinstance(ans, np.ndarray):
                self.__answers.append(ans.flatten()) # almacenamos los arreglos de numpy en 1D
            elif isinstance(ans, dict):
                self.__answers.append(np.array([list(ans.keys()), list(ans.values())]).flatten())
            elif isinstance(ans, complex):
                self.__answers.append([ans.real, ans.imag])      
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
            path = '/usr/local/share/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
#            path = '/srv/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
        else:
            print('Invalid option: {}'.format(self.__server))
        
        if not os.path.exists(path):
            print('Creando el directorio :{}'.format(path))
            os.makedirs(path, exist_ok=True)
        else:
            print('El directorio :{} ya existe'.format(path))
        
        ans_df.to_parquet(path + '.__ans_' + qnum, compression='gzip')
        feed_df.to_parquet(path + '.__fee_' + qnum, compression='gzip')
        print('Respuestas y retroalimentación almacenadas.')
        
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

    file_answer = FileAnswer('CURSO', 'Tema1', server = 'local')
    quizz = Quizz('1', 'CURSO', 'Tema1', 'local')
    
    t = np.linspace(0,1,10)
    w = np.sin(t)
    opcion = 'c'
    derivada = 'x**2'
    matriz_np = np.array([[0.10, -1.],[0.30,-1.]] )
    array_np = np.array([-200, 20])
    flotante = 0.0
    entero = 1
    complejo = 1 + 5j
    logico = True
    lista = [0, 1, 3.4]
#    tupla = ('a', 'b', 'c')
    tupla = (1.2, 3.1416, np.pi)
#    diccionario = {1:'k1', 2:'2.0'}
    diccionario = {1:1.3, 2:3.14}

    conjunto = {4,1,8,0,4,20}

    x = sy.Symbol('x')
    y = sy.Symbol('y')
    A, B, C = matriz_np, array_np, flotante
    forma_cuadratica = 0.5 * A[0,0] * x**2 + 0.5 * A[1,1] * y**2 + 0.5 * (A[0,1]+A[1,0])* x * y - B[0] * x - B[1] * y + C

    file_answer.write('1a', t, 'Deberías checar ...')
    file_answer.write('1b', w)
    file_answer.write('2', opcion, 'Las opciones válidas son ...')
    file_answer.write('3', derivada, 'Checa las reglas de derivación')
    file_answer.write('4', matriz_np, 'Checa las entradas de la matriz A')
    file_answer.write('5', array_np, 'Checa las entradas del vector B')
    file_answer.write('6', flotante, 'Checa el valor de flotante')
    file_answer.write('7', entero, 'Checa el valor de entero')
    file_answer.write('8', complejo, 'Checa el valor de complejo')
    file_answer.write('9', logico, 'Checa  logico')
    file_answer.write('10', lista, 'Checa la lista')
    file_answer.write('11', tupla, 'Checa la tupla')
    file_answer.write('12', diccionario, 'Checa la diccionario')
    file_answer.write('13', conjunto, 'Checa la conjunto')
    file_answer.write('14', str(forma_cuadratica),'Revisa tus operaciones algebráicas para calcular f(x)')
    file_answer.to_file('1')

    ans_df2 = pd.read_parquet('../utils/.ans/Tema1/.__ans_1') # Se lee en un DataFrame
    print('-'*40)
    for i in ans_df2.columns:
        print("{} --> {}".format(i, ans_df2[i][0]))
    print('-'*40)

    
    quizz.eval_numeric('1a', t)
    quizz.eval_numeric('1b', w)
    quizz.eval_option('2', 'c')
    
    x = sy.Symbol('x')
    resultado = x*x
    display(resultado)
    quizz.eval_expression('3', resultado)
    
    quizz.eval_numeric('4', matriz_np)
    quizz.eval_numeric('5', array_np)
    quizz.eval_numeric('6', flotante)
    quizz.eval_numeric('7', entero)
    quizz.eval_numeric('8', complejo)
    quizz.eval_numeric('9', logico)
    quizz.eval_numeric('10', lista)
    quizz.eval_numeric('11', tupla)
    quizz.eval_numeric('12', diccionario)
    quizz.eval_numeric('13', conjunto)
    quizz.eval_expression('14', forma_cuadratica)
    

