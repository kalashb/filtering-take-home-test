import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# coefficients
b = [0.99901921, -1.99790074, 0.99901921] 
a = [1.0, -1.99790074, 0.99803843] 

# frequency response
w, h = signal.freqz(b, a, fs=32000)  

# group delay
w_gd, gd = signal.group_delay((b, a), w=w, fs=32000)

# Find passband (where magnitude is close to 0 dB)
magnitude_db = 20 * np.log10(np.abs(h))
passband_mask = magnitude_db > -3  # Define passband as frequencies with less than 3dB attenuation
passband_gd = gd[passband_mask]
passband_freq = w_gd[passband_mask]
plt.figure(figsize=(12, 10))

# plot magnitude response
plt.subplot(3, 1, 1)
plt.plot(w, 20 * np.log10(np.abs(h)))
plt.grid(True)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude [dB]')
plt.title('Filter Magnitude Response')
# add -3dB line (red dashed line) because it's the passband
plt.axhline(y=-3, color='r', linestyle='--', label='-3dB')
plt.legend()

# plot phase response
plt.subplot(3, 1, 2)
plt.plot(w, np.unwrap(np.angle(h)) * 180 / np.pi)
plt.grid(True)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [degrees]')
plt.title('Filter Phase Response')

# plot group delay
plt.subplot(3, 1, 3)
plt.plot(w_gd, gd, 'b-', label='All frequencies')
plt.plot(passband_freq, passband_gd, 'r-', linewidth=2, label='Passband only')
plt.grid(True)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Group Delay [samples]')
plt.title('Filter Group Delay')
plt.legend()

plt.tight_layout()
plt.savefig('filter_response.png', dpi=300, bbox_inches='tight')
plt.close()

# Print some statistics
print("\nFilter Response Statistics:")
print("-" * 30)
print(f"Average group delay: {np.mean(gd):.2f} samples")
print(f"Maximum group delay: {np.max(gd):.2f} samples")
print(f"Minimum group delay: {np.min(gd):.2f} samples")

# Convert to time
sampling_period = 1/32000  # seconds
print(f"\nTime Delays (All Frequencies):")
print("-" * 30)
print(f"Average group delay: {np.mean(gd) * sampling_period * 1e6:.2f} microseconds")
print(f"Maximum group delay: {np.max(gd) * sampling_period * 1e6:.2f} microseconds")
print(f"Minimum group delay: {np.min(gd) * sampling_period * 1e6:.2f} microseconds")

# Passband statistics
print(f"\nTime Delays (Passband Only):")
print("-" * 30)
print(f"Average passband delay: {np.mean(passband_gd) * sampling_period * 1e6:.2f} microseconds")
print(f"Maximum passband delay: {np.max(passband_gd) * sampling_period * 1e6:.2f} microseconds")
print(f"Minimum passband delay: {np.min(passband_gd) * sampling_period * 1e6:.2f} microseconds")

# Calculate -3dB bandwidth
minus_3db_idx = np.where(magnitude_db <= -3)[0]
if len(minus_3db_idx) >= 2:
    bandwidth = w[minus_3db_idx[-1]] - w[minus_3db_idx[0]]
    print(f"\nFilter Bandwidth:")
    print("-" * 30)
    print(f"-3dB Bandwidth: {bandwidth:.2f} Hz")
    print(f"Lower -3dB point: {w[minus_3db_idx[0]]:.2f} Hz")
    print(f"Upper -3dB point: {w[minus_3db_idx[-1]]:.2f} Hz") 