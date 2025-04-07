"""
@author: Luis M. de la Cruz [Updated on Tue Dec 12 15:32:38 2023].
"""

# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
#from nose.tools import assert_equal
import numpy as np
import pandas as pd
import sympy as sy
import os, sys, platform

#import pkg_resources
from IPython.display import display, Latex

class FileAnswer():
    def __init__(self):
        """
        Clase para la escritura de las respuestas a los ejercicios.
        
        Se asume que se ejecuta dentro del directorio de un tema del curso
        por ejemplo course/topic.
        
        Los datos (answers & feedback) se almacenan en el directorio:.
        $PWD/course/.ans/topic/. 
        
        Las respuestas/retroalimentación para cada quiz 
        se almacenan en archivos diferentes, veáse la función to_file().
        """
        cp, to = os.path.split(os.getcwd()) # Extracción del path del curso y del tema
        self.__course_path = cp + os.sep # Agregamos el separador a la ruta del curso 
        self.__topic = to + os.sep       # Agregamos el separador al nombre del tema

        # Construcción del path para los archivos de respuestas
        self.__ans_path = self.__course_path + ".ans" + os.sep + self.__topic

        # Listas para almacenar los números de las respuestas, las respuestas
        # y la retroalimentación.
        self.__exernum = []
        self.__answers = []
        self.__feedback = []

        # Por omisión la verbosidad es igual a 2, es decir toda la ayuda posible al alumno
        self.__verb = 2

        # Cadena final del nombre de los archivos, se actualiza en la función self.to_file()
        self.__quiz_num = ""

    @property
    def quiz_num(self):
        return self.__quiz_num
        
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
        Escribe la respuest y la retroalimentación de una pregunta.
        
        Esta función escribe una respuesta en una lista (self.__answer) y la retroalimentación de 
        esta respuesta en otra lista (self.__feedback). El número del ejercicio se almacena en 
        otra lista (self.__exernum). Si la respuesta es nueva, se agrega un elemento a la lista, 
        si el ejercicio ya existía entonces se sustituye.

        Parameters
        ----------
        enum: str
            Cadena con el identificador del ejercicio. Este parámetro no puede ser '0' debido
            a que ese identificador está destinado a almacenar la verbosidad de la retroalimentación.

        ans: str, float, int, complex, boolean, ndarray, list, tuple, dict
            Objeto que contiene la respuesta, puede ser de cualquier tipo soportado por la
            biblioteca (str, float, int, complex, boolean, ndarray, list, tuple, dict)

        feed: str
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
                    if ans.dtype == complex:
                        # Preprocesamiento especial para números complejos.
                        self.__answers[index] = np.array([[c.real, c.imag] for c in ans.flatten()]).flatten()
                    else:
                        self.__answers[index] = ans.flatten() # almacenamos los arreglos de numpy en 1D
                        
                elif isinstance(ans, dict):
                    # Extraemos cada key y value del diccionario y almacenamos en 
                    # columnas separadas lo siguiente:
                    # - La longitud del diccionario
                    # - Las keys como un arreglo
                    # - Cada valueo como un arreglo
                    dict_len = len(ans)
                    keys = np.array(list(ans.keys()))
                    enum_l = enum + "_len"
                    enum_k = enum + "_key"

                    self.write(enum_l, dict_len, f"{feed}. \n{enum_l} Longitudes de los diccionarios incompatibles.")
                    self.write(enum_k, keys, f"{feed}. \n{enum_k} Keys del diccionario incompatibles.")

                    for i, v in enumerate(ans.values()):
                        enum_v = enum + "_val_" + str(i)        
                        self.write(enum_v, v, f"{feed}. \n{enum_v} Valor en el diccionario incorrecto.")
                    
                elif isinstance(ans, set):
                    self.__answers[index] = np.array(list(ans)).flatten()
                    
                elif isinstance(ans, list) or isinstance(ans, tuple):
                    self.__answers[index] = np.array(ans).flatten()
                    
                elif isinstance(ans, complex):
                    # Almacenamos la parte real e imaginaria del número complejo en una lista.
                    self.__answers[index] = [ans.real, ans.imag]
                    
                else:
                    self.__answers[index] = ans
                    
                self.__feedback[index] = feed 
                
            else: # Si el ejercicio es nuevo, lo agregamos
                
                # Todos los arreglos de numpy se deben almacenar en formato unidimensional
                if isinstance(ans, np.ndarray):
                    if ans.dtype == complex:
                        # Preprocesamiento especial para números complejos.
                        self.__answers.append(np.array([[c.real, c.imag] for c in ans.flatten()]).flatten())
                    else:
                        self.__answers.append(ans.flatten()) # almacenamos los arreglos de numpy en 1D   
                        
                elif isinstance(ans, dict): 
                    # Extraemos cada key y value del diccionario y almacenamos en 
                    # columnas separadas lo siguiente:
                    # - La longitud del diccionario
                    # - Las keys como un arreglo
                    # - Cada valueo como un arreglo
                    dict_len = len(ans)
                    keys = np.array(list(ans.keys()))
                    enum_l = enum + "_len"
                    enum_k = enum + "_key"
                    self.write(enum_l, dict_len, f"{feed}. \n{enum_l} Longitudes de los diccionarios incompatibles.")
                    self.write(enum_k, keys, f"{feed}. \n{enum_k} Keys del diccionario incompatibles.")

                    for i, v in enumerate(ans.values()):
                        enum_v = enum + "_val_" + str(i)        
                        self.write(enum_v, v, f"{feed}. \n{enum_v} Valor en el diccionario incorrecto.")
                    
                elif isinstance(ans, set):
                    self.__answers.append(np.array(list(ans)).flatten())
                    
                elif isinstance(ans, list) or isinstance(ans, tuple):
                    self.__answers.append(np.array(ans).flatten())
                    
                elif isinstance(ans, complex):
                    # Parquet no soporta complejos, dividimos en parte real e imaginaria
                    self.__answers.append([ans.real, ans.imag])    
                    
                else:
                    self.__answers.append(ans)

                if not isinstance(ans, dict):
                    self.__exernum.append(enum)  # Se almacena el número de la pregunta
                    self.__feedback.append(feed) # Se almacena la retroalimentación de la pregunta
    
    def to_file(self, qnum):
        """
        Escribe las respuestas y la retroalimentación en un archivo tipo parquet.

        Parameters
        ----------
        qnum: str
            Es una cadena que identifica a una pregunta del quiz. 
            Se recomienta usar: '1', '2', ...
        """
        # Cadena final del nombre de los archivos de respuestas y de retroalimentación
        self.__quiz_num = qnum
        
        # Se define la verbosidad de la retroalimentación de cada respuesta. 
        self.write('0', self.__verb, verb = True)
        
        if not os.path.exists(self.__ans_path):
            print('Creando el directorio :{}'.format(self.__ans_path))
            os.makedirs(self.__ans_path, exist_ok=True)
        else:
            print('El directorio :{} ya existe'.format(self.__ans_path))

        # Creación del archivo de respuestas
        ans_df = pd.DataFrame([self.__answers], columns=self.__exernum)
        ans_df.to_parquet(self.__ans_path + '.__ans_' + qnum, compression='gzip')

        # Creación del archivo de retroalimentación
        feed_df = pd.DataFrame([self.__feedback], columns=self.__exernum) 
        feed_df.to_parquet(self.__ans_path + '.__fee_' + qnum, compression='gzip')
        
        print('Respuestas y retroalimentación almacenadas.')
        
class Quiz():
    def __init__(self, qnum, server = 'hub', spath = ''):
        """
        Clase para la evaluación de ejercicios.
        
        Parameters
        ----------
        qnum : str
            Nombre del quiz.

        course : str
            Nombre del directorio del curso.
        
        server : str
            Puede tener cualquiera de los dos siguientes valores:
            'local' cuando los datos (answers & feedback) se almacenan en un directorio local.
            'hub' cuando los datos (answers & feedback) se almacenan en un directorio global del hub.

        spath : str
            Directorio de intercambio de nbgrader. Cuando server = 'hub' esta ruta se debe proporcionar.
        """
        self.__server = server

        # MACTI: '/usr/local/share/nbgrader/exchange/' 
        # OJO: esta ruta debe incluir el caracter '/' al final.
        self.__server_path = "/usr/local/share/nbgrader/exchange/" # spath

        cp, to = os.path.split(os.getcwd()) # Extracción del path del curso y del tema
        self.__course_path = cp + os.sep    # Agregamos el separador a la ruta del curso
        self.__course = cp.split(os.sep)[-1] + os.sep # Nombre del curso con separador
        self.__topic = to + os.sep       # Agregamos el separador al nombre del tema

        # Construcción del path para los archivos de respuestas
        if self.__server == 'local':
            self.__ans_path = self.__course_path + ".ans" + os.sep + self.__topic
        elif self.__server == 'hub':
            self.__ans_path = self.__server_path + self.__course + ".ans" + os.sep + self.__topic
        
        self.__quiz_num = qnum # Número del quiz

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
            filename = name + self.__quiz_num
            stream = self.__ans_path + filename

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

    def __test_array(self, a, b):
        """
        Compara dos valores numéricos o arreglos de valores numéricos.
        
        Para comparar la respuesta del alumno (b) con la respuesta correcta (a) 
        debemos usar la función flatten(), para que ambos arreglos sean lineales (1D).
        Utilizamos la función np.allcose() para comparar los arreglos elemento por elemento
        dentro de una tolerancia definida (rtol=1e-05, atol=1e-08). Si hay NaN´s en los arreglos
        la función devuelve True si están en el mismo lugar dentro de los arreglos.

        Parameters
        ----------
        a : ndarray
            Respuesta correcta.

        b : ndarray
            Respuesta del alumno.

        Returns
        -------
        AssertionError cuando hay diferencia entre a y b.
        """
        b = b.flatten()
        msg = ""
        if len(a) == len(b):
            if not np.allclose(a, b, equal_nan=True):
                first = int(np.where((a == b) == False)[0][0]) # primer elemento donde hay diferencia
    
                if self.__verb >= 1:
                    # Mensaje de ayuda
                    msg = f"\n Primer elemento con error: [{first:>5d}]\n valor correcto {a[first]}, \n valor calculado {b[first]}\n"
                    
        else:
            # Cuando la longitud de los arreglos es distinta
            msg = f"\nLongitud correcta={len(a)}\nLongitud de tu respuesta={len(b)}"
                
        return msg
            
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

        msg = ""

        try:
            if isinstance(ans, np.ndarray):
                if ans.dtype == complex:
                    # Preprocesamiento especial para números complejos.
                    b = np.array([[c.real, c.imag] for c in ans.flatten()]).flatten()
                    msg = self.__test_array(correct, b)
                    np.testing.assert_allclose(correct, b)
                else:                        
                    msg = self.__test_array(correct, ans)
                    np.testing.assert_allclose(correct, ans)

            elif isinstance(ans, list) or isinstance(ans, tuple):
                b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                msg = self.__test_array(correct, b)
                np.testing.assert_allclose(correct, b)

            elif isinstance(ans, set):
                b = np.array(list(ans))
                msg = self.__test_array(correct, b)
                np.testing.assert_allclose(correct, b)

            elif isinstance(ans, complex):
                a = np.array([complex(correct[0], correct[1])])
                b = np.array([ans])
                msg = self.__test_array(a, b)
                np.testing.assert_allclose(a, b)

            elif isinstance(ans, int) or isinstance(ans, float) or isinstance(ans, bool):
                msg = self.__test_array(np.array([correct]), np.array([ans]))
                np.testing.assert_allclose(correct, ans)

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
                print(Fore.RED + feedback[enum][0] + msg)
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

    def eval_dict(self, enum, ans):
        """
        Evalúa una respuesta numérica almacenada en un diccionario.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
            Respuesta del alumno.
        """
        enum_copy = enum
        msg = ""       
        try:
            if isinstance(ans, dict):
                dict_len = len(ans)
                keys = np.array(list(ans.keys()))

                # Se obtiene la longitud del diccionario y se compara con la respuesta del alumno.
                enum = enum_copy + "_len"
                value = self.read(enum)        
                correct = value[enum][0]
                a = np.array([correct])
                b = np.array([dict_len])
                msg = self.__test_array(a, b)
                np.testing.assert_allclose(a, b)
                
                # Se obtienen los keys del diccionario y se comparan con la respuesta del alumno.
                enum = enum_copy + "_key"
                value = self.read(enum)        
                correct = value[enum][0]
                b = np.array(keys)
                msg = self.__test_array(correct, b)
                np.testing.assert_allclose(correct, b)

                # Se obtienen los valores del diccionario, uno a uno, y se comparan con la respuesta del alumno.
                for i, v in enumerate(ans.values()):
                    enum = enum_copy + "_val_" + str(i)
                    value = self.read(enum)        
                    correct = value[enum][0]
                    if isinstance(v, set):
                        v = list(v)
                    a = np.array([correct]).flatten() # cuando los valores son listas, se requiere flatten()
                    b = np.array([v]).flatten() 
                    msg = self.__test_array(a, b)
                    np.testing.assert_allclose(a, b)

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
                print(Fore.RED + feedback[enum][0] + msg)
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
            


            
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    #----- CREACIÓN DE RESPUESTAS
    
    opcion = 'c'
    
    # Símbolos de sympy para cálculo simbólico
    x = sy.Symbol('x')
    y = sy.Symbol('y')
    # Función simbólica
    derivada = x*x
    # Forma cuadrática
    matriz_np = np.array([[0.10, -1.],[0.30,-1.]] )
    array_np = np.array([-200, 20])
    A, B, C = matriz_np, array_np, 0.0
    forma_cuadratica = 0.5 * A[0,0] * x**2 + 0.5 * A[1,1] * y**2 + 0.5 * (A[0,1]+A[1,0])* x * y - B[0] * x - B[1] * y + C
    
    flotante = 0.1
    entero = 1
    complejo = 1 + 5j
    logico = True
    w = np.sin(np.linspace(0,1,10))
    lista_num = [0, 1, 3.4]
    tupla_num = (1.2, 3.1416, np.pi)
    conjunto_num = {1, 3, 2, 6, 5, 4}
    diccionario_num = {1:3.446, 2:5.6423, 3:2.234324}
    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564], 3:[2.234324, 5.65645]}

    arreglo_complejo = np.array([1j,2j,3j,4j,5j])
    lista_lista = [[1,2],[3,4]]

    array_no_num = np.array(['a', 'x', 'w'])
    lista = ['luis', 'miguel', 'delacruz']
    tupla = ('a', 'b', 'c')
    conjunto = {'a', 'b', 'c'}
    diccionario= {'k1':'luis', 'k2':'miguel', 'k3':'x'}

    #----- CREACIÓN DEL DATAFRAME DE RESPUESTAS
    
    print("Iniciamos con FileAnswer")
    file_answer = FileAnswer()
#    file_answer.verb = 0 # Se puede cambiar la verbosidad, por omisión es igual 2
    file_answer.write('0', 'a', 'Opción inválida')
    file_answer.write('1', opcion, 'Las opciones válidas son ...')
    
    # OJO: las expresiones de sympy se deben convertir en 'str' antes de escribirse en el archivo
    file_answer.write('2', str(derivada), 'Checa las reglas de derivación')
    file_answer.write('3', str(forma_cuadratica),'Revisa tus operaciones algebráicas para calcular f(x)')

    file_answer.write('4', flotante, 'Checa el valor de flotante')
    file_answer.write('5', entero, 'Checa el valor de entero')
    file_answer.write('6', complejo, 'Checa el valor de complejo')
    file_answer.write('7', logico, 'Checa  logico')
    mensaje ="""Puedes poner mucho texto y ver que sucede en la impresión del hint,
    quizá es necesario usar triples comillas"""
    file_answer.write('8', w, mensaje)
    file_answer.write('9', lista_num, 'Checa la lista numérica')
    file_answer.write('10', tupla_num, 'Checa la tupla numérica')
    file_answer.write('11', conjunto_num, 'Checa los conjuntos numéricos')
    file_answer.write('12', diccionario_num, 'Checa los diccionarios numéricos')
    file_answer.write('13', diccionario_num_list, 'Checa los diccionarios numéricos con valores tipo lista')

    file_answer.write('14', arreglo_complejo, 'Checa el arreglo complejo')
    file_answer.write('15', lista_lista, "Checa la lista de listas")
    file_answer.write('16', lista, "checa la estructura de tipo lista")
    file_answer.write('17', tupla, "checa la estructura de tipo tupla")
    file_answer.write('18', conjunto, "checa la estructura de tipo conjunto")
    file_answer.write('19', diccionario, "checa la estructura de tipo diccionario")

