"""
@author: Luis M. de la Cruz [Updated on Tue Nov 17 17:54:11 2026].
"""

import os
import shutil
import gettext
from pathlib import Path
import importlib.resources
from colorama import Fore, Back, Style, init
init(autoreset=True)

#
## ---> Common functions
#

def print_macti_info(msg):
    """
    Imprime información de las acciones del script.
    """
    print(Fore.GREEN + "[MACTI | INFO] " + Style.RESET_ALL + msg)

def init_translator(appname, lang):

    # Directorio local
    locale_dir = importlib.resources.files("macti").joinpath("locales")

#    with importlib.resources.as_file(locale_dir) as path:
#        print(f"RUTA {path}")
        
    # Set up Gettext
    trans_i18n = gettext.translation(appname, locale_dir, fallback=True, languages=[lang])
    
    # Create the "magic" function
    trans_i18n.install()

#
## ---> Helper functions ---
#

def __make_dirs(paths):
    """
    Crea los subdirectorios iniciales del curso.
    """
    for p in paths:
        if not os.path.exists(p):
            print_macti_info(_("Creando el directorio : {}  ").format(p))
            os.makedirs(p , exist_ok=True)
        else:
            print_macti_info(_("El directorio : {} ya existe  ").format(p))
    
def __copy_files(filenames, abspath, path):
    """
    Obtiene los archivos del curso de los recursos de macti.
    """
    
    for f in filenames:
        resource = importlib.resources.files("macti").joinpath(f"resources/{f}")
        print_macti_info(_("Copiando {} al directorio {}  ").format(resource.name, path))
        destination_file = Path(path) / f
        with resource.open("rb") as src, destination_file.open("wb") as dst:
            shutil.copyfileobj(src, dst)

def __initial_screen():
    #
    # --- Pantalla inicial
    #
    #os.system("clear")
    print()
    print_macti_info(Fore.WHITE + Back.GREEN + _(" Creación de directorio del curso ") )
    print()
    c_name = input(_(" Nombre del curso : "))
    print()

    return c_name

def __local_dirs_creation(c_name):
    #
    # --- Creación de directorios ---
    #
    abspath = os.getcwd()
    paths = [c_name,
             os.path.join(c_name, "01_Topic_A"), 
             os.path.join(c_name, ".ans"), 
             os.path.join(c_name, "resources"), 
            ]
    __make_dirs(paths)

    return abspath, paths

def __git_repo_init(c_name):
    #
    # --- Iniciar el repositorio local con git ---
    #
    print_macti_info(_("Cambiando al directorio : {}  ".format("/" + c_name + "/")))
    os.chdir(c_name)
    
    print_macti_info(_("Inicializando el repositorio con git "))
    os.system("git init")
    
    print_macti_info(_("Cambiando el nombre de la rama principal a 'main' "))
    os.system("git branch -M main")
  
def __copy_course_files(abspath, paths):
    #
    # --- Copiar archivos ---
    #
    filenames = ["plantilla.ipynb", 
                 "q1_plantilla.ipynb"]
    __copy_files(filenames, abspath, paths[1])
    
    filenames = ["nbgex", 
                 "assignments_creation.csv", 
                 "assignments_update.csv", 
                 "macti_nbg_qs.py"]
    __copy_files(filenames, abspath, paths[0])
    os.rename(os.path.join(abspath, paths[0],"nbgex"), 
              os.path.join(abspath, paths[0],".nbgex"))

    filenames = ["calificador.ipynb",
                 "preproc_gb.ipynb",
                 "test_evaluation.ipynb",
                 "test_visual.ipynb",
                 "interactivo_test.ipynb"]
    __copy_files(filenames, abspath, paths[3])
    
#
## ---> Config the course---
#

def init_course():
    lang = input("English? (Yes [y] / No [n])? ")
    lang = "en" if lang.upper() == "Y" else "es"

    init_translator("macti", lang)
    
    c_name = __initial_screen()
    abspath, paths = __local_dirs_creation(c_name)
    __copy_course_files(abspath, paths)
    __git_repo_init(c_name)
    
    print_macti_info(_(Fore.WHITE + Back.GREEN \
                     + _(" Configuración exitosa de ") \
                     + Style.BRIGHT + f" {c_name} ") )

            
#----------------------- TEST OF THE MODULE ----------------------------------   
if __name__ == '__main__':
    init_course()
