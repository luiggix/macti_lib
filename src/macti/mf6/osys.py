import os
from colorama import Fore, Style, Back
import flopy
#from xmf6.mesh import MeshDis
#from xmf6.tdis import TDis

def nice_print(data, message = ''):
    print(Fore.BLUE)
    print(message)
    print('{:^30}'.format(30*'-') + Style.RESET_ALL)

    if isinstance(data, dict):
        for k,v in data.items():
            print('{:>20} = {:<10}'.format(k, v))
    else: #if not isinstance(data, dict):# or isinstance(data, TDis):
        data.print()

class OSPar():
    """
    Clase para definición del espacio de trabajo, nombre del ejecutable de MF6,
    nombres de las simulaciones y nombres de archivos de salida.

    Parameters
    ----------
    ws: str
    Ruta del espacio de trabajo
    
    exe: str
    Ejecutable de MODFLOW 6, incluyendo la ruta del archivo.

    fn: str
    Nombre para la simulación de GWF
    
    hf: str
    Archivo para almacenar la carga hidraúlica
    
    hbf: str
    Archivo para almacenar el balance de la carga hidraúlica
    
    tn: str
    Nombre para la simulación de GWT
    
    cf: str
    Archivo para almacenar la carga concentración

    cbf: str
    Archivo para almacenar el balance de la concentración
    

    """
    def __init__(self, ws, exe, fn, hf, hbf, tn = "", cf = "", cbf = ""):
        self.__workspace = ws          # Espacio de trabajo
        self.__mf6exe = exe            # Ejecutable de MODFLOW 6
        self.__flow_name = fn          # Nombre para la simulación de GWF
        self.__head_file = hf          # Archivo para la carga hidraúlica
        self.__hbudget_file = hbf      # Archivo para el balance de h
        self.__transport_name = tn     # Nombre para la simulación de GWT
        self.__concentration_file = cf # Archivo para la concentración
        self.__cbudget_file = cbf      # Archivo para el balance de c

    def print(self):
        print('         Workspace = {:12s}'.format(self.__workspace))
        print('     MODFLOW 6 exe = {:12s}'.format(self.__mf6exe))
        print('         Flow name = {:12s}'.format(self.__flow_name))
        print('         Head file = {:12s}'.format(self.__head_file))
        print('     h Budget file = {:12s}'.format(self.__hbudget_file))
        if self.__transport_name != "":
            print('    Transport name = {:12s}'.format(self.__transport_name))
        if self.__concentration_file != "":
            print('Concentration file = {:12s}'.format(self.__concentration_file))
        if self.__cbudget_file != "":
            print('     c Budget file = {:12s}'.format(self.__cbudget_file))

    @property
    def workspace(self):
        return self.__workspace

    @workspace.setter
    def workspace(self, ws):
        self.__workspace = ws

    @property
    def mf6exe(self):
        return self.__mf6exe

    @mf6exe.setter
    def mf6exe(self, exe):
        self.__mf6exe = exe
        
    @property
    def flow_name(self):
        return self.__flow_name

    @flow_name.setter
    def flow_name(self, fn):
        self.__flow_name = fn
        
    @property
    def head_file(self):
        return self.__head_file

    @head_file.setter
    def head_file(self, hf):
        self.__head_file = hf
        
    @property
    def hbudget_file(self):
        return self.__hbudget_file

    @hbudget_file.setter
    def hbudget_file(self, hbf):
        self.__hbudget_file = hbf
        
    @property
    def transport_name(self):
        return self.__transport_name

    @transport_name.setter
    def transport_name(self, tn):
        self.__transport_name = tn
        
    @property
    def concentration_file(self):
        return self.__concentration_file
        
    @concentration_file.setter
    def concentration_file(self, cf):
        self.__concentration_file = cf
        
    @property
    def cbudget_file(self):
        return self.__cbudget_file

    @cbudget_file.setter
    def cbudget_file(self, hbf):
        self.__cbudget_file = cbf
                 
class OFiles():
    def __init__(self, os_par, oc_par):
        self.os_par = os_par
        self.oc_par = oc_par

    def get_head(self):
        return flopy.utils.HeadFile(
            os.path.join(self.os_par["ws"], 
                         self.oc_par["head_file"])).get_data()

    def get_bud(self):    
        return flopy.utils.CellBudgetFile(
            os.path.join(self.os_par["ws"], 
                         self.oc_par["fbudget_file"]),
            precision='double')

    def get_spdis(self):
        bud = self.get_bud()
        return bud.get_data(text='DATA-SPDIS')[0]

    def get_q(self, gwf):
        spdis = self.get_spdis()
        return flopy.utils.postprocessing.get_specific_discharge(spdis, gwf)

    def get_concentration(self, sim, t):
        ucnobj_mf6 = sim.transport.output.concentration()
        simconc = ucnobj_mf6.get_data(totim=t).flatten()
        return simconc

if __name__ == '__main__':

    ospar = OSPar(ws = "test", exe = "test", 
                  fn = "test", hf = "test", hbf = "test")

    from osys import nice_print
    nice_print(ospar, 'Testing ...')

