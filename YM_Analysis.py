#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: khatereh
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


WORKING_DIRECTORY = "/Users/khaterekashmari/Desktop/Large_System/SuperCellPEEK/YoungM/1"
CSV_FILENAME = "PEEKCr_E3_Stress_Strain_Data.csv"
ENDPOINT = 1500  

os.chdir(WORKING_DIRECTORY)

ym_filename = CSV_FILENAME.split(".")[0]
ym_dat = pd.read_csv(CSV_FILENAME)

etruex = ym_dat.iloc[:, 1].values
etruey = ym_dat.iloc[:, 2].values
etruez = ym_dat.iloc[:, 3].values
sxx = ym_dat.iloc[:, 4].values
syy = ym_dat.iloc[:, 5].values
szz = ym_dat.iloc[:, 6].values
direction = ym_dat.iloc[:, 7].values

if direction[0] == 1:
    primary_strain = etruex
    primary_stress = sxx
    E_label = "E_xx"
    E_name = f"{ym_filename}_sxx_etruex"

elif direction[0] == 2:
    primary_strain = etruey
    primary_stress = syy
    E_label = "E_yy"
    E_name = f"{ym_filename}_syy_etruey"

elif direction[0] == 3:
    primary_strain = etruez
    primary_stress = szz
    E_label = "E_zz"
    E_name = f"{ym_filename}_szz_etruez"

else:
    raise ValueError("Invalid loading direction in CSV.")

strain = primary_strain[:ENDPOINT]
stress = primary_stress[:ENDPOINT]

def linear_fit(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return slope, intercept

def find_best_breakpoint(x, y, min_index=50):
    best_error = np.inf
    best_index = None

    for i in range(min_index, len(x) - min_index):
        slope1, intercept1 = linear_fit(x[:i], y[:i])
        slope2, intercept2 = linear_fit(x[i:], y[i:])

        y1_pred = slope1 * x[:i] + intercept1
        y2_pred = slope2 * x[i:] + intercept2

        error = np.sum((y[:i] - y1_pred)**2) + np.sum((y[i:] - y2_pred)**2)

        if error < best_error:
            best_error = error
            best_index = i

    return best_index

break_index = find_best_breakpoint(strain, stress)

E_value, E_intercept = linear_fit(strain[:break_index], stress[:break_index])

yield_strain_value = strain[break_index]
yield_stress_value = E_value * yield_strain_value + E_intercept

# Convert to GPa
E_display = round(E_value / 1000.0, 2)

results = pd.DataFrame({
    "Youngs_Modulus_MPa": [E_value],
    "Yield_Strain": [yield_strain_value],
    "Yield_Stress_MPa": [yield_stress_value],
    "Intercept": [E_intercept]
})

results.to_csv(f"{E_name}_Numeric_Values.txt", sep="\t", index=False)

plt.figure(figsize=(6,5))
plt.scatter(primary_strain, primary_stress, s=5, color="black")

x_fit = np.linspace(0, max(primary_strain), 200)
plt.plot(x_fit, E_value * x_fit + E_intercept, color="red", linewidth=2)

plt.scatter(yield_strain_value, yield_stress_value, s=80)

plt.title(f"{E_label} = {E_display} GPa")
plt.xlabel("True Strain")
plt.ylabel("True Stress (MPa)")

plt.savefig(f"{E_name}_Plot.pdf")
plt.close()

print("\nYoung's modulus analysis complete!")
print(f"{E_label} = {E_display} GPa")
print("Plot and numeric results saved.")
