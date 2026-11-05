"""
@author: Luis M. de la Cruz [Updated on Mon Aug 25 09:30:10 CST 2025].
"""

import os
import sys
import platform
from colorama import Fore
import math
import numpy as np
import pandas as pd
import sympy as sp


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
     
        # Extracción del path del curso y del tema
        cp, to = os.path.split(os.getcwd()) 
        # Construcción del path del directorio para los archivos de respuestas
        self.__ans_path = os.path.join(cp, ".ans", to)

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
        Escribe la respuesta y la retroalimentación de una pregunta.
        
        Esta función escribe una respuesta en una lista (self.__answers) y la retroalimentación de 
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
                    # - Cada value como un arreglo
                    dict_len = len(ans)
                    keys = np.array(list(ans.keys()))
                    enum_l = enum + "_len"
                    enum_k = enum + "_key"

                    # Escribimos la longitud del diccionario
                    self.write(enum_l, dict_len, f"{feed}. \n{enum_l} Longitudes de los diccionarios incompatibles.")
                    # Escribimos la lista de claves
                    self.write(enum_k, keys, f"{feed}. \n{enum_k} Keys del diccionario incompatibles.")
                    # Escribimos cada valor
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

                    # Escribimos la longitud del diccionario
                    self.write(enum_l, dict_len, f"{feed}. \n{enum_l} Longitudes de los diccionarios incompatibles.")
                    # Escribimos la lista de claves
                    self.write(enum_k, keys, f"{feed}. \n{enum_k} Keys del diccionario incompatibles.")
                    # Escribimos cada valor
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

                if not isinstance(ans, dict): # El caso de diccionarios los números de pregunta y la retroalimentación se
                                              # almacenan de forma diferente. Véase la primera opción del 'if'
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
        ans_filename = os.path.join(self.__ans_path, '.__ans_' + qnum)
        # Escritura de las respuestas en formato parquet
        ans_df.to_parquet(ans_filename, compression='gzip')

        # Creación del archivo de retroalimentación
        feed_df = pd.DataFrame([self.__feedback], columns=self.__exernum) 
        feed_filename = os.path.join(self.__ans_path, '.__fee_' + qnum)
        # Escritura de la retroalimentación en formato parquet
        feed_df.to_parquet(feed_filename, compression='gzip')
        
        print('Respuestas y retroalimentación almacenadas.')
        
