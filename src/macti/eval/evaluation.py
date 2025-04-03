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

class Quiz():
    def __init__(self, qnum, course, server = 'hub', path_from_read = None):
        """
        Clase para la evaluación de ejercicios.
        
        Parameters
        ----------
        qnum : str
            Nombre del quiz.

        course : str
            Nombre del directorio del curso.
        
        server: str
            Puede tener cualquiera de los dos siguientes valores:
            'local' cuando los datos (answers & feedback) se almacenan en un directorio local.
            'hub' cuando los datos (answers & feedback) se almacenan en un directorio global del hub.

        path_from_read: string
            Ruta de donde se leerán las respuestas y la retroalimentación. 
            NOTA: Esta es una característica en proceso de desarrollo.
        """
        self.__server = server
        self.__path_from_read = path_from_read
        self.__course_path = ''

        # Separador dependiendo de la plataforma
        self.__platform = platform.system()
        sep = '\\' if self.__platform == 'Windows' else '/'
        
        # Obtenemos el nombre a partir del path actual
        # Se asume que se ejecuta dentro de course/topic/
        self.__path = os.getcwd()
        self.__course = course # sin separador
        self.__topic = self.__path.split('/')[-1] + sep

        if server == 'local':
            # Construcción de una lista con los componentes de la ruta absoluta
            # a partir de donde se ejecuta la notebook
            abs_path = os.getcwd().split(sep = sep)  # Ruta absoluta

            # Obtención del índice donde está el nombre del curso dentro de la lista abs_path
            index_co = abs_path.index(self.__course)

            # Construcción del path del curso
            for i in abs_path[0:index_co+1]:
                self.__course_path += i + sep
        
        self.__course += sep  # Agregamos el separador
        self.__ans = '.ans' + sep # .ans/
        self.__qnum = qnum # Número del quiz

        # Verbosity
        self.__verb = self.read('0', verb = True)['0'][0]

        self.__line_len = 40

    @property
    def verb(self):
        return self.__verb
        
    @property
    def server(self):
        return self.__server
    
    @server.setter
    def server(self, server):
        self.__server = server
        
    def read(self, enum, name = '.__ans_', verb = False):
        """
        Lectura de la respuesta del ejercicio con número enum. 
        
        Esta lectura se realiza del archivo en donde se encuentran las respuestas de todo el quiz.
        El archivo está en formato parquet y las respuestas se almacenan en columnas y en un solo renglón.
        El identificador de la columna corresponde con el número del ejercicio enum.

        Parameters
        ----------
        enum: str
            Número del ejercicio dentro del quiz.
        
        name: string
            Nombre del archivo donde se guardan las respuestas, por omisión es: ".__ans_".

        verb: bool
            Es False siempre, excepto cuando se lee la verbosidad.
        
        Returns
        -------
            Regresa la respuesta correcta al ejercicio enum almacenada en el archivo.
        """
        try:
            # Solo se permite enum == '0' cuando se lee la verbosidad (verb == True)
            if enum == '0' and not verb:
                raise ValueError from None

        except ValueError:
            print('NO EXISTE LA RESPUESTA. No está permitido usar \'{}\' para identificar un ejercicio \n'.format(enum))
        else:   
            # Se agrega el número del quiz correspondiente al nombre del archivo de respuestas. 
            filename = name + self.__qnum

            if self.__server == 'local' and self.__path_from_read == None:
                path = self.__course_path + self.__ans + self.__topic
                stream = path + filename
                
            elif self.__server == 'hub' and self.__path_from_read == None: 
                # Directorio global en el hub
                path = '/usr/local/share/nbgrader/exchange/' + self.__course + self.__ans + self.__topic
                stream = path + filename 
                
            elif self.__path_from_read != None:
                path = self.__path_from_read + sep + self.__topic
                
    #        elif self.__server == 'macti':
                # Se utiliza pkg_resources para obtener el directorio de instalación de la biblioteca.
                # /opt/conda/lib/python3.11/site-packages/macti/data/course/.ans/topic/
    #            path = '/data/' + self.__course + self.__ans + self.__topic
    #            stream = pkg_resources.resource_stream('macti', path + filename)
                
            else:
                print('Opciones inválidas. Revisa la declaración de Quiz()')

            # Lectura del archivo en formato parquet, se regresa en un DataFrame.
            return (pd.read_parquet(stream, columns=[enum]))
            
    def eval_option(self, enum, ans):
        """
        Evalúa una pregunta de opción múltiple. 
        
        Cuando la respuesta es incorrecta lanza un excepción.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
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
            print(Fore.GREEN + enum + ' | Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.GREEN + ', es correcta.')
            print(Fore.RESET + self.__line_len*'-')
        else:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + enum + ' | Tu respuesta:', end = ' ')
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
        enum: str
            Número de pregunta.
        
        ans: str
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
            print(Fore.GREEN + enum + ' | Tu respuesta:')
            display(ans)
            print(Fore.GREEN + 'es correcta.')
            print(Fore.RESET + self.__line_len*'-')
        else:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + enum + ' | Tu respuesta:')
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
        enum: str
            Número de pregunta.
        
        ans: str
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
                    assert_equal(list(correct), ans)
                        
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
                print(enum + ' | Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
                
        except AssertionError as info:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + enum + ' | Ocurrió un error en tus cálculos.')
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
            print(Fore.GREEN + enum + ' | Tu resultado es correcto.')
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

            elif isinstance(ans, str):
                assert_equal(correct, ans)
            
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
            print(Fore.RED + enum + ' | Ocurrió un error.')
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
            print(Fore.GREEN + enum + ' | Tu resultado es correcto.')
            print(Fore.RESET + self.__line_len*'-') 

    def eval_ordered_datastruct(self, enum, ans):
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
                assert_equal(list(correct), list(ans.flatten()))
            
            elif isinstance(ans, list) or isinstance(ans, tuple):
                assert_equal(list(correct), list(ans))
                    
            else:
                print('Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
            
        except AssertionError as info:
            print(Fore.RESET + self.__line_len*'-')
            print(Fore.RED + enum + ' | Ocurrió un error.')
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
            print(Fore.GREEN + enum + ' | Tu resultado es correcto.')
            print(Fore.RESET + self.__line_len*'-') 


class FileAnswer():
    def __init__(self, 
                 path_to_store = None):
        """
        Clase para la escritura de las respuestas a los ejercicios.
        Se asume que se ejecuta dentro del directorio de un tema del curso:
        course/topic.
        
        Parameters
        ----------
        path_to_store: string
        Ruta donde se guardarán las respuestas y la retroalimentación.
        Por omisión, los datos (answers & feedback) se almacenan en el directorio:.
        $PWD/course/.ans/topic/. Las respuestas/retroalimentación para cada quiz 
        se almacenan en archivos diferentes, veáse la función to_file().
        
        """
        self.__path_to_store = path_to_store
        self.__platform = platform.system()
        self.__course_path = ''

        # Separador dependiendo de la plataforma
        sep = '\\' if self.__platform == 'Windows' else '/'
        
        # Obtenemos el nombre a partir del path actual
        # Se asume que se ejecuta dentro de course/topic/
        self.__path = os.getcwd()
        self.__course = self.__path.split('/')[-2] # sin separador
        self.__topic = self.__path.split('/')[-1] + sep

        # Obtención del directorio del curso
        abs_path = os.getcwd().split(sep = sep)
        index_co = abs_path.index(self.__course)
        for i in abs_path[0:index_co+1]:
            self.__course_path += i + sep
  
        self.__course += sep  # Agregamos el separador
        self.__ans = '.ans' + sep # .ans/
        
        self.__exernum = []
        self.__answers = []
        self.__feedback = []

        # Por omisión la verbosidad es igual a 2, es decir toda la ayuda posible al alumno
        self.__verb = 2

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
             
    def write(self, enum, ans, feed=None, verb = False):
        """
        Esta función escribe una respuesta en una lista (self.__answer) y la retroalimentación de 
        esta respuesta en otra lista (self.__feedback). El número del ejercicio se almacena en 
        otra lista (self.__exernum). Si la respuesta es nueva, se agrega un elemento a la lista, 
        si el ejercicio ya existía entonces se sustituye.

        Parameters
        ----------
        enum: string
        Cadena con el identificador del ejercicio. Este parámetro no puede ser '0' debido
        a que ese identificador está destinado a almacenar la verbosidad de la retroalimentación.

        ans: 
        Objeto que contiene la respuesta, puede ser de cualquier tipo soportado por la
        biblioteca (str, float, int, complex, boolean, ndarray, list, tuple, dict

        feed: string
        Cadena con la retroalimentación del ejercicio. Por omisión está vacía.

        verb: bool
        Es False siempre, excepto cuando se escribe la verbosidad.
        """
        try:
            # Solo se permite enum == '0' cuando se almacena la verbosidad (verb == True)
            if enum == '0' and not verb:
                raise ValueError from None

        except ValueError:
            print('RESPUESTA NO ALMACENADA. No está permitido usar el valor \'{}\' para identificar un ejercicio.\n'.format(enum))
            
        else:
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
        """
        Escribe las respuestas y la retroalimentación en un archivo tipo parquet.

        Parameters
        ----------
        qnum: string
        Es una cadena que proporciona el número del quiz. La cadena debe ser una
        cadena, se recomienta usar: '1', '2', ...
        """
        # Se define la verbosidad de la retroalimentación de cada respuesta. 
        self.write('0', self.__verb, verb = True)
        
        ans_df = pd.DataFrame([self.__answers], columns=self.__exernum)
        feed_df = pd.DataFrame([self.__feedback], columns=self.__exernum) 
        
        filename = '.__ans_' + qnum

        if self.__path_to_store == None:
            # Se almacena en el directorio course/.ans/topic
            path = self.__course_path + self.__ans + self.__topic
        else:
            # Se almacena en el directorio course/topic
            path = self.__path_to_store + sep + self.__topic
        
        if not os.path.exists(path):
            print('Creando el directorio :{}'.format(path))
            os.makedirs(path, exist_ok=True)
        else:
            print('El directorio :{} ya existe'.format(path))
        
        ans_df.to_parquet(path + '.__ans_' + qnum, compression='gzip')
        feed_df.to_parquet(path + '.__fee_' + qnum, compression='gzip')
        print('Respuestas y retroalimentación almacenadas.')
            
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    #---------------------- CREACIÓN DEL ARCHIVO DE RESPUESTAS
    print()
    file_answer = FileAnswer()
#    file_answer.verb = 0

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

    file_answer.write('0', 'a', 'Opción inválida')

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
    ans_df2 = pd.read_parquet('../utils/.ans/macti/.__ans_1') # Se lee en un DataFrame
    print('-'*40)
    for i in ans_df2.columns:
        print("{} --> {}".format(i, ans_df2[i][0]))
    print('-'*40)

    fee_df2 = pd.read_parquet('../utils/.ans/macti/.__fee_1') # Se lee en un DataFrame
    fee_df2
    print('-'*40)

    #---------------------- EVALUACIÓN DE LAS RESPUESTAS
    quiz = Quiz('1', 'macti_lib', 'local')

    print('\nVerbosidad de la ayuda : {} \n'.format(quiz.verb))

#    print('¿qué pasa si uso enum == 0?')
#    quiz.eval_datastruct('0', 'a')
    
    print('Opción')
    quiz.eval_option('1', 'c')
    
    x = sy.Symbol('x')
    resultado = x*x
    display(resultado)

    print('Expresión')
    quiz.eval_expression('2', resultado)

    quiz.eval_numeric('3a', t)
    quiz.eval_numeric('3b', w)
    
    print('Matriz')
    quiz.eval_numeric('4', matriz_np)
    print('Array')
    quiz.eval_numeric('5', array_np)
    
    print('Flotante')
    quiz.eval_numeric('6', flotante)
    print('Entero')
    quiz.eval_numeric('7', entero)
    print('Complejo')
    quiz.eval_numeric('8', complejo)
    print('Logico')
    quiz.eval_numeric('9', logico)
    
    print('Lista numérica')
    quiz.eval_numeric('10', lista_num)
    print('Tupla numérica')
    quiz.eval_numeric('11', tupla_num)    
#    print('Conjunto numérico')
#    quiz.eval_numeric('12', conjunto_num)

    print('Lista')
    quiz.eval_datastruct('13', lista)
#    quiz.eval_datastruct('13', ['delacruz', 'luis', 'miguel'])

    print('Tupla')
    quiz.eval_datastruct('14', tupla)
#    quiz.eval_datastruct('14', ('c', 'b', 'a'))

    print('Conjunto')
    quiz.eval_datastruct('15', conjunto)
#    quiz.eval_datastruct('15', {'c', 'b', 'a'})

    print('Diccionario')
    quiz.eval_datastruct('16', diccionario)
#    quiz.eval_datastruct('16', {'k1':3.446, 'k2':5.6423, 'k3':3.234324})
    
    print('nd.array NO NUMÉRICO')
    quiz.eval_datastruct('17', array_no_num)
#    quiz.eval_datastruct('17', np.array(['x', 'a', 'w']))

    print('Expresión más compleja')
    quiz.eval_expression('18', forma_cuadratica)
    

