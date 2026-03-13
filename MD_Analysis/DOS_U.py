import matplotlib.pyplot as plt
from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.core import Spin, OrbitalType
import numpy as np
import os

# -------- Choose U values to plot --------
U_values = [0,1, 4, 6, 8, 10]   # change if needed

plt.figure(figsize=(9, 7))

for U in U_values:

    folder = f"{U}"
    vasprun_path = os.path.join(folder, "vasprun.xml")

    if not os.path.exists(vasprun_path):
        print(f"Missing file: {vasprun_path}")
        continue

    print(f"Processing U = {U}")

    # ---- Read VASP output ----
    vasp = Vasprun(vasprun_path, parse_projected_eigen=True)
    dos = vasp.complete_dos

    # ---- Shift energy relative to Fermi level ----
    energies = dos.energies - vasp.efermi

    # ---- Find Mn sites ---- #Change Based on the System of Interest
    mn_sites = [site for site in dos.structure if site.species_string == "Mn"]

    if len(mn_sites) == 0:
        print(f"No Mn found in structure for U={U}")
        continue

    # Use first site 
    mn_d_dos = dos.get_site_spd_dos(mn_sites[0])[OrbitalType.d]

    # ---- Spin Handling ----
    if Spin.down in mn_d_dos.densities:
        spin_up = mn_d_dos.get_densities(Spin.up)
        spin_down = mn_d_dos.get_densities(Spin.down)

        # Normalize
        spin_up = spin_up / np.max(spin_up)
        spin_down = spin_down / np.max(spin_down)

        # Plot
        plt.fill_between(
            energies, spin_up,
            alpha=0.3, label=f"U={U} (↑)"
        )
        plt.fill_between(
            energies, -spin_down,
            alpha=0.3, label=f"U={U} (↓)"
        )

    else:
        spin_up = mn_d_dos.get_densities(Spin.up)

        spin_up = spin_up / np.max(spin_up)

        plt.plot(
            energies, spin_up,
            linewidth=2, label=f"U={U}"
        )

# -------- Final Plot Formatting --------
plt.axvline(0, color="black", linestyle="--", linewidth=1)
plt.xlim(-8, 8)

plt.xlabel("Energy (eV)  (E - E$_F$)", fontsize=12)
plt.ylabel("Normalized DOS", fontsize=12)
#plt.title("Spin-Resolved Mn d-Projected DOS Evolution with Hubbard U", fontsize=13)

plt.legend(fontsize=8, ncol=2)
plt.tight_layout()

plt.show()