#    file_answer.write('17', array_no_num, 'Checa el nd.array')

    #----- CHECAMOS LAS RESPUESTAS Y LA RETROALIMENTACIÓN
#    print(" CHECAMOS LAS RESPUESTAS Y LA RETROALIMENTACIÓN ")
    
#    print(len(file_answer.answers), "\n", file_answer.answers)
#    print()
#    print(len(file_answer.feedback), "\n", file_answer.feedback)


    #----- ESCRITURA DE LAS RESPUESTAS Y LA RETROALIMENTACIÓN ARCHIVOS.
    
    file_answer.to_file('test01')

    # Recuperación de la información
    ans = pd.read_parquet('../.ans/eval/.__ans_test01')
    fee = pd.read_parquet('../.ans/eval/.__fee_test01')
    print("\n----- RESPUESTAS Y DE RETROALIMENTACIÓN")
    fstr = "Pregunta {}:\n a --> {}\n f --> {}\n"
    [print(fstr.format(i, ans[i][0], fee[i][0])) for i in ans.columns]
    
    #----- CREACIÓN DE LAS EVALUACIONES
    
    print("Quiz number:", file_answer.quiz_num)

    quiz = Quiz(file_answer.quiz_num, 'local')

    print('\nVerbosidad de la ayuda : {} \n'.format(quiz.verb))
    
    print('Opción')
    quiz.eval_option('1', 'c')
    
    print('Expresión')
    quiz.eval_expression('2', derivada)

    print('Expresión más compleja')
    quiz.eval_expression('3', forma_cuadratica)
    
    print('Flotante')
    quiz.eval_numeric('4', flotante)
    print('Entero')
    quiz.eval_numeric('5', entero)
    print('Complejo')
    quiz.eval_numeric('6', complejo)
    print('Logico')
    quiz.eval_numeric('7', logico)
    print('numpy array')
    quiz.eval_numeric('8', w)
    print('Lista numérica')
