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