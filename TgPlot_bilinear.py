
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import convolve
import statsmodels.api as sm
import pwlf
import os

tgfile = "PEEKPoly1_TgCooling2.txt"
tgdat = pd.read_csv(tgfile, delim_whitespace=True, header=None)

tgfilename = os.path.splitext(tgfile)[0]

print(tgdat.shape)

# Remove first column (R: tgdat <- tgdat[,-1])
tgdat = tgdat.iloc[:, 1:]

print(tgdat.shape)

tgtemp = tgdat.iloc[:, 0].values      # R: tgdat[,1]
tgdens = tgdat.iloc[:, 11].values     # R: tgdat[,12]

X = sm.add_constant(tgtemp)
lin_mod = sm.OLS(tgdens, X).fit()

pwlf_model = pwlf.PiecewiseLinFit(tgtemp, tgdens)

# Initial guess psi = 416
breaks = pwlf_model.fit_with_breaks([tgtemp.min(), 416, tgtemp.max()])

tg_value = breaks[1]

tg_value_stderror = np.nan

def moving_average(x, n):
    return convolve(x, np.ones(n) / n, mode="same")

tgdens_ma = moving_average(tgdens, 50)

beta0, beta1 = lin_mod.params
tg_y_value = beta1 * tg_value + beta0

plt.figure()
plt.plot(tgdat.iloc[:100, 0], tgdat.iloc[:100, 14])
plt.show()

plt.figure()
plt.scatter(tgtemp, tgdens, color="blue")
plt.xlim(100, 600)
plt.ylim(1.1, 1.30)
plt.xlabel("Temperature (Kelvin)")
plt.ylabel("Density (g/cc)")

x_hat = np.linspace(100, 600, 500)
y_hat = pwlf_model.predict(x_hat)
plt.plot(x_hat, y_hat, color="red")

# Tg point (triangle)
plt.scatter(tg_value, tg_y_value, marker="^",
            facecolors="white", edgecolors="black")

plt.savefig(f"{tgfilename}.pdf")
plt.close()

plt.figure()
plt.plot(tgtemp, tgdens_ma, color="lightskyblue")
plt.xlim(100, 600)
plt.ylim(1.1, 1.30)
plt.xlabel("Temperature (K)", fontsize=14)
plt.ylabel("Density (g/cc)", fontsize=14)

x1 = np.linspace(300, tg_value + 30, 200)
y1 = beta1 * x1 + beta0
plt.plot(x1, y1, color="black")

x2 = np.linspace(tg_value - 30, 600, 200)
y2 = 1.381 + (-0.0002156) * x2
plt.plot(x2, y2, color="black")

# Tg point
plt.scatter(tg_value, tg_y_value, color="black")

plt.savefig(f"{tgfilename}_ma.pdf")
plt.close()


tg_data = pd.DataFrame({
    "tg_value": [tg_value],
    "tg_value_stderror": [tg_value_stderror]
})

tg_data.to_csv(f"{tgfilename}.txt", sep="\t", index=False)
