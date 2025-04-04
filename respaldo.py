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