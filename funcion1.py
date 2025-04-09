#
def print_error_and_hint(self, enum, msg, info=""):
    print(Fore.RESET + self.__line)
    print(Fore.RED + enum + ' - '+ info + ' | Ocurrió un error en tus cálculos.')
    print(Fore.RESET + self.__line)
    print(Fore.RED + 'Hint:', end = ' ')
    
    # Se obtiene la retroalimentación para la pregunta correspondiente.            
    feedback = self.read(enum, '.__fee_')
    
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