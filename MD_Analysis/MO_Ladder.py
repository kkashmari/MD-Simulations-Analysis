import matplotlib.pyplot as plt
from pymatgen.io.vasp.outputs import Vasprun

vasp = Vasprun("vasprun.xml")
eigenvalues = vasp.eigenvalues

energies = []
occupations = []

# Gamma-only assumed
for spin in eigenvalues:
    for kpoint in eigenvalues[spin]:
        for band in kpoint:
            energies.append(band[0])
            occupations.append(band[1])

# Sort by energy
orbitals = sorted(zip(energies, occupations), key=lambda x: x[0])

# Find HOMO index
homo_index = max(i for i, (_, occ) in enumerate(orbitals) if occ > 0.5)
lumo_index = homo_index + 1

homo_energy = orbitals[homo_index][0]
lumo_energy = orbitals[lumo_index][0]
gap = lumo_energy - homo_energy

# Select frontier region (±5 orbitals)
window = 5
start = max(0, homo_index - window)
end = min(len(orbitals), lumo_index + window)

frontier = orbitals[start:end]

# Shift energies so HOMO = 0
relative_orbitals = [(energy - homo_energy, occ) for energy, occ in orbitals]

relative_homo = 0
relative_lumo = lumo_energy - homo_energy
gap = relative_lumo

# Select frontier region
window = 5
start = max(0, homo_index - window)
end = min(len(relative_orbitals), homo_index + window + 1)

frontier = relative_orbitals[start:end]

plt.figure(figsize=(4,6))

for energy, occ in frontier:
    if abs(energy - relative_homo) < 1e-6:
        plt.hlines(energy, 0.4, 0.6, linewidth=3, color='blue')
    elif abs(energy - relative_lumo) < 1e-6:
        plt.hlines(energy, 0.4, 0.6, linewidth=3, color='red')
    else:
        plt.hlines(energy, 0.45, 0.55, linewidth=1.5, color='black')

plt.axhspan(0, relative_lumo, alpha=0.1)

plt.ylabel("Energy (eV, relative to HOMO)")
plt.xticks([])
plt.ylim(-2, relative_lumo + 1)

plt.title(f"Frontier Molecular Orbitals\nHOMO–LUMO Gap = {gap:.2f} eV")

plt.tight_layout()
plt.show()