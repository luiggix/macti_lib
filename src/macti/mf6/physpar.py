
class PhysPar():
    def __init__(self, time = "seconds", length = "centimeters"):
        self.__ppar = {}
        self.__ppar['time'] = time
        self.__ppar['length'] = length
        
    def print(self):
        for k, v in self.__ppar.items():
            if isinstance(v, str):
                print(f"{k:>30s} = {v:<20s}")
            if isinstance(v, int):
                print(f"{k:>30s} = {v:<20d}")                
            if isinstance(v, float):
                print(f"{k:>30s} = {v:<10.5f}")
#        print('  Time units = {:20s}'.format(self.__time))
#        print('Length units = {:20s}\n'.format(self.__length))
        

    @property
    def time(self):
        return self.__ppar['time']

    @property
    def length(self):
        return self.__ppar['length']

    @property
    def specific_discharge(self):
        return self.__ppar['specific discharge']

    @specific_discharge.setter
    def specific_discharge(self, value):
        self.__ppar['specific discharge'] = value

    @property
    def hydraulic_conductivity(self):
        return self.__ppar['hydraulic conductivity']

    @specific_discharge.setter
    def hydraulic_conductivity(self, value):
        self.__ppar['hydraulic conductivity'] = value

    @property
    def source_concentration(self):
        return self.__ppar['source concentration']

    @specific_discharge.setter
    def source_concentration(self, value):
        self.__ppar['source concentration'] = value

if __name__ == '__main__':

    phpar = PhysPar()
    print(phpar.time)
    print(phpar.length)

    phpar.specific_discharge = 0.1
    
    from osys import nice_print
    nice_print(phpar, 'Testing ...')

