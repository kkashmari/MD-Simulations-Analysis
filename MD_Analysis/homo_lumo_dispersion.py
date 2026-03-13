import matplotlib.pyplot as plt
from pymatgen.io.vasp.outputs import Vasprun
import os

methods = ["No_Dispersion","MB","dDsC","TSHP", "D2", "D3", "D3BJ", "TS"]
gaps = []

for method in methods:

    vasprun_path = os.path.join(method, "vasprun.xml")

    if not os.path.exists(vasprun_path):
        print(f"Missing {method}")
        gaps.append(None)
        continue

    vasp = Vasprun(vasprun_path)
    eigenvalues = vasp.eigenvalues

    homo = -1e10
    lumo =  1e10

    for spin in eigenvalues:
        for kpoint in eigenvalues[spin]:
            for band in kpoint:

                energy = band[0]
                occupation = band[1]

                if occupation > 0.5:
                    homo = max(homo, energy)
                else:
                    lumo = min(lumo, energy)

    gap = lumo - homo
    gaps.append(gap)

plt.figure(figsize=(6,4))
plt.plot(methods, gaps, marker='o', linewidth=2)
plt.ylabel("HOMO–LUMO Gap (eV)")
plt.title("Effect of Dispersion Correction on HOMO–LUMO Gap")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
for method in methods:

    vasprun_path = os.path.join(method, "vasprun.xml")

    if not os.path.exists(vasprun_path):
        print(f"Missing {method}")
        gaps.append(None)
        continue

    vasp = Vasprun(vasprun_path)
    eigenvalues = vasp.eigenvalues
    efermi = vasp.efermi

    homo = -1e10
    lumo =  1e10

    for spin in eigenvalues:
        for kpoint in eigenvalues[spin]:
            for band in kpoint:
                energy = band[0]

                if energy <= efermi:
                    homo = max(homo, energy)
                else:
                    lumo = min(lumo, energy)

    gap = lumo - homo
    gaps.append(gap)

plt.figure(figsize=(6,4))

plt.plot(methods, gaps, marker='o', linewidth=2)
plt.ylim(3.5, 4.5)
plt.ylabel("HOMO–LUMO Gap (eV)")
plt.title("Effect of Dispersion Correction on HOMO–LUMO Gap")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
