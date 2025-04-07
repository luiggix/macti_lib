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



----------------

    def __test_datastruct(self, a, b):
        """
        Compara dos estructuras de datos.
        
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
        if len(a) == len(b):
            if not np.allclose(a, b, equal_nan=True):
                first = int(np.where((a == b) == False)[0][0]) # primer elemento donde hay diferencia
    
                if self.__verb >= 1:
                    # Mensaje de ayuda
                    msg = f"\n 1er elemento con error: {first}.\n valor correcto {a[first]}, \n valor calculado {b[first]}\n"
                else:
                    msg = ""
                    
                # Se lanza la excepción
                return np.testing.assert_allclose(a, b, err_msg=msg)
        else:
            # Cuando la longitud de los arreglos es distinta se lanza una excepción
            # y se guardan los datos para dar retroalimentación al alumno.
            self.__array_len_correct = len(a)
            self.__array_len_answer = len(b)
            self.__array_len_diff = True
            
            # Se lanza la excepción para que sea detectada por NBGrader
            raise AssertionError from None
            
