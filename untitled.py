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