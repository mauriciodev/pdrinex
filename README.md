# pdrinex
GNSS files reader that builds pandas dataframes.

# Example usage:

from pdrinex import pdrinex
reader=pdrinex()

obsRinex="test_data/RJNI00BRA_R_20210680000_01D_15S_MO.rnx"

obs,header=reader.readRinexObs(obsRinex) 
    
navRinex="test_data/BRDC00WRD_S_20210680000_01D_MN.rnx"

nav,header=reader.readRinexNav(navRinex) 
