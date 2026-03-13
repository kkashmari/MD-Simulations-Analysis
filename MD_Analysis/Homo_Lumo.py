from pymatgen.io.vasp import Vasprun
import numpy as np
import matplotlib.pyplot as plt

# -------- read vasprun --------
v = Vasprun("vasprun.xml", parse_eigen=True)

# try to get Fermi level
Efermi = v.efermi

# fallback: read from OUTCAR
if Efermi is None:
    with open("OUTCAR") as f:
        for line in f:
            if "E-fermi" in line:
                Efermi = float(line.split()[2])
                break

print("Fermi level:", Efermi)

# -------- collect eigenvalues --------
energies = []

for spin in v.eigenvalues:
    for k in v.eigenvalues[spin]:
        for band in k:
            energies.append(band[0])

energies = np.array(energies)

# shift energies
energies = energies - Efermi

# -------- HOMO / LUMO --------
HOMO = np.max(energies[energies <= 0])
LUMO = np.min(energies[energies > 0])

gap = LUMO - HOMO

print("HOMO =", HOMO)
print("LUMO =", LUMO)
print("Gap =", gap)

# -------- plot --------
plt.figure(figsize=(4,6))

# energy levels
plt.hlines(HOMO,0.3,0.7,linewidth=4,color='royalblue')
plt.hlines(LUMO,0.3,0.7,linewidth=4,color='darkorange')

# fill the band gap region
plt.fill_between([0.3,0.7], HOMO, LUMO, color='lightgray', alpha=0.4)

# labels
plt.text(0.72,HOMO,f"HOMO = {HOMO:.2f} eV",va="center")
plt.text(0.72,LUMO,f"LUMO = {LUMO:.2f} eV",va="center")

# gap arrow
plt.annotate('',xy=(0.5,LUMO),xytext=(0.5,HOMO),
             arrowprops=dict(arrowstyle="<->",lw=2))

plt.text(0.52,(HOMO+LUMO)/2,f"Gap = {gap:.2f} eV")

plt.xlim(0,1)
plt.xticks([])
plt.ylabel("Energy (eV)")
plt.title("Band Gap")

plt.tight_layout()
plt.show()