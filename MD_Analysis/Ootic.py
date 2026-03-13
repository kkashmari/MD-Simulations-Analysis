import numpy as np
import matplotlib.pyplot as plt

# Load data
abs_data = np.loadtxt('ABSORPTION_2D.dat')
ref_data = np.loadtxt('REFLECTION_2D.dat')
trans_data = np.loadtxt('TRANSMISSION_2D.dat')
cond_data = np.loadtxt('REAL_OPTICAL_CONDUCTIVITY_2D.dat')

# Extract columns
E_abs, A = abs_data[:,0], abs_data[:,1]
E_ref, R = ref_data[:,0], ref_data[:,1]
E_trans, T = trans_data[:,0], trans_data[:,1]
E_cond, sigma = cond_data[:,0], cond_data[:,1]

# Plot settings
plt.rcParams.update({
    "font.size": 14,
    "figure.figsize": (6,4),
    "axes.linewidth": 1.5
})

# 1. Absorption
plt.figure()
plt.plot(E_abs, A, color='red', linewidth=2)
plt.xlabel("Photon Energy (eV)")
plt.ylabel("Absorption")
plt.title("Absorption Spectrum")
plt.tight_layout()
plt.show()

# 2. Reflection
plt.figure()
plt.plot(E_ref, R, color='green', linewidth=2)
plt.xlabel("Photon Energy (eV)")
plt.ylabel("Reflection")
plt.title("Reflection Spectrum")
plt.tight_layout()
plt.show()

# 3. Transmission
plt.figure()
plt.plot(E_trans, T, color='blue', linewidth=2)
plt.xlabel("Photon Energy (eV)")
plt.ylabel("Transmission")
plt.title("Transmission Spectrum")
plt.tight_layout()
plt.show()

# 4. Optical Conductivity
plt.figure()
plt.plot(E_cond, sigma, color='purple', linewidth=2)
plt.xlabel("Photon Energy (eV)")
plt.ylabel("Optical Conductivity")
plt.title("Optical Conductivity")
plt.tight_layout()
plt.show()