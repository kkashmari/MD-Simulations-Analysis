import matplotlib.pyplot as plt

atoms = ['Mn1','Mn2','Mn3','Mn4']
moments = [4.545,-4.545, 4.545,-4.545]

plt.figure(figsize=(6,4))
plt.bar(atoms, moments)

plt.axhline(0, linewidth=1)
plt.ylabel("Magnetic moment (μB)")
plt.title("Magnetic moment per Mn atom")

plt.show()