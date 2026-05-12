"""
@author: Luis M. de la Cruz [Updated on Mon Aug 25 09:30:10 CST 2025].
"""

# Herramientas para colorear texto y comparación de los resultados
from colorama import Fore
import math
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
            _, cn = os.path.split(cp)
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
        correct = sy.sympify(value[enum][0])

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
                            if isinstance(ans, set): ans = list(ans)
                            b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
                            msg = self.__test_numeric_array(b, correct)
                            np.testing.assert_allclose(b, correct)    
                    else:
                        if isinstance(b, str):
                            if correct != b:
                                msg = f"\n Valor correcto  : {correct}\n Valor calculado : {b}\n"
                                raise AssertionError from None
                                
                        elif isinstance(b, list) or isinstance(b, tuple) or isinstance(b, set):
                            if isinstance(ans, set): ans = list(ans)
                            b = np.array(ans).flatten() # Se requiere flatten() para listas de listas
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
            self.__print_correct(enum) 
            
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

    # Datos básicos
    flotante = 0.1
    entero = 1
    logico = True
    complejo = 1 + 5j

    # Estructuras de datos
    lista_num = [0, 1, 3.4]
    lista = ['luis', 'miguel', 'delacruz']

    tupla_num = (1.2, 3.1416, np.pi)
    tupla = ('a', 'b', 'c')

    conjunto_num = {1, 3, 2, 6, 5, 4}
    conjunto = {'a', 'b', 'c'}
    
    diccionario_num = {1:3.446, 2:5.6423, 3:2.234324}
    diccionario_k_str = {'k1':1, 'k2':2, 'k3':3}
    diccionario_kv_str= {'k1':'luis', 'k2':'miguel', 'k3':'x'}

    # Arreglos de numpy
    w = np.sin(np.linspace(0,1,10))
    arreglo_complejo = np.array([1j,2j,3j,4j,5j])

    # Estructuras de datos más complejas
    lista_lista = [[1,2],[3,4]]

    # Lista y tuplas no ordenadas
    lista_no = ['a', 'b', 'x', '4', 'c']
    tupla_no = ('a', 'b', 'x', '4', 'c')

    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564], 3:[2.234324, 5.65645]}

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
    file_answer.write('6', logico, 'Checa  logico')
    file_answer.write('7', complejo, 'Checa el valor de complejo')

    file_answer.write('8', lista_num, 'Checa la lista numérica')
    file_answer.write('9', lista, "checa la estructura de tipo lista")

    file_answer.write('10', tupla_num, 'Checa la tupla numérica')
    file_answer.write('11', tupla, "checa la estructura de tipo tupla")

    file_answer.write('12', conjunto_num, 'Checa los conjuntos numéricos')
    file_answer.write('13', conjunto, "checa la estructura de tipo conjunto")

    file_answer.write('14', diccionario_num, 'Checa los diccionarios numéricos')
    file_answer.write('15', diccionario_k_str, 'Checa los diccionarios con keys str')
    file_answer.write('16', diccionario_kv_str, "checa la estructura de tipo diccionario")
    
    mensaje ="""Puedes poner mucho texto y ver que sucede en la impresión del hint,
    quizá es necesario usar triples comillas"""
    file_answer.write('17', w, mensaje)
    file_answer.write('18', arreglo_complejo, 'Checa el arreglo complejo')

    file_answer.write('19', lista_lista, "Checa la lista de listas")
    file_answer.write('20', lista_no, "Checa la lista NO ordenada")
    file_answer.write('21', tupla_no, "Checa la tupla NO ordenada")

#    file_answer.write('21', diccionario_num_list, 'Checa los diccionarios numéricos con valores tipo lista')

    #----- ESCRITURA DE LAS RESPUESTAS Y LA RETROALIMENTACIÓN ARCHIVOS.
    
    file_answer.to_file('test01')

    #----- MOSTRAMOS LOS ARCHIVO DE RESPUESTAS Y DE RETROALIMENTACIÓN
    
    ans = pd.read_parquet('../.ans/eval/.__ans_test01')
    fee = pd.read_parquet('../.ans/eval/.__fee_test01')
    print("\n----- RESPUESTAS Y DE RETROALIMENTACIÓN")
    fstr = "Pregunta {}:\n a --> {}\n f --> {}\n"
    [print(fstr.format(i, ans[i][0], fee[i][0])) for i in ans.columns]

#    print(len(file_answer.answers), "\n", file_answer.answers)
#    print()
#    print(len(file_answer.feedback), "\n", file_answer.feedback)

    #----- CREACIÓN DE LAS EVALUACIONES
    
    print("Quiz number:", file_answer.quiz_num)

    quiz = Quiz(file_answer.quiz_num, 'macti', 'local')
#    quiz2 = Quiz(file_answer.quiz_num, 'macti')
    
    print('\nVerbosidad de la ayuda : {} \n'.format(quiz.verb))
    
    print('Opción')
    quiz.eval_option('1', opcion)
    
    print('Expresión')
    quiz.eval_expression('2', derivada)

    print('Expresión más compleja')
    quiz.eval_expression('3', forma_cuadratica)
    
    print('Flotante')
    quiz.eval_numeric('4', flotante)
    
    print('Entero')
    quiz.eval_numeric('5', entero)
    
    print('Logico')
    quiz.eval_numeric('6', logico)

    print('Complejo')
    quiz.eval_numeric('7', complejo)

    print('Lista numérica')
#    lista_num = [0, 1]
#    lista_num[-2] =0.001
    quiz.eval_numeric('8', lista_num)

    print('Lista')
#    lista = ['miguel', 'delacruz']
#    lista = ['luis', 'migul', 'delacruz']
    quiz.eval_datastruct('9', lista)

    print('Tupla numérica')
#    tupla_num = (0, 1)
#    tupla_num = (1.2, 3.1416, 2*np.pi)
    quiz.eval_numeric('10', tupla_num)    

    print('Tupla')
#    tupla = ('a', 'b')
#    tupla = ('a', 'd', 'c')
    quiz.eval_datastruct('11', tupla)  
    
    print('Conjunto numérico')
#    conjunto_num = {1,2,3,4,5,1}
#    conjunto_num = {1,2,3.5,4,5,6}
    quiz.eval_numeric('12', conjunto_num)

    print('Conjunto')
#    conjunto = {'a', 'b'}
#    conjunto = {'a', 'b', 'x'}
    quiz.eval_datastruct('13', conjunto)
    
    print('Diccionario numérico')
#    diccionario_num = {1:3.446, 2:5.6423}
#    diccionario_num = {1:3.44, 4:5.6423, 3:2.234324}
#    diccionario_num = {1:3.446, 2:5.642, 3:2.234324}
    quiz.eval_dict('14', diccionario_num)

    print('Diccionario con keys str y values numéricos')
#    diccionario_k_str = {'k1':1, 'k2':2}
#    diccionario_k_str = {'k1':1, 'k4':2, 'k3':3}
#    diccionario_k_str = {'k1':1, 'k2':2.4, 'k3':3}
    quiz.eval_dict('15', diccionario_k_str)

    print('Diccionario con keys y values str')
#    diccionario_kv_str= {'k1':'luis', 'k2':'miguel'}
#    diccionario_kv_str= {'k1':'luis', 'k4':'miguel', 'k3':'x'}
#    diccionario_kv_str= {'k1':'luis', 'k2':'mil', 'k3':'x'}
    quiz.eval_dict('16', diccionario_kv_str, numeric = False)

    print('numpy array')
#    w = np.sin(np.linspace(0,1,5))
#    w[2:4] = 4.5
    quiz.eval_numeric('17', w)

    print('numpy array complex')
#    arreglo_complejo = np.array([2j,3j,4j,5j])
#    arreglo_complejo = np.array([0j,2j,3j,4j,5j])
    quiz.eval_numeric('18', arreglo_complejo)

    print('Lista de listas')
#    lista_lista = [[1,2],[3,4],[5,6]]
#    lista_lista = [[1,2],[3.14,4]]
    quiz.eval_numeric('19', lista_lista)

    print('Lista NO ordenada')
    # Lista original: lista_no = ['a', 'b', 'x', '4', 'c']
    # La respuesta puede estar en otro orden y ser correcta
#    lista_no = ['x', '4', 'a', 'c', 'b']
    # Los siguientes casos fallan
#    lista_no = ['x', '4', 'c', 'b']
#    lista_no = ['x', '4', 'c', 'b', 'y']
    quiz.eval_datastruct('20', lista_no, in_order=False)

    print('Tupla NO ordenada')
    # Tupla original: tupla_no = ('a', 'b', 'x', '4', 'c')
    # La respuesta puede estar en otro orden y ser correcta
#    tupla_no = ('x', '4', 'a', 'c', 'b')
    # Los siguientes casos fallan
#    tupla_no = ('x', '4', 'c', 'b')
#    tupla_no = ('x', '4', 'c', 'b', 'y')
    quiz.eval_datastruct('21', tupla_no, in_order=False)
    
#    print('Diccionario numérico con valores tipo lista')
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564]}
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.6423, 6.7564], 5:[2.234324, 5.65645]}
#    diccionario_num_list = {1:[3.446,34.566], 2:[5.643, 6.7564], 3:[2.234324, 5.65645]}
#    quiz.eval_dict('22', diccionario_num_list)
    



    

