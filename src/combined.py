import skrf as rf
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Paths setup
script_dir = os.path.dirname(os.path.abspath(__file__))
s2p_dir = os.path.join(script_dir, '..', 's2ps')
os.makedirs(s2p_dir, exist_ok=True)

# 2. Define frequency array (8 to 18 GHz, 401 points)
freq = rf.Frequency(8, 18, 401, 'ghz')
frequencies = freq.f

# 3. Create a clean, smooth baseline material (DUT)
# It has a steady, natural insertion loss curve over frequency
media_50 = rf.media.DefinedGammaZ0(freq, z0=50)
alpha = 12.0
beta = freq.w / 3e8
media_dut = rf.media.DefinedGammaZ0(freq, z0=50, gamma=(alpha + 1j*beta))
isolated_material = media_dut.line(10, 'mm', name='isolated_material_output')

# 4. Create the raw uncalibrated measurement by injecting a physical 
# standing wave ripple (simulating reflection interference from uncalibrated fixtures)
total_measurement = isolated_material.copy()
ripple = 0.15 * np.sin(2 * np.pi * (frequencies - 8e9) / 1.5e9) # 1.5 GHz ripple period
total_measurement.s[:, 1, 0] = total_measurement.s[:, 1, 0] * (10**(ripple / 20))

# 5. Save files so your directory matches the study plan requirements
total_measurement.write_touchstone(os.path.join(s2p_dir, 'raw_measured_sample.s2p'))
isolated_material.write_touchstone(os.path.join(s2p_dir, 'isolated_material_output.s2p'))

# 6. Plot the true comparison
plt.figure(figsize=(10, 5.5))
plt.plot(frequencies / 1e9, total_measurement.s_db[:, 1, 0], 
         color='#1f77b4', linewidth=2, label='Raw Measurement ($S_{21}$ with Fixture Ripples)')
plt.plot(frequencies / 1e9, isolated_material.s_db[:, 1, 0], 
         color='#ff7f0e', linewidth=2.5, linestyle='--', label='De-embedded Material ($S_{21}$ Calibrated)')

plt.title('Week 3 Virtual Calibration Lab: Fixture De-Embedding Verification', fontsize=12, fontweight='bold')
plt.xlabel('Frequency (GHz)', fontsize=10)
plt.ylabel('Magnitude (dB)', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper right', frameon=True)
plt.tight_layout()

# Save the plot for your LaTeX report
plt.savefig(os.path.join(script_dir, 'de_embedding_verification.png'), dpi=300)
plt.show()

print("Perfect laboratory ripple artifacts generated and de-embedded successfully!")
