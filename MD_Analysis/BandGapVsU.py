import matplotlib.pyplot as plt
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.core import Spin
import os
import numpy as np

U_values = list(range(0, 8))
gaps = []

for U in U_values:

    folder = f"{U}"
    vasprun_path = os.path.join(folder, "vasprun.xml")

    if not os.path.exists(vasprun_path):
        gaps.append(None)
        continue

    print(f"Processing U={U}")

    vasp = Vasprun(vasprun_path)
    eigenvalues = vasp.eigenvalues
    efermi = vasp.efermi

    vbm = -1e10
    cbm =  1e10

    for spin in eigenvalues:
        for kpoint in eigenvalues[spin]:
            for band in kpoint:
                energy = band[0]

                if energy <= efermi:
                    vbm = max(vbm, energy)
                else:
                    cbm = min(cbm, energy)

    gap = max(cbm - vbm, 0)
    gaps.append(gap)

U_clean = [u for u, g in zip(U_values, gaps) if g is not None]
gaps_clean = [g for g in gaps if g is not None]

plt.figure(figsize=(7,5))
plt.plot(U_clean, gaps_clean, marker='o', linewidth=2)

plt.xlabel("Hubbard U (eV)")
plt.ylabel("Band Gap (eV)")
#plt.title("Band Gap Evolution in MnO with Hubbard U")

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
