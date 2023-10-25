import rtlsdr
import numpy as np
import time
import multilateration  # Optional: For aircraft position calculations

# Parameters
center_freq = 1090e6  # Frequency for ADS-B signals (1090 MHz)
sample_rate = 2.048e6  # Sample rate (2.048 MHz)
num_samples = 2**15  # Number of samples per capture
num_captures = 100  # Number of signal captures
gain = 'auto'  # Gain control ('auto' for automatic gain)

# Initialize RTL-SDR
sdr = rtlsdr.RtlSdr()
sdr.sample_rate = sample_rate
sdr.center_freq = center_freq
sdr.gain = gain

try:
    for i in range(num_captures):
        # Read samples from RTL-SDR
        samples = sdr.read_samples(num_samples)
        
        # Process ADS-B messages
        adsb_messages = process_adsb_samples(samples)
        
        # Display ADS-B data
        for message in adsb_messages:
            print(message)
        
        # Optional: Perform multilateration for aircraft positions
        if len(adsb_messages) >= 4:
            positions = multilateration.calculate_positions(adsb_messages)
            for position in positions:
                print(f"Aircraft Position: {position}")
        
        # Sleep for a short interval between captures
        time.sleep(1)
finally:
    # Close the RTL-SDR device
    sdr.close()
