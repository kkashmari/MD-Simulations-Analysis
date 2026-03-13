import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.fft import fft, fftfreq

file_path = 'PBD_MD_NVT_50ns_GK_2.xlsx' 
df = pd.read_excel(file_path, usecols=['time(ps)', 'xy', 'vol(A3)'], nrows=50000)

time = df['time(ps)'].values  # Time in ps
stress = df['xy'].values      # Shear stress (Pxy)
volume = df['vol(A3)'].mean() * 1e-30 

def compute_sacf(signal):
    signal -= np.mean(signal)
    n = len(signal)
    result = np.correlate(signal, signal, mode='full')[n - 1:] / np.arange(n, 0, -1)
    result /= result[0] 
    return result

sacf = compute_sacf(stress)
dt = time[1] - time[0]  # Time step in ps

kB = 1.38064852e-23  # Boltzmann constant (J/K)
T = 300  # Temperature in K
G_t = (volume / (kB * T)) * sacf  # G(t) in Pa

plt.figure()
plt.plot(time[:len(G_t)], G_t)
plt.title("Relaxation Modulus G(t)")
plt.xlabel("Time (ps)")
plt.ylabel("G(t) (Pa)")
plt.grid(True)
plt.tight_layout()
plt.show()
