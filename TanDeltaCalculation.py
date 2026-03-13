import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from scipy.fft import fft, fftfreq
from pathlib import Path
import matplotlib.pyplot as plt

class AutoTanDelta:
    def __init__(self, time, strain, stress):
        self.time = time
        self.strain = strain
        self.stress = stress
        self.raw_strain = strain.copy()
        self.raw_stress = stress.copy()
        self.sample_rate = 1 / (time[1] - time[0])
        self.window_scale = 1  
        self.fundamental_freq = None
        self.freq_tolerance = 0.01  
        self.smoothing_applied = False

    def perform_fft(self, signal):
        n = len(self.time)
        signal_fft = fft(signal)
        freqs = fftfreq(n, 1 / self.sample_rate)
        dominant_idx = np.argmax(np.abs(signal_fft[1:])) + 1
        return freqs[dominant_idx]

    def smooth_signals(self):
        window_length = int(self.sample_rate / self.fundamental_freq / self.window_scale)
        if window_length >= len(self.time):
            window_length = len(self.time) - 1 if len(self.time) % 2 == 0 else len(self.time)
        if window_length % 2 == 0:
            window_length -= 1
        if window_length < 5:
            window_length = 5

        self.strain = savgol_filter(self.strain , window_length, 3)
        self.stress = savgol_filter(self.stress, window_length, 3)
        self.smoothing_applied = True

    def match_frequencies(self):
        freq_strain = self.perform_fft(self.strain)
        freq_stress = self.perform_fft(self.stress)
        match = abs(freq_strain - freq_stress) / freq_strain < self.freq_tolerance
        return match, freq_strain, freq_stress

    def plot_signals(self):
        plt.figure(figsize=(12, 12))

        plt.subplot(5, 1, 1)
        plt.plot(self.time, self.raw_strain, label='Raw Strain', color='gray')
        plt.title('Raw Strain')
        plt.ylabel('Strain')
        plt.grid(True)

        plt.subplot(5, 1, 2)
        plt.plot(self.time, self.raw_stress, label='Raw Stress', color='black')
        plt.title('Raw Stress')
        plt.ylabel('Stress')
        plt.grid(True)

        if self.smoothing_applied:
            plt.subplot(5, 1, 3)
            plt.plot(self.time, self.strain, label='Smoothed Strain', color='blue')
            plt.title('Smoothed Strain')
            plt.ylabel('Strain')
            plt.grid(True)

            plt.subplot(5, 1, 4)
            plt.plot(self.time, self.stress, label='Smoothed Stress', color='orange')
            plt.title('Smoothed Stress')
            plt.ylabel('Stress')
            plt.grid(True)

            plt.subplot(5, 1, 5)
            plt.plot(self.time, self.raw_strain, label='Raw Strain', color='gray', linestyle='--')
            plt.plot(self.time, self.raw_stress, label='Raw Stress', color='black', linestyle='--')
            plt.plot(self.time, self.strain, label='Smoothed Strain', color='blue')
            plt.plot(self.time, self.stress, label='Smoothed Stress', color='orange')
            plt.title('Overlay: Raw vs Smoothed Strain and Stress')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        plt.show()

    def analyze(self):
        match, freq_strain, freq_stress = self.match_frequencies()
        self.fundamental_freq = (freq_strain + freq_stress) / 2

        while not match:
            print(f" Frequencies do not match: Strain = {freq_strain:.3e} Hz, Stress = {freq_stress:.3e} Hz")
            print(" Applying smoothing and retrying...")
            self.smooth_signals()
            self.window_scale *= 1.5

            match, freq_strain, freq_stress = self.match_frequencies()
            if self.window_scale > 10:
                print(" Frequencies still don't match after multiple smoothing attempts.")
                print(" Try increasing initial smoothing or check signal quality.")
                return False

        if match:
            print(f" Frequencies matched: {freq_strain:.3e} Hz")

            strain_fft = fft(self.strain)
            stress_fft = fft(self.stress)
            dom_idx = np.argmax(np.abs(stress_fft[1:])) + 1

            strain_amp = np.abs(strain_fft[dom_idx]) / len(self.time)
            stress_amp = np.abs(stress_fft[dom_idx]) / len(self.time)

            print(f"Strain Amplitude: {strain_amp:.5e}")
            print(f"Stress Amplitude: {stress_amp:.5e}")

            phase_angle = np.angle(stress_fft[dom_idx]) - np.angle(strain_fft[dom_idx])
            if phase_angle < 0:
                phase_angle += 2 * np.pi
            phase_deg = np.degrees(phase_angle)
            if phase_deg > 180:
                print(f" Phase angle {phase_deg:.2f}° is greater than 180°, adjusting by 360 - δ")
                phase_deg = 360 - phase_deg
            elif phase_deg > 90:
                print(f" Phase angle {phase_deg:.2f}° is greater than 90°, adjusting by 180 - δ")
                phase_deg = 180 - phase_deg
            phase_angle = np.radians(phase_deg)

            G_star = stress_amp / strain_amp
            G_prime = G_star * np.cos(phase_angle)
            G_double_prime = G_star * np.sin(phase_angle)
            tan_delta = G_double_prime / G_prime

            print(f"Storage Modulus G': {G_prime:.4f}")
            print(f"Loss Modulus G'': {G_double_prime:.4f}")
            print(f"tan(δ): {tan_delta:.4f}")
            print(f"δ (degrees): {phase_deg:.2f}°")

            self.plot_signals()

            return True

if __name__ == "__main__":
        input_path = input("Enter the path to your CSV file (or leave blank to use uploaded file): ").strip()

        if Path(input_path).exists():
            data = pd.read_csv(input_path, header=None)
            data.columns = ['Time_ps', 'Strain', 'Stress']
            time = data['Time_ps'].values * 1e-12
            strain = data['Strain'].values
            stress = data['Stress'].values
    
            analyzer = AutoTanDelta(time, strain, stress)
            analyzer.analyze()
        else:
            print(f" File not found: {input_path}")
