import numpy as np
from rtlsdr import RtlSdr
import matplotlib.pyplot as plt

# Configuration
center_freq = 7.074e6  # Center frequency in Hz
sample_rate = 2.4e6  # Sample rate in Hz
num_samples = 1024 * 1024  # Number of samples per capture
num_rotations = 12  # Number of antenna rotations
angles = np.linspace(0, 360, num_rotations)
direct_sampling_mode = 2 if center_freq < 24e6 else 0

# Initialize RTL-SDR
sdr = RtlSdr()
sdr.set_direct_sampling(direct_sampling_mode)
sdr.sample_rate = sample_rate
sdr.center_freq = center_freq
sdr.gain = 'auto'

# Initialize arrays to store results
signal_strengths = []
msg_str = f"Rotate antenna {360/num_rotations} degrees. <press enter>"

for angle in angles:
    # Rotate antenna, capture samples, calculate signal strength
    samples = sdr.read_samples(num_samples)
    signal_strength_dB = 10 * np.log10(np.mean(np.abs(samples)**2))
    signal_strengths.append(signal_strength_dB)
    input(msg_str)

# Close the RTL-SDR device
sdr.close()

# Plot the results
plt.plot(angles, signal_strengths, marker='o')
plt.title("Signal Strength vs. Antenna Angle")
plt.xlabel("Antenna Angle (degrees)")
plt.ylabel("Signal Strength (dB)")
plt.grid()
plt.show()
