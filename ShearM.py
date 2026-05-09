#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 11:41:15 2024

@author: khatereh
"""
import log # From Pizza.py
import os
import numpy as np

if __name__ == "__main__":
    directory = "/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/4/Seq/Recharged/ShearM/80"
    filename = "CE4Sxy_80.log.lammps"

# Set directory and filename information
os.chdir(directory)

with open(filename,'r') as logfile:
    log_contents = logfile.read().split('\n')
   
for line in log_contents:
    if line.find('WARNING: Bond/angle/dihedral extent > half of periodic box length (../domain.cpp:903)') > -1:
        log_contents.remove(line) # Remove the line if it matches
temp_filename = filename.split('.')[0]+"_temp.log.lammps"
with open(temp_filename,'w') as newlogfile:
    for line in log_contents:
        newlogfile.write(line+"\n")
# Extract all stress-strain data, time, direction
thermo = log.log(temp_filename)
step,etruexy, etruexz, etrueyz, sxx_ave, syy_ave, szz_ave,sxy_ave, sxz_ave, syz_ave, direction = thermo.get("Step","v_etruexy","v_etruexz","v_etrueyz","f_sxx_ave","f_syy_ave","f_szz_ave","f_sxy_ave","f_sxz_ave","f_syz_ave","v_dir")

# Put extracted data into numpy array
# Save data for use in R, MS Excel, or other software
data = np.zeros((len(step),11))
data[:,0] = step
data[:,1] = etruexy
data[:,2] = etruexz
data[:,3] = etrueyz
data[:,4] = sxx_ave
data[:,5] = syy_ave
data[:,6] = szz_ave
data[:,7] = sxy_ave
data[:,8] = sxz_ave
data[:,9] = syz_ave
data[:,10] = direction
csvtitle = filename.split('.')[0] + '_Stress_Strain_Data' + '.csv'
np.savetxt(csvtitle,data,delimiter=",",header="timestep,true strain in xy, true strain in xz, true strain in yz, true stress in x, true stress in y, true stress in z, true stress in xy, true stress in xz, true stress in yz, direction")
print("Data file ready for R analysis has been saved as {}\n".format(csvtitle))

        
        
    