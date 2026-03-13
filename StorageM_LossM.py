import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import find_peaks

#Input
csv_file = "stress_strain_data.csv"  
time_col = "time_ps"
stress_col = "stress_mpa"
strain_col = "strain"

n_keep = 1 #Number of Frequencies to check

# Data
df = pd.read_csv(csv_file)

time_ps = df[time_col].values
stress = df[stress_col].values
strain = df[strain_col].values

idx = np.argsort(time_ps)
time_ps = time_ps[idx]
stress = stress[idx]
strain = strain[idx]

dt_ps = np.mean(np.diff(time_ps))
n = len(time_ps)

#Filtering in Frequency domain
freq = fftfreq(n, d=dt_ps)   # unit: 1/ps

stress_fft = fft(stress)
strain_fft = fft(strain)

stress_psd = np.abs(stress_fft) ** 2 / n
strain_psd = np.abs(strain_fft) ** 2 / n

# check the frequencies 
pos_mask = freq > 0
freq_pos = freq[pos_mask]
stress_psd_pos = stress_psd[pos_mask]
strain_psd_pos = strain_psd[pos_mask]
stress_fft_pos = stress_fft[pos_mask]
strain_fft_pos = strain_fft[pos_mask]


# strain to find the loading frequency
peaks, _ = find_peaks(strain_psd_pos)

if len(peaks) == 0:
    # fallback: use maximum PSD 
    dom_idx_local = np.argmax(strain_psd_pos)
else:

    strongest_peak = peaks[np.argmax(strain_psd_pos[peaks])]
    dom_idx_local = strongest_peak

f0 = freq_pos[dom_idx_local]   # dominant frequency [1/ps]

print(f"Dominant frequency = {f0:.6e} 1/ps")


def filter_signal_by_frequency(signal, freq, target_freq, n_keep=1):
    """
    Keep the strongest n_keep positive-frequency components closest to target_freq,
    plus their negative-frequency counterparts.
    """
    F = fft(signal)
    filtered_F = np.zeros_like(F, dtype=complex)

    pos_indices = np.where(freq > 0)[0]
    pos_freq = freq[pos_indices]

    # sort by distance to target frequency
    dist = np.abs(pos_freq - target_freq)
    candidate_order = np.argsort(dist)

    kept = 0
    used = []

    for k in candidate_order:
        idx_pos = pos_indices[k]
        if np.abs(F[idx_pos]) > 0:
            idx_neg = np.where(np.isclose(freq, -freq[idx_pos]))[0]
            filtered_F[idx_pos] = F[idx_pos]
            if len(idx_neg) > 0:
                filtered_F[idx_neg[0]] = F[idx_neg[0]]
            used.append(idx_pos)
            kept += 1
        if kept >= n_keep:
            break

    filtered_signal = np.real(ifft(filtered_F))
    return filtered_signal, filtered_F, used

stress_filt, stress_filt_fft, stress_used = filter_signal_by_frequency(
    stress, freq, f0, n_keep=n_keep
)
strain_filt, strain_filt_fft, strain_used = filter_signal_by_frequency(
    strain, freq, f0, n_keep=n_keep
)

# Go back to time domain

def get_amp_phase_from_fft(filtered_F, freq, target_freq, n):
    idx = np.argmin(np.abs(freq - target_freq))
    coeff = filtered_F[idx]

    # For real signal: amplitude = 2*|Ck|/N for nonzero frequency
    amplitude = 2.0 * np.abs(coeff) / n
    phase = np.angle(coeff)
    return amplitude, phase, idx

sigma0, phi_sigma, idx_sigma = get_amp_phase_from_fft(stress_filt_fft, freq, f0, n)
gamma0, phi_gamma, idx_gamma = get_amp_phase_from_fft(strain_filt_fft, freq, f0, n)

delta = phi_sigma - phi_gamma

# wrap phase lag to [-pi, pi]
delta = np.arctan2(np.sin(delta), np.cos(delta))

#compute G' and G"

G_star = sigma0 / gamma0
Gp = G_star * np.cos(delta) #MPa
Gpp = G_star * np.sin(delta)

print("\n===== Viscoelastic results =====")
print(f"Stress amplitude sigma0 = {sigma0:.6f} MPa")
print(f"Strain amplitude gamma0 = {gamma0:.6f}")
print(f"Phase lag delta = {delta:.6f} rad = {np.degrees(delta):.3f} deg")
print(f"|G*| = {G_star:.6f} MPa")
print(f"G'  = {Gp:.6f} MPa")
print(f'G"  = {Gpp:.6f} MPa')

stress_peaks, _ = find_peaks(stress_psd_pos)
strain_peaks, _ = find_peaks(strain_psd_pos)

#Just for vizualizations

def top_peaks(freq_pos, psd_pos, peaks, n_show=3):
    if len(peaks) == 0:
        return np.array([]), np.array([])
    top = peaks[np.argsort(psd_pos[peaks])[-n_show:]]
    return freq_pos[top], psd_pos[top]

stress_peak_freqs, stress_peak_vals = top_peaks(freq_pos, stress_psd_pos, stress_peaks, n_show=3)
strain_peak_freqs, strain_peak_vals = top_peaks(freq_pos, strain_psd_pos, strain_peaks, n_show=3)

#Plots

fig, axes = plt.subplots(3, 2, figsize=(14, 10))
plt.subplots_adjust(hspace=0.4, wspace=0.35)

# 1) Stress PSD
ax = axes[0, 0]
ax.plot(freq_pos, stress_psd_pos, 'o', markersize=4, color='tab:orange', label='PSD')
if len(stress_peak_freqs) > 0:
    ax.scatter(stress_peak_freqs, stress_peak_vals, s=35, color='tab:cyan', label='Filtered Peaks', zorder=3)
ax.set_title("Stress Power Spectrum")
ax.set_xlabel("Frequency [1/ps]")
ax.set_ylabel("PSD")
ax.legend()
ax.grid(True, alpha=0.4)

# 2) Stress over time
ax = axes[0, 1]
ax.plot(time_ps, stress, lw=1.2, color='tab:blue', label='Raw Stress')
ax.plot(time_ps, stress_filt, '--', lw=1.5, color='tab:cyan', label='Filtered Stress')
ax.set_title("Stress Over Time")
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Stress (MPa)")
ax.legend()
ax.grid(True, alpha=0.4)

# 3) Strain PSD
ax = axes[1, 0]
ax.plot(freq_pos, strain_psd_pos, 'o', markersize=4, color='tab:red', label='PSD')
if len(strain_peak_freqs) > 0:
    ax.scatter(strain_peak_freqs, strain_peak_vals, s=35, color='lightgreen', label='Filtered Peaks', zorder=3)
ax.set_title("Strain Power Spectrum")
ax.set_xlabel("Frequency [1/ps]")
ax.set_ylabel("PSD")
ax.legend()
ax.grid(True, alpha=0.4)

# 4) Strain over time
ax = axes[1, 1]
ax.plot(time_ps, strain, lw=1.5, color='tab:green', label='Raw Strain')
ax.plot(time_ps, strain_filt, '--', lw=1.5, color='lightgreen', label='Filtered Strain')
ax.set_title("Strain Over Time")
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Strain")
ax.legend()
ax.grid(True, alpha=0.4)

# 5) Raw stress and strain dual axis
ax1 = axes[2, 0]
ax2 = ax1.twinx()
ax1.plot(time_ps, strain, color='tab:green', lw=1.5)
ax2.plot(time_ps, stress, color='tab:blue', lw=1.2)
ax1.set_title("Raw Stress and Strain (Dual Axis)")
ax1.set_xlabel("Time (ps)")
ax1.set_ylabel("Strain", color='tab:green')
ax2.set_ylabel("Stress (MPa)", color='tab:blue')
ax1.grid(True, alpha=0.4)

# 6) Filtered stress and strain dual axis
ax1 = axes[2, 1]
ax2 = ax1.twinx()
ax1.plot(time_ps, strain_filt, color='tab:green', lw=1.6)
ax2.plot(time_ps, stress_filt, color='tab:cyan', lw=1.6)
ax1.set_title("Filtered Stress and Strain (Dual Axis)")
ax1.set_xlabel("Time (ps)")
ax1.set_ylabel("Strain", color='tab:green')
ax2.set_ylabel("Stress (MPa)", color='tab:cyan')
ax1.grid(True, alpha=0.4)

plt.suptitle(
    f"Dynamic Mechanical Analysis from Time Series\n"
    f"f0 = {f0:.4e} 1/ps,  G' = {Gp:.4f} MPa,  G\" = {Gpp:.4f} MPa",
    fontsize=14,
    y=0.98
)

plt.show()