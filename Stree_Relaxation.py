import numpy as np

def compute_sacf(stress):
    stress = np.array(stress)
    stress -= np.mean(stress) 
    n = len(stress)
    result = np.correlate(stress, stress, mode='full')
    result = result[n - 1:]  # keep only non-negative time lags
    result /= np.arange(n, 0, -1)  # normalize by number of samples at each lag
    result /= result[0]  # optional: normalize so C(0) = 1
    return result