
class TDis():
    def __init__(self, perioddata):
        self.__perioddata = perioddata
        self.__nper = len(perioddata)
        self.__total_time = 0
        self.__dt = []
        for p in self.__perioddata:
            self.__total_time += p[0] # Suma los perlen

            PERLEN, NSTP, TSMULT = p[0], p[1], p[2] 
            if TSMULT == 1:
                Dt1 = PERLEN / NSTP
            else:
                Dt1 = PERLEN * (TSMULT - 1) / (TSMULT**NSTP - 1)
            self.__dt.append(Dt1)

    def print(self):
        print('      NPER = {:<8d}'.format(self.__nper))
        print('TOTAL TIME = {:<5.2f}\n'.format(self.__total_time))
        print('{:>3s} {:>10s} {:>8s} {:>10s} {:>10s}'.format('PER', 'PERLEN', 'NSTP', 'TSMULT', 'Dt1'))
        for i, p in enumerate(self.__perioddata):
            print('{:3d} {:>10.2f} {:>10.2f} {:>10.2f} {:>10.2e}'.format(i+1, p[0], p[1], p[2], self.__dt[i]))

    @property
    def nper(self):
        return self.__nper

    @property
    def total_time(self):
        return self.__total_time

#    @property
    def perioddata(self, i = -1):
        if i < 0:
            return self.__perioddata
        else:
            return self.__perioddata[i]

#    @property
    def dt(self, i = -1):
        if i < 0:
            return self.__dt
        else:
            return self.__dt[i]

if __name__ == '__main__':

    perioddata = [(120.0, 240, 1.0),
                 (120.0, 60, 1.0),
                 (65.5, 30, 1.2)] # perlen, nstp, tsmult
    tdis = TDis(perioddata)
    print(tdis.nper)
    print(tdis.total_time)
    print(tdis.perioddata(0))
    print(tdis.dt(0))
    print(tdis.perioddata())
    print(tdis.dt())

    from osys import nice_print
    nice_print(tdis, 'Testing ...')

