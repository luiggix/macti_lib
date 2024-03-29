"""
@author: Luis M. de la Cruz [Updated on Tue Dec 12 15:32:38 2023].
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
        Clase para la evaluación de ejercicios.
        
        Parameters
        ----------
        qnum: string
        Número de quizz del tema (topic). Puede haber varios quizzes para un solo tema.
        
        course: string
        Nombre o identificador del curso.
        
        topic: string
        Tema del curso en el que se aplica el quizz.
        
        server: string
        'local' cuando los datos (answers & feedback) se almacenan en un directorio local.
        'hub' cuando los datos (answers & feedback) se almacenan en un directorio global del hub.
        'macti' cuando los datos (answers & feedback) se almacenan en el directorio de instalación de la biblioteca.
        """
        self.__server = server
        self.__platform = platform.system()
        self.__course_path = ''  # Ruta del curso
        self.__course = course   # Nombre de curso
        self.__line_len = 40
        
        # Cuando se usa la instalación local, se debe determinar
        # si el sistema es tipo Windows o Linux, en cada caso el
        # separador de la ruta es diferente.
        sep = '\\' if self.__platform == 'Windows' else '/'
        
        if server == 'local':
            # Construcción de una lista con los componentes de la ruta absoluta
            # a partir de donde se ejecuta la notebook
            abs_path = os.getcwd().split(sep = sep)  # Ruta absoluta

            # Obtención del índice donde está el nombre del curso dentro de la lista abs_path
            index_co = abs_path.index(self.__course)

            # Construcción del path del curso
            for i in abs_path[0:index_co+1]:
                self.__course_path += i + sep

        self.__course += sep  # Curso/
        self.__topic = topic + sep   # Topico/
        self.__u_a = 'utils' + sep + '.ans' + sep # utils/.ans/
        self.__qnum = qnum # Número del quizz

        # Verbosity
        self.__verb = self.read('0')['0'][0]

    @property
    def verb(self):
        return self.__verb
        
    @property
    def server(self):
        return self.__server
    
    @server.setter
    def server(self, server):
        self.__server = server
        
    def read(self, enum, name = '.__ans_'):
        """
        Lectura de la respuesta del ejercicio con número enum. Esta lectura
        se realiza del archivo en donde se encuentran las respuestas de todo el quizz.
        El archivo está en formato parquet y las respuestas se almacenan en columnas y en un solo renglón.
        El identificador de la columna corresponde con el número del ejercicio enum.

        Parameters
        ----------
        enum: string
        Número del ejercicio dentro del quizz.
        
        name: string
        Nombre del archivo donde se guardan las respuestas, por omisión es: ".__ans_".
        
        Returns
        -------
        
        """
        # Se agrega el número del quizz correspondiente al nombre del archivo de respuestas. 
        filename = name + self.__qnum

        if self.__server == 'local':
            path = self.__course_path + self.__u_a + self.__topic
            stream = path + filename
            
        elif self.__server == 'hub': 
            # Directorio global en el hub
            path = '/usr/local/share/nbgrader/exchange/' + self.__course + self.__u_a + self.__topic
            stream = path + filename 
            
        elif self.__server == 'macti':
            # Se utiliza pkg_resources para obtener el directorio de instalación de la biblioteca.
            path = '/data/' + self.__topic
            stream = pkg_resources.resource_stream('macti', path + filename)
            
        else:
            print('Invalid option: {}'.format(self.__server))

        # Lectura del archivo en formato parquet, se regresa en un DataFrame.
        return(pd.read_parquet(stream, columns=[enum]))
            
    def eval_option(self, enum, ans):
        """
        Evalúa una pregunta de opción múltiple. Cuando la respuesta es incorrecta lanza un excepción.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo.
        answer = self.read(enum)
        ans = ans.replace(" ","") 

        # Se compara la respuesta del alumno (ans) con la correcta (answer[enum][0])
        # La comparación se realiza en minúsculas.
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

            # Se obtiene la retroalimentación para la pregunta correspondiente.
            feedback = self.read(enum, '.__fee_')

            # Si el ejercicio (enum) contiene retroalimentación, se imprime en pantalla.
            # En otro caso no se imprime nada.
            if feedback[enum][0] != None and self.__verb >= 1:            
                print(Fore.RED + feedback[enum][0])
            else: 
                print()
            print(Fore.RESET + self.__line_len*'-')

            # Se lanza una excepción con la información correspondiente.
            raise AssertionError from None

    def eval_expression(self, enum, ans):
        """
        Evalúa una expresión simbólica escrita en formato Python+Sympy.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo.
        value = self.read(enum)

        # Se convierte la respuesta correcta (value) en formato SymPy.
        problema = sy.sympify(value[enum][0])

        # Se compara la respuesta correcta (problema) con la respuesta
        # del alumno (ans) usando la función equals().
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

            # Se obtiene la retroalimentación para la pregunta correspondiente.
            feedback = self.read(enum, '.__fee_')   

            # Si el ejercicio (enum) contiene retroalimentación, se imprime en pantalla.
            # En otro caso no se imprime nada.
            if feedback[enum][0] != None and self.__verb >= 1:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()
            print(Fore.RESET + self.__line_len*'-')

            # Se lanza una excepción con la información correspondiente.
            raise AssertionError from None

    def eval_numeric(self, enum, ans):
        """
        Evalúa una respuesta numérica que puede ser un número o un arreglo de números.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo. Recordemos que
        # Parquet escribe listas y tuplas en forma de np.ndarray, por lo que
        # al recuperarlas del archivo vienen en formato np.ndarray en 1D.
        value = self.read(enum)        
        correct = value[enum][0]
        
        try:
            # Cuando la respuesta es un np.ndarray:
            if isinstance(ans, np.ndarray):
                # Para comparar la respuesta del alumno (ans) con la respuesta correcta (correct) 
                # debemos usar la función flatten(), para que ambos arreglos sean lineales (1D).
                # Utilizamos la función np.allcose() para comparar los arreglos elemento por elemento
                # dentro de una tolerancia definida (rtol=1e-05, atol=1e-08). Si hay NaN´s en los arreglos
                # la función devuelve True si están en el mismo lugar dentro de los arreglos.
                if not np.allclose(correct, ans.flatten(), equal_nan=True):
                    # Cuando la condición anterior se cumple (NO SON IGUALES), se lanza una excepción
                    # y se ubica el primer lugar de los arreglos donde hay diferencia en los arreglos.
                    # La función assert_equal() requiere de listas.
                    assert_equal(list(correct), list(ans.flatten()))
                    
            elif isinstance(ans, list):
                if not np.allclose(list(correct), ans):
                    assert_equal(list(correct), list(ans.flatten()))
                        
            elif isinstance(ans, tuple):
                if not np.allclose(tuple(correct), ans):
                    assert_equal(tuple(correct), ans)
                    
            elif isinstance(ans, complex):
                if not np.allclose(list(correct), [ans.real, ans.imag]):
                    assert_equal(list(correct), [ans.real, ans.imag])

            elif isinstance(ans, int) or isinstance(ans, float) or isinstance(ans, bool):
                if not np.allclose(correct, ans):
                    assert_equal(correct, ans)
            else:
                print('Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
                
        except AssertionError as info:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Ocurrió un error en tus cálculos.')
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Hint:', end = ' ')

            # Se obtiene la retroalimentación para la pregunta correspondiente.            
            feedback = self.read(enum, '.__fee_')

            # Si el ejercicio (enum) contiene retroalimentación, se imprime en pantalla.
            # En otro caso no se imprime nada.
            if feedback[enum][0] != None and self.__verb >= 1:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()            
            print(Fore.RESET + self.__line_len*'-')

            # Se imprime la información del error.
            if self.__verb >= 2:
                print(info)

            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
        else:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.GREEN + 'Tu resultado es correcto.')
            print(Fore.RESET + self.__line_len*'-')            

    def eval_datastruct(self, enum, ans):
        """
        Evalúa una respuesta numérica que puede ser un número o un arreglo de números.
        
        Parameters
        ----------
        enum: string
        Número de pregunta.
        
        ans: string
        Respuesta del alumno.
        """
        # Se obtiene la respuesta correcta del archivo. Recordemos que
        # Parquet escribe listas y tuplas en forma de np.ndarray, por lo que
        # al recuperarlas del archivo vienen en formato np.ndarray en 1D.
        value = self.read(enum)        
        correct = value[enum][0]
        
        try:
            if isinstance(ans, np.ndarray):
                # Para comparar la respuesta del alumno (ans) con la respuesta correcta (correct) 
                # debemos usar la función flatten(), para que ambos arreglos sean lineales (1D).
                # La función assert_equal() requiere de listas.
                assert_equal(set(correct), set(ans.flatten()))
                    
            elif isinstance(ans, list) or isinstance(ans, tuple) or isinstance(ans, set):
                assert_equal(set(correct), set(ans))
                
            elif isinstance(ans, dict):
                n = len(ans)
                ans = np.array([list(ans.keys()), list(ans.values())]).flatten()
                k1 = correct[0:n]
                v1 = correct[n:]
                k2 = ans[0:n]
                v2 = ans[n:]
                
                assert_equal(list(k1), list(k2)) # Comparamos keys
                assert_equal(list(v1), list(v2)) # Comparamos values
                    
            else:
                print('Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
            
        except AssertionError as info:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Ocurrió un error.')
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + 'Hint:', end = ' ')

            # Se obtiene la retroalimentación para la pregunta correspondiente.            
            feedback = self.read(enum, '.__fee_')

            # Si el ejercicio (enum) contiene retroalimentación, se imprime en pantalla.
            # En otro caso no se imprime nada.
            if feedback[enum][0] != None and self.__verb >= 1:            
                print(Fore.RED + feedback[enum][0])
            else:
                print()            
            print(Fore.RESET + self.__line_len*'-')

            # Se imprime la información del error.
            if self.__verb >= 2:
                print(info)

            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
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
        self.__verb = 0

    @property
    def answers(self):
        return self.__answers
    
    @property
    def feedback(self):
        return self.__feedback

    @property
    def verb(self):
        return self.__verb
        
    @verb.setter
    def verb(self, verb):
        self.__verb = verb
             
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

        self.write('0', self.__verb)
        
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

    #---------------------- CREACIÓN DEL ARCHIVO DE RESPUESTAS
    print()
    file_answer = FileAnswer('CURSO', 'Tema1', server = 'local')
    file_answer.verb = 2

    #---------------------- CONSTRUCCIÓN DE RESPUESTAS
    opcion = 'c'
    derivada = 'x**2'

    t = np.linspace(0,1,10)
    w = np.sin(t)

    matriz_np = np.array([[0.10, -1.],[0.30,-1.]] )
    array_np = np.array([-200, 20])
    
    flotante = 0.0
    entero = 1
    complejo = 1 + 5j
    logico = True
    
    lista_num = [0, 1, 3.4]
    tupla_num = (1.2, 3.1416, np.pi)
    conjunto_num = {3, 5, 6, 2, 9,8}

    lista = ['luis', 'miguel', 'delacruz']
    tupla = ('a', 'b', 'c')
    conjunto = {'a', 'b', 'c'}
    diccionario = {'k1':3.446, 'k2':5.6423, 'k3':2.234324}

    x = sy.Symbol('x')
    y = sy.Symbol('y')
    A, B, C = matriz_np, array_np, flotante

    array_no_num = np.array(['a', 'x', 'w'])
    
    forma_cuadratica = 0.5 * A[0,0] * x**2 + 0.5 * A[1,1] * y**2 + 0.5 * (A[0,1]+A[1,0])* x * y - B[0] * x - B[1] * y + C

    #---------------------- ALMACENAMIENTO DE RESPUESTAS
    file_answer.write('1', opcion, 'Las opciones válidas son ...')
    file_answer.write('2', derivada, 'Checa las reglas de derivación')
    
    file_answer.write('3a', t, 'Deberías checar ...')
    
    mensaje ="""Puedes poner mucho texto y ver que sucede en la impresión del hint,
    quizá es necesario usar triples comillas"""
    file_answer.write('3b', w, mensaje)

    file_answer.write('4', matriz_np, 'Checa las entradas de la matriz A')
    file_answer.write('5', array_np, 'Checa las entradas del vector B')
    
    file_answer.write('6', flotante, 'Checa el valor de flotante')
    file_answer.write('7', entero, 'Checa el valor de entero')
    file_answer.write('8', complejo, 'Checa el valor de complejo')
    file_answer.write('9', logico, 'Checa  logico')
    
    file_answer.write('10', lista_num, 'Checa la lista numérica')
    file_answer.write('11', tupla_num, 'Checa la tupla numérica')
    file_answer.write('12', conjunto_num, 'No es posible usar conjuntos numéricos')

    file_answer.write('13', lista, 'Checa la lista')
    file_answer.write('14', tupla, 'Checa la tupla')
    file_answer.write('15', conjunto, 'Checa la conjunto')
    file_answer.write('16', diccionario, 'Checa la diccionario')
    file_answer.write('17', array_no_num, 'Checa el nd.array')

    file_answer.write('18', str(forma_cuadratica),'Revisa tus operaciones algebráicas para calcular f(x)')
    file_answer.to_file('1')

    #---------------------- MOSTRAMOS EL ARCHIVO DE RESPUESTAS
    ans_df2 = pd.read_parquet('../utils/.ans/Tema1/.__ans_1') # Se lee en un DataFrame
    print('-'*40)
    for i in ans_df2.columns:
        print("{} --> {}".format(i, ans_df2[i][0]))
    print('-'*40)

    fee_df2 = pd.read_parquet('../utils/.ans/Tema1/.__fee_1') # Se lee en un DataFrame
    fee_df2
    print('-'*40)

    #---------------------- EVALUACIÓN DE LAS RESPUESTAS
    quizz = Quizz('1', 'CURSO', 'Tema1', 'local')

    print('\nVerbosidad de la ayuda : {} \n'.format(quizz.verb))

    print('Opción')
    quizz.eval_option('1', 'c')
    
    x = sy.Symbol('x')
    resultado = x*x
    display(resultado)

    print('Expresión')
    quizz.eval_expression('2', resultado)

    quizz.eval_numeric('3a', t)
    quizz.eval_numeric('3b', w)
    
    print('Matriz')
    quizz.eval_numeric('4', matriz_np)
    print('Array')
    quizz.eval_numeric('5', array_np)
    
    print('Flotante')
    quizz.eval_numeric('6', flotante)
    print('Entero')
    quizz.eval_numeric('7', entero)
    print('Complejo')
    quizz.eval_numeric('8', complejo)
    print('Logico')
    quizz.eval_numeric('9', logico)
    
    print('Lista numérica')
    quizz.eval_numeric('10', lista_num)
    print('Tupla numérica')
    quizz.eval_numeric('11', tupla_num)    
#    print('Conjunto numérico')
#    quizz.eval_numeric('12', conjunto_num)

    print('Lista')
    quizz.eval_datastruct('13', lista)
#    quizz.eval_datastruct('13', ['delacruz', 'luis', 'miguel'])

    print('Tupla')
    quizz.eval_datastruct('14', tupla)
#    quizz.eval_datastruct('14', ('c', 'b', 'a'))

    print('Conjunto')
    quizz.eval_datastruct('15', conjunto)
#    quizz.eval_datastruct('15', {'c', 'b', 'a'})

    print('Diccionario')
    quizz.eval_datastruct('16', diccionario)
#    quizz.eval_datastruct('16', {'k1':3.446, 'k2':5.6423, 'k3':3.234324})
    
    print('nd.array NO NUMÉRICO')
    quizz.eval_datastruct('17', array_no_num)
#    quizz.eval_datastruct('17', np.array(['x', 'a', 'w']))

    print('Expresión más compleja')
    quizz.eval_expression('18', forma_cuadratica)
    