#    lista_num[-2] =0.001
#    lista_num = [0, 1]
    quiz.eval_numeric('9', lista_num)
    print('Tupla numérica')
#    tupla_num = (1.2, 3.1416, 2*np.pi)
#    tupla_num = (0, 1)
    quiz.eval_numeric('10', tupla_num)    
    print('Conjunto numérico')
#    conjunto_num = {1,2,3,4,5,1}
#    conjunto_num = {1,2,3.5,4,5,6}
    quiz.eval_numeric('11', conjunto_num)
    print('Diccionario numérico')
#    diccionario_num = {1:3.446, 2:5.6423}
#    diccionario_num = {1:3.44, 4:5.6423, 3:2.234324}
#    diccionario_num = {1:3.446, 2:5.642, 3:2.234324}
    quiz.eval_dict('12', diccionario_num)
    print('Diccionario numérico con valores tipo lista')
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564]}
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564], 5:[2.234324, 5.65645]}
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.643, 6.7564], 3:[2.234324, 5.65645]}
    quiz.eval_dict('13', diccionario_num_list)
    print('numpy array complex')
#    arreglo_complejo = np.array([2j,3j,4j,5j])
#    arreglo_complejo = np.array([0j,2j,3j,4j,5j])
    quiz.eval_numeric('14', arreglo_complejo)
    print('Lista de listas')
    quiz.eval_numeric('15', lista_lista)
    
#    print('estructura de datos')
#    quiz.eval_numeric('15', lista)
    
#    print('nd.array NO NUMÉRICO')
#    quiz.eval_datastruct('17', array_no_num)

    #----- MOSTRAMOS LOS ARCHIVO DE RESPUESTAS Y DE RETROALIMENTACIÓN

    # Recuperación de la información
    ans = pd.read_parquet('../.ans/eval/.__ans_test01')
    fee = pd.read_parquet('../.ans/eval/.__fee_test01')
    print("\n----- RESPUESTAS Y DE RETROALIMENTACIÓN")
    fstr = "Pregunta {}:\n a --> {}\n f --> {}\n"
    [print(fstr.format(i, ans[i][0], fee[i][0])) for i in ans.columns]



    