class Quiz():
    def __init__(self, qnum, course, server = 'hub', spath = ''):
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

        cp, to = os.path.split(os.getcwd()) # Extracción del path del curso y del tema

        # Construcción del path para los archivos de respuestas
        if self.__server == 'local':
            self.__ans_path = os.path.join(cp, ".ans", to)
        elif self.__server == 'hub':
            #_, cn = os.path.split(cp)
            cn = course
            self.__server_path = "/usr/local/share/nbgrader/exchange/" # Ruta en MACTI
            self.__ans_path = os.path.join(self.__server_path, cn, ".ans", to)
        
        self.__quiz_num = qnum # Número del quiz

        # Verbosity
        self.__verb = self.__read('0', verb = True)['0'][0]

        self.__line_len = 40
        self.__line = 40 * chr(0x2015)

    @property
    def verb(self):
        return self.__verb
        
    @property
    def server(self):
        return self.__server
    
    @server.setter
    def server(self, server):
        self.__server = server
        
    def __read(self, enum, name = '.__ans_', verb = False):
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
            stream = os.path.join(self.__ans_path, filename)

            # Lectura del archivo en formato parquet, se regresa en un DataFrame.
            # Solo se lee la columna correspondiente con el identificador 'enum'
            return (pd.read_parquet(stream, columns=[enum]))

    def __print_correct(self, enum, equiz="", ans=""):
        """
        Imprime el mensaje cuando la respuesta es correcta.

        Parameters
        ----------
        enum : str
            Número del ejercicio dentro del quiz.      

        equiz : str
            Tipo de evaluación.
        """
        print(Fore.RESET + self.__line)
        if equiz == "option":
            print(Fore.GREEN + enum + ' | Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.GREEN + ', es correcta.') 
        elif equiz == "expression":
            print(Fore.GREEN + enum + ' | Tu respuesta:')
            display(ans)
            print(Fore.GREEN + 'es correcta.')
        else:
            print(Fore.GREEN + enum + ' | Tu resultado es correcto.')
        print(Fore.RESET + self.__line)
    
    def __print_error_hint(self, enum, equiz="", ans="", msg="", info=""):
        """
        Imprime el mensaje cuando hay un error y la retroalimentación.

        Parameters
        ----------
        enum : str
            Número del ejercicio dentro del quiz.

        equiz : str
            Tipo de evaluación.
            
        msg : str
            Mensaje con el posible error encontrado.
        """
        print(Fore.RESET + self.__line)
        if equiz == "option":
            print(Fore.RED + enum + ' | Tu respuesta:', end = ' ')
            print(Fore.RESET + '{}'.format(ans), end = '')
            print(Fore.RED + ', es INCORRECTA.') 
        elif equiz == "expression":
            print(Fore.RED + enum + ' | Tu respuesta:')
            display(ans)
            print(Fore.RED + 'NO es correcta.')
        else:
            print(Fore.RED + enum + ' | Ocurrió un error en tus cálculos.')
        print(Fore.RESET + self.__line)
        print(Fore.RED + 'Hint:', end = ' ')
    
        # Se obtiene la retroalimentación para la pregunta correspondiente.            
        feedback = self.__read(enum, '.__fee_')
        
        # Si el ejercicio (enum) contiene retroalimentación, se imprime en pantalla.
        # En otro caso no se imprime nada.
        if feedback[enum][0] != None and self.__verb >= 1:            
            print(Fore.RED + feedback[enum][0] + msg)
        else:
            print()            
            print(Fore.RESET + self.__line)
            
        # Se imprime la información del error.
        if self.__verb >= 2:
            print(info)

    def __test_string_array(self, b, a):
        """
        Compara dos arreglos de valores tipo cadena (str).
        
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
        msg : str
            Mensaje con el posible error encontrado: 
             - diferencia entre longitudes de los arreglos.
             - diferencia en algún elemento de los arreglos (la primera que ocurre).
        """
        b = b.flatten()
        msg = ""
        if len(a) == len(b):
            first = np.where((a == b) == False)[0]
            msg = f"\n Lugares donde hay diferencia: {first}"
                    
        else:
            # Cuando la longitud de los arreglos es distinta
            msg = f"\nLongitud correcta={len(a)}\nLongitud de tu respuesta={len(b)}"
                
        return msg
        
    def __test_numeric_array(self, b, a):
        """
        Compara dos arreglos de valores numéricos.
        
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
        msg : str
            Mensaje con el posible error encontrado: 
             - diferencia entre longitudes de los arreglos.
             - diferencia en algún elemento de los arreglos (la primera que ocurre).
        """
        b = b.flatten()
        msg = ""
        if len(a) == len(b):
            if not np.allclose(a, b, equal_nan=True):
                first = np.where((a == b) == False)[0]
                msg = f"\n Lugares donde hay diferencia: {first}"    
        else:
            # Cuando la longitud de los arreglos es distinta
            msg = f"\nLongitud correcta={len(a)}\nLongitud de tu respuesta={len(b)}"
                
        return msg
        
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
        answer = self.__read(enum)
        # Eliminamos espacios que haya de más en la respuesta del alumno.
        ans = ans.replace(" ","") 

        # Se compara la respuesta del alumno (ans) con la correcta (answer[enum][0])
        # La comparación se realiza en minúsculas.
        correct = ans.lower() == answer[enum][0].lower()
        
        if correct:
            self.__print_correct(enum, equiz="option", ans=ans)
        else:
            self.__print_error_hint(enum, equiz="option", ans=ans)

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
        value = self.__read(enum)

        # Se convierte la respuesta correcta (value) en formato SymPy.
        correct = sp.sympify(value[enum][0])

        # Se compara la respuesta correcta (correct) con la respuesta
        # del alumno (ans) usando la función equals().
        if correct.equals(ans):
            self.__print_correct(enum, equiz="expression", ans=ans)
        else:
            self.__print_error_hint(enum, equiz="expression", ans=ans)

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
        value = self.__read(enum)        
        correct = value[enum][0]
        msg = ""

        try:
            if isinstance(ans, np.ndarray):
                if ans.dtype == complex:
                    # Preprocesamiento especial para números complejos.
                    b = np.array([[c.real, c.imag] for c in ans.flatten()]).flatten()
                    msg = self.__test_numeric_array(b, correct)
                    np.testing.assert_allclose(b, correct)                  
                else:                        
                    msg = self.__test_numeric_array(ans, correct)
                    np.testing.assert_allclose(ans, correct)

            elif isinstance(ans, list) or isinstance(ans, tuple):
                b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                msg = self.__test_numeric_array(b, correct)
                np.testing.assert_allclose(b, correct)

            elif isinstance(ans, set):
                b = np.array(list(ans))
                msg = self.__test_numeric_array(b, correct)
                np.testing.assert_allclose(b, correct)

            elif isinstance(ans, complex):
                a = complex(correct[0], correct[1])
                b = np.array([ans.real, ans.imag])
                
                if not np.allclose(correct, b):
                    msg = f"\n Valor correcto  : {a}\n Valor calculado : {ans}\n"
                    raise AssertionError from None

            elif isinstance(ans, int) or isinstance(ans, float) or isinstance(ans, bool):
                if not math.isclose(correct, ans):
                    msg = f"\n Valor correcto  : {correct}\n Valor calculado : {ans}\n"
                    raise AssertionError from None

            else:
                print(enum + ' | Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
                
        except AssertionError as info:
            self.__print_error_hint(enum, msg=msg, info=info)

            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
        else:
            self.__print_correct(enum)

    def eval_datastruct(self, enum, ans, in_order=True):
        """
        Evalúa una respuesta almacenada en una estructura de datos.
        
        Parameters
        ----------
        enum: string
            Número de pregunta.
        
        ans: string
            Respuesta del alumno.

        in_order: bool
            Si la respuesta debe estar en orden (True) o no (False).
        """
        # Se obtiene la respuesta correcta del archivo. Recordemos que
        # Parquet escribe listas y tuplas en forma de np.ndarray, por lo que
        # al recuperarlas del archivo vienen en formato np.ndarray en 1D.
        value = self.__read(enum)        
        correct = value[enum][0]
        msg = ""       

        try:
            if isinstance(ans, set) or isinstance(ans, tuple): ans = list(ans)
                
            if isinstance(ans, list):
                if in_order: 
                    b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                    msg = self.__test_string_array(b, correct)
                    np.testing.assert_equal(b, correct)
                else:
                    b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                    b.sort()
                    correct.sort()
                    msg = self.__test_string_array(b, correct)
                    np.testing.assert_equal(b, correct)                    
                    
            else:
                print('Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
            
        except AssertionError as info:
            self.__print_error_hint(enum, msg=msg, info=info)

            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
        else:
            self.__print_correct(enum)
            
    def eval_dict(self, enum, ans, numeric = True):
        """
        Evalúa una respuesta almacenada en un diccionario.
        
        Parameters
        ----------
        enum: str
            Número de pregunta.
        
        ans: str
            Respuesta del alumno.

        numeric: bool.
            Verifica
        """
        enum_copy = enum
        msg = ""       
        
        try:
            if isinstance(ans, dict):
                # Se obtiene la longitud del diccionario y se compara con la respuesta del alumno.
                dict_len = len(ans) # Respuesta del alumno
                enum = enum_copy + "_len" # etiqueta de la columna con la respuesta en el archivo
                value = self.__read(enum)   
                correct = value[enum][0]
                if not math.isclose(correct, dict_len):
                    msg = f"\n Valor correcto  : {correct}\n Valor calculado : {dict_len}\n"
                    raise AssertionError from None
                
                # Se obtienen los keys del diccionario y se comparan con la respuesta del alumno.
                keys = np.array(list(ans.keys())) # Respuesta del alumno
                enum = enum_copy + "_key" # etiqueta de la columna con la respuesta en el archivo
                value = self.__read(enum)        
                correct = value[enum][0]
                where = np.where((correct == keys) == False)
                if len(where[0]) > 0:
                    msg = f"\n Keys correctas  : {correct}\n Keys calculadas : {keys}\n"
                    np.testing.assert_equal(keys, correct)

                # Se obtienen los valores del diccionario, uno a uno, y se comparan con la respuesta del alumno.
                for i, b in enumerate(ans.values()):
                    enum = enum_copy + "_val_" + str(i)
                    value = self.__read(enum)        
                    correct = value[enum][0]

                    if numeric:
                        if isinstance(b, int) or isinstance(b, float) or isinstance(b, bool):
                            if not math.isclose(correct, b):
                                msg = f"\n Valor correcto  : {correct}\n Valor calculado : {b}\n"
                                raise AssertionError from None
                                
                        elif isinstance(b, list) or isinstance(b, tuple) or isinstance(b, set):
                            if isinstance(b, set): b = list(b)
                            b = np.array(b).flatten() # Se requiere flatten() para listas de listas
                            msg = self.__test_numeric_array(b, correct)
                            np.testing.assert_allclose(b, correct)    
                    else:
                        if isinstance(b, str):
                            if correct != b:
                                msg = f"\n Valor correcto  : {correct}\n Valor calculado : {b}\n"
                                raise AssertionError from None
                                
                        elif isinstance(b, list) or isinstance(b, tuple) or isinstance(b, set):
                            if isinstance(b, set): b = list(b)
                            b = np.array(b).flatten() # Se requiere flatten() para listas de listas
                            msg = self.__test_string_array(b, correct)
                            np.testing.assert_equal(b, correct)   

            else:
                print(enum + ' | Respuesta inválida: {} es de tipo {}'.format(ans, type(ans)))

                # Se lanza la excepción para que sea detectada por NBGrader
                raise AssertionError from None
                
        except AssertionError as info:
            self.__print_error_hint(enum, msg=msg,  info=info)
            
            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None

        else:
            self.__print_correct(enum_copy) 
            
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':

    mi_dict_1 = {"k1": "luis", "k2": "miguel", "k3": "x"}
    mi_dict_2 = {"k1": 1, "k2": 2, "k3": 3}
    mi_dict_3 = {1: 3.446, 2: 5.6423, 3: 2.234324}
    diccionario_num_list = {1:[3.446,34.566], 
                            2:[5.6423, 6.7564], 
                            3:[2.234324, 5.65645]}

    for i, b in enumerate(diccionario_num_list.values()):
        print(i, b)
    #----- CREACIÓN DEL DATAFRAME DE RESPUESTAS
    
    print("Iniciamos con FileAnswer")
    file_answer = FileAnswer()
    file_answer.write('1', mi_dict_1, 'mi_dict_1')
    file_answer.write('2', mi_dict_2, 'mi_dict_2')
    file_answer.write('3', mi_dict_3, 'mi_dict_3')
    file_answer.write('4', diccionario_num_list, 'Checa los diccionarios numéricos con valores tipo lista')
    file_answer.to_file('test01')
    
    ans = pd.read_parquet('../.ans/eval/.__ans_test01')
    fee = pd.read_parquet('../.ans/eval/.__fee_test01')
    print("\n----- RESPUESTAS Y DE RETROALIMENTACIÓN")
    print(ans)
    fstr = "Pregunta {}:\n a --> {}\n f --> {}\n"
    [print(fstr.format(i, ans[i][0], fee[i][0])) for i in ans.columns]

    quiz = Quiz("test01", "resources", "local")
    mi_dict_1 = {"k1": "luis", "k2": "miguel", "k3": "x"}
    quiz.eval_dict("1", mi_dict_1, numeric = False)
    quiz.eval_dict("2", mi_dict_2)
    quiz.eval_dict("3", mi_dict_3)

    diccionario_num_list = {1:[3.446,34.566], 
                            2:[5.6423, 6.7564], 
                            3:[2.234324, 5.65645]}
    quiz.eval_dict('4', diccionario_num_list)
    



    

