import numpy as np
import matplotlib.pyplot as plt

doscar = "DOSCAR"

with open(doscar) as f:
    lines = f.readlines()

# number of atoms
natoms = int(lines[0].split()[0])

# DOS header line
header = lines[5].split()

emin = float(header[0])
emax = float(header[1])
nedos = int(header[2])
efermi = float(header[3])

energy = []
dos_up = []
dos_down = []

# read total DOS
for i in range(6, 6 + nedos):

    data = lines[i].split()

    e = float(data[0]) - efermi
    up = float(data[1])
    down = float(data[2])

    energy.append(e)
    dos_up.append(up)
    dos_down.append(down)

energy = np.array(energy)
dos_up = np.array(dos_up)
dos_down = np.array(dos_down)

# plot
plt.figure(figsize=(8,6))

plt.plot(energy, dos_up, label="Spin Up", color="blue")
plt.plot(energy, -dos_down, label="Spin Down", color="red")

plt.axvline(0, linestyle="--", color="black")

plt.xlabel("Energy (eV)")
plt.ylabel("Density of States")
plt.title("Spin-Polarized DOS (MnO)")

plt.legend()

plt.show()