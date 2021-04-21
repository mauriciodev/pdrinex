import pandas as pd
import re,time
from datetime import datetime



class pdrinex:
    """Splits a string in fixed parts."""
    def __init__(self):
        pass
    def chunks(self,l, n): 
        return [l[i:i+n].strip() for i in range(0, len(l), n)]

    """Creates a pandas dataframe with columns: observable,observableid,satellite and epoch."""
    def readRinexObs(self,fileName):
        obs={} #epoch, sat, obsvector
        currentEpoch=None
        
        obsIds={} #this will represent the observables on each system. Ex.: 'C': ['C2I', 'C6I', 'C7I', 'L2I', 'L6I', 'L7I', 'S2I', 'S6I', 'S7I']
        data = {'observable':  [],
            'observableid': [],
            'satellite': [],
            'epoch':[]
            }
        with open(fileName) as f:
            header=[]
            headerEnded=False
            for line in f:
                if not headerEnded:
                    if not "END OF HEADER" in line:
                        header.append(line)
                        if "SYS / # / OBS TYPES" in line:
                            line, sep, tail = line.partition('SYS')
                            if not line[0]==' ': #if we have a system on first digit, it's the first line of measures.
                                system=line[0]
                                obsIds[system]=re.split(' +', line)[2:-1]
                            else:
                                obsIds[system]+=re.split(' +', line)[1:-1]
                    else:
                        headerEnded=True
                else:
                    if line[0]==">": #new epoch
                        values = re.split(' +', line)                
                        values[6]="{:.6f}". format(float(values[6])) #reducing second decimal places
                        epoch=' '.join(values[1:7])
                        currentEpoch=datetime.strptime(epoch, "%Y %m %d %H %M %S.%f")
                    else:
                        values=self.chunks(line[3:].strip(),16)
                        sat=line[:3]

                        for i,observable in enumerate(values):
                            if not observable=='' and i<len(obsIds[sat[0]]):
                                observable=observable.split(" ")[0] #ignoring the single digit after the observable
                                data['satellite'].append(sat) #first val ex.:'C19'
                                data['observable'].append(float(observable))
                                data['observableid'].append(obsIds[sat[0]][i])
                                data['epoch'].append(currentEpoch)
        obs=pd.DataFrame(data)
        return obs,header

    """Creates a pandas dataframe with columns: satellite, epoch and navigation values."""
    def readRinexNav(self,fileName):
        eph={} #epoch, sat, obsvector
        currentEpoch=None
        
        obsIds={} #this will represent the observables on each system. Ex.: 'C': ['C2I', 'C6I', 'C7I', 'L2I', 'L6I', 'L7I', 'S2I', 'S6I', 'S7I']
        data = {'ephemeris':  [],
            'satellite': [],
            'epoch':[]
            }
        with open(fileName) as f:
            header=[]
            headerEnded=False
            for line in f:
                if not headerEnded:
                    if not "END OF HEADER" in line:
                        header.append(line)
                    else:
                        headerEnded=True
                else:
                    if line[0]!=" ": #new ephemeris
                        values=self.chunks(line[23:].strip(),19)
                        sat=line[:4].strip()
                        
                        epoch=line[4:23]
                        currentEpoch=datetime.strptime(epoch, "%Y %m %d %H %M %S")
                        data['satellite'].append(sat)
                        data['epoch'].append(currentEpoch)
                        data['ephemeris'].append(values)
                        
                    else:
                        values=self.chunks(line[4:].strip(),19)
                        data['ephemeris'][-1]+=values
        obs=pd.DataFrame(data)
        return obs,header



if __name__=="__main__":
    obsRinex="RJNI00BRA_R_20210680000_01D_15S_MO.rnx"


    start=time.perf_counter()
    reader=pdrinex()
    obs,header=reader.readRinexObs(obsRinex) 
    end=time.perf_counter()    
    print(f"RINEX read in {end - start:0.4f} seconds")

    start=time.perf_counter()
    print(obs[ obs.observableid=='C2I' ] )
    end=time.perf_counter()    
    print(f"Observables filtered in {end - start:0.4f} seconds")

    start=time.perf_counter()
    epoch=datetime.strptime("2021 03 09 23 59 30.000000", "%Y %m %d %H %M %S.%f")
    gps_p1=obs[(obs['epoch']==epoch) & (obs.observableid=='C1P')]
    end=time.perf_counter()    
    print(gps_p1)
    print(f"epochs iterated {end - start:0.4f} seconds")

    start=time.perf_counter()
    navRinex="BRDC00WRD_S_20210680000_01D_MN.rnx"
    nav,header=reader.readRinexNav(navRinex) 
    end=time.perf_counter()  
    print(f"Nav RINEX read in {end - start:0.4f} seconds")
    print(nav)
    print("Done")


