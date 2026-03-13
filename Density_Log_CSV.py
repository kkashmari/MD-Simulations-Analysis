import log  # From Pizza.py
import os
import numpy as np

def calculate_average_of_last_n(data, column_index1, column_index2, n=500):
    if len(data) < n:
        raise ValueError("Not enough data points to calculate the average.")
    return np.mean(data[-n:, column_index1]), np.mean(data[-n:, column_index2])

def Density_Log_CSV(directory, filename, column_index1, column_index2, n=500):
    # Set directory and filename information
    os.chdir(directory)
    
    # Open log file and strip all lines with a warning about bond/angle/dihedral extent
    with open(filename, 'r') as logfile:
        log_contents = logfile.read().split('\n')
    
    # Iterate through log contents
    log_contents = [line for line in log_contents if 'WARNING: Bond/angle/dihedral extent > half of periodic box length (../domain.cpp:903)' not in line]
        
    # Write "new" logfile to file
    temp_filename = filename.split('.')[0] + "_temp.log.lammps"
    with open(temp_filename, 'w') as newlogfile:
        for line in log_contents:
            newlogfile.write(line + "\n")
        
    # Load thermo-dynamic data using log module
    thermo = log.log(temp_filename)
    
    # Delete temp log file
    os.remove(temp_filename)
    
    # Extract all data
    step, Temperature, Density, Volume = thermo.get("Step", "Temp", "Density", "Volume")
    
    # Put extracted data into numpy array
    data = np.array([step, Temperature, Density, Volume]).T
    
    # Save data to CSV
    csvtitle = filename.split('.')[0] + '.csv'
    np.savetxt(csvtitle, data, delimiter=",", header="timestep,Temperature,Density,Volume", fmt='%.8f')
    print(f"Data file ready for R analysis has been saved as {csvtitle}\n")

    # Calculate average of the last n data points in the specified columns
    try:
        average1, average2 = calculate_average_of_last_n(data, column_index1, column_index2, n)
        print(f"The average of the last {n} data points in column index {column_index1} is {average1:.8f}")
        print(f"The average of the last {n} data points in column index {column_index2} is {average2:.8f}")
    except ValueError as e:
        print(f"An error occurred while calculating the average: {e}")

if __name__ == "__main__":
    directory = "/Users/khatereh/Desktop/Research/ProcessModeling/Cynate_ester/Cyanate_Ester_datafile/5/Seq_180K/Equilibrated_300K"
    filename = "PolyCE5_p95_nptr_300K_r_Recharged.log.lammps"
    column_index1 = 2  # Index of the first column to calculate the average (e.g., 2 for Density)
    column_index2 = 3  # Index of the second column to calculate the average
    n = 500  # Number of data points to average

    Density_Log_CSV(directory, filename, column_index1, column_index2, n)
