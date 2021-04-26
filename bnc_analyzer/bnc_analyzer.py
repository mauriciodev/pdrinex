import pandas as pd
import re,time,sys, os
from datetime import datetime
import logging
logging.basicConfig(filename='bnc_analyzer.log',  level=logging.DEBUG)


class BNCAnalyzer:
    """Splits a string in fixed parts."""
    def __init__(self):
        pass
    def chunks(self,l, n): 
        return [l[i:i+n].strip() for i in range(0, len(l), n)]
    
    def str2date(self,line):
        return datetime.strptime(line, "%Y-%m-%d_%H:%M:%S.%f") 
    def fillLists(self,data):
        for key in data.keys():#empty line for the incomplete columns
            if len(data['epoch'])>len(data[key]):
                data[key].append('')
            if len(data['epoch'])<len(data[key]):
                logging.info("Found less epochs than information. This is probably a major data issue in the input file.") 
                data[key]=data[key][:len(data['epoch'])]
        return data
    def fillColumn(self,data,n,column):
        pass



    """Creates a pandas dataframe with columns: observable,observableid,satellite and epoch."""
    def readPPP(self,fileName,outFileName):
        currentEpoch=None
        sats={} #this will represent the observables on each system. Ex.: 'C': ['C2I', 'C6I', 'C7I', 'L2I', 'L6I', 'L7I', 'S2I', 'S6I', 'S7I']
        data = {'epoch':[],
            'X':  [],
            'devX':  [],
            'Y': [],
            'devY': [],
            'Z': [],
            'devZ': [],
            'TRP':[],
            'devTRP':[],
            'clk': []
            }
        
        with open(fileName) as f:
            for line in f:
                if line.startswith("PPP of Epoch"): #new epoch
                    parts=line.split(' ')[-1].strip()
                    currentEpoch=self.str2date(parts)
                    data=self.fillLists(data)
                    data['epoch'].append(currentEpoch)

                elif "CLK" in line:
                    clk=line.split("CLK")[-1].strip()
                    data['clk'].append(clk)
                elif "X =" in line:
                    #2021-04-15_22:39:34.000 POAL00BRA0 X = 3467520.4867 +- 11.4204 Y = -4300378.8761 +- 11.6294 Z = -3177520.1725 +- 17.3975 dN = -1.8964 +- 13.7633 dE = 0.6864 +- 8.5675 dU = 2.0424 +- 17.4788
                    values=re.search('X = (.+) \+- (.+) Y = (.+) \+- (.+) Z = (.+) \+- (.+) dN',line)
                    data['X'].append(float(values[1]))
                    data['devX'].append(float(values[2]))
                    data['Y'].append(float(values[3]))
                    data['devY'].append(float(values[4]))
                    data['Z'].append(float(values[5]))
                    data['devZ'].append(float(values[6]))
                elif "AMB" in line and (not "RESET" in line):
                    #2021-04-15_22:39:34.000 AMB lIF G13    52.0000   +17.6756 +-  81.6740 el =  27.42 epo =    1
                    values=re.split(' +', line)
                    column=values[1]+"_"+values[2]+"_"+values[3]
                    if not column in data.keys():
                        data[column]=['']*(len(data['epoch'])-1)
                    data[column].append(float(values[4]))
                elif "TRP" in line:
                    values=re.split(' +', line)
                    data['TRP'].append(float(values[2]))
                    data['devTRP'].append(float(values[5].strip()))


                    
                
        data=self.fillLists(data)
        df=pd.DataFrame(data)
        df.to_excel(outFileName)
        return df
        


        

if __name__=="__main__":
    """if len(sys.argv)==1:
        pppFile="POAL21534.ppp"
    else:
        pppFile=sys.argv[1]"""
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name.endswith(".ppp"):
                pppFile=os.path.join(root, name)
                logging.info("Processing "+pppFile)
                print("Processing "+pppFile)
                outFilePath=pppFile.replace(".ppp",".xlsx")
                start=time.perf_counter()
                try:
                    reader=BNCAnalyzer()
                    reader.readPPP(pppFile,outFilePath) 
                    end=time.perf_counter()    
                    logging.info(f"PPP converted in {end - start:0.4f} seconds")
                except Exception as e:
                    logging.info("Problems processing ", pppFile)
                    logging.info(e)
                

    start=time.perf_counter()
    input("Finished. Press ENTER to exit.")
