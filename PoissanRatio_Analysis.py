#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: khatereh
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pwlf

os.chdir("/Users/khaterekashmari/Desktop/Large_System/SuperCellPEEK/Poisson_Ratio/5")
ym_file = "PEEKCr5_E3_Stress_Strain_Data.csv"
ym_filename = ym_file.split(".")[0]

ym_dat = pd.read_csv(ym_file)

timestep = ym_dat.iloc[:, 0].values
etruex = ym_dat.iloc[:, 1].values
etruey = ym_dat.iloc[:, 2].values
etruez = ym_dat.iloc[:, 3].values
sxx = ym_dat.iloc[:, 4].values
syy = ym_dat.iloc[:, 5].values
szz = ym_dat.iloc[:, 6].values
direction = ym_dat.iloc[:, 7].values

print("\n")

if direction[0] == 1:
    primary_strain = etruex
    secondary_strain1 = etruey
    secondary_strain2 = etruez
    Nu1_name = f"{ym_filename}_Nuxy"
    Nu2_name = f"{ym_filename}_Nuxz"
    Nu1_label = r"$\nu_{xy}$"
    Nu2_label = r"$\nu_{xz}$"

elif direction[0] == 2:
    primary_strain = etruey
    secondary_strain1 = etruex
    secondary_strain2 = etruez
    Nu1_name = f"{ym_filename}_Nuyx"
    Nu2_name = f"{ym_filename}_Nuyz"
    Nu1_label = r"$\nu_{yx}$"
    Nu2_label = r"$\nu_{yz}$"

elif direction[0] == 3:
    primary_strain = etruez
    secondary_strain1 = etruex
    secondary_strain2 = etruey
    Nu1_name = f"{ym_filename}_Nuzx"
    Nu2_name = f"{ym_filename}_Nuzy"
    Nu1_label = r"$\nu_{zx}$"
    Nu2_label = r"$\nu_{zy}$"

nu_strainp1 = primary_strain
nu_strainp2 = primary_strain
nu_strain1 = secondary_strain1
nu_strain2 = secondary_strain2

X1 = sm.add_constant(nu_strainp1)
model1 = sm.OLS(nu_strain1, X1).fit()

X2 = sm.add_constant(nu_strainp2)
model2 = sm.OLS(nu_strain2, X2).fit()

pwlf1 = pwlf.PiecewiseLinFit(nu_strainp1, nu_strain1)
breaks1 = pwlf1.fit(2)

pwlf2 = pwlf.PiecewiseLinFit(nu_strainp2, nu_strain2)
breaks2 = pwlf2.fit(2)

Nu1_value = pwlf1.slopes[0]
Nu2_value = pwlf2.slopes[0]

Nu1_intercept = pwlf1.intercepts[0]
Nu2_intercept = pwlf2.intercepts[0]

df_Nu1 = pd.DataFrame({
    "Nu_value": [Nu1_value],
    "Intercept": [Nu1_intercept]
})
df_Nu2 = pd.DataFrame({
    "Nu_value": [Nu2_value],
    "Intercept": [Nu2_intercept]
})

df_Nu1.to_csv(f"{Nu1_name}_Numeric_Values.txt", sep="\t", index=False)
df_Nu2.to_csv(f"{Nu2_name}_Numeric_Values.txt", sep="\t", index=False)

Nu1_x_value = breaks1[1]
Nu1_y_value = Nu1_value * Nu1_x_value + Nu1_intercept

Nu2_x_value = breaks2[1]
Nu2_y_value = Nu2_value * Nu2_x_value + Nu2_intercept
Nu1_display = -round(Nu1_value, 4)
Nu2_display = -round(Nu2_value, 4)

plt.figure()
plt.scatter(primary_strain, secondary_strain1, color='black', s=5)
x_hat = np.linspace(0, max(primary_strain), 100)
plt.plot(x_hat, pwlf1.predict(x_hat), color='red', linewidth=2)
plt.scatter(Nu1_x_value, Nu1_y_value, s=80)
plt.title(f"{Nu1_label} = {Nu1_display}")
plt.xlabel("Primary True Strain")
plt.ylabel("Secondary True Strain")
plt.savefig(f"{Nu1_name}.pdf")
plt.close()

plt.figure()
plt.scatter(primary_strain, secondary_strain2, color='black', s=5)
plt.plot(x_hat, pwlf2.predict(x_hat), color='red', linewidth=2)
plt.scatter(Nu2_x_value, Nu2_y_value, s=80)
plt.title(f"{Nu2_label} = {Nu2_display}")
plt.xlabel("Primary True Strain")
plt.ylabel("Secondary True Strain")
plt.savefig(f"{Nu2_name}.pdf")
plt.close()

print("\nPoisson's ratio analysis complete!")
print(f"Plot 1: {Nu1_name}.pdf")
print(f"Plot 2: {Nu2_name}.pdf")
print(f"Text file 1: {Nu1_name}_Numeric_Values.txt")
print(f"Text file 2: {Nu2_name}_Numeric_Values.txt")
