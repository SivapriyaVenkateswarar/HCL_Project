import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

df = pd.read_csv("tamil_main_error_rate.csv")
df['percentage_correct'] = (1 - df['error_rate']) * 100

lpf_df = df[df['filter_type'] == 'lpf'].sort_values(by='frequency')
hpf_df = df[df['filter_type'] == 'hpf'].sort_values(by='frequency')

lpf_interp = interp1d(lpf_df['frequency'], lpf_df['percentage_correct'], kind='linear', fill_value='extrapolate')
hpf_interp = interp1d(hpf_df['frequency'], hpf_df['percentage_correct'], kind='linear', fill_value='extrapolate')
freqs = np.linspace(min(df['frequency']), max(df['frequency']), 1000)
lpf_vals = lpf_interp(freqs)
hpf_vals = hpf_interp(freqs)

diffs = np.abs(lpf_vals - hpf_vals)
crossover_idx = np.argmin(diffs)
crossover_freq = freqs[crossover_idx]
crossover_pc = (lpf_vals[crossover_idx] + hpf_vals[crossover_idx]) / 2

plt.figure(figsize=(12, 6))
plt.plot(lpf_df['frequency'], lpf_df['percentage_correct'], label='LPF (raw)', marker='o')
plt.plot(hpf_df['frequency'], hpf_df['percentage_correct'], label='HPF (raw)', marker='s')
plt.scatter([crossover_freq], [crossover_pc], color='red', zorder=5)
plt.text(crossover_freq, crossover_pc + 2, f'a = {int(crossover_freq)} Hz', color='red')

# Max SII = 1
max_score = df['percentage_correct'].max()
plt.axhline(y=max_score, color='gray', linestyle=':', label='Max Score (SII = 1)')

plt.xscale('log')
plt.xlabel('Cut-off Frequency (Hz)')
plt.ylabel('Percentage Correct')
plt.title('Cut-off Frequency vs Percentage Correct')
plt.ylim(0, 105)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()

print(f'Crossover Frequency: {crossover_freq:.2f} Hz')
print(f'Percentage Correct at Crossover: {crossover_pc:.2f}% → SII = 0.5')
print(f'Max Percentage Correct: {max_score:.2f}% → SII = 1')
