# %%
import skrf as rf
import os
import matplotlib.pyplot as plt

# Finds the absolute path to the directory containing this script ('python_scripts')
base_dir = os.path.dirname(os.path.abspath(__file__))

# Resolves directly to your target s2ps folder files
total_measurement = rf.Network(os.path.join(base_dir, 's2ps', 'raw_measured_sample.s2p'))
adapter_left = rf.Network(os.path.join(base_dir, 's2ps', 'left_fixture_profile.s2p'))
adapter_right = rf.Network(os.path.join(base_dir, 's2ps', 'right_fixture_profile.s2p'))


# Execute matrix de-embedding to strip away the virtual adapters
isolated_material = adapter_left.inv * total_measurement * adapter_right.inv

# Verify the math worked by plotting the isolated result
isolated_material.plot_s_db()


print("Saving de-embedded material parameter file...")
isolated_material.write_touchstone('isolated_material_output.s2p')

# Plot the comparison to verify the calibration math worked
plt.figure(figsize=(10, 5))
total_measurement.plot_s_db(m=1, n=0, label='Raw Measurement ($S_{21}$)')
isolated_material.plot_s_db(m=1, n=0, label='De-embedded Material ($S_{21}$)')
plt.title('Week 3 Virtual Calibration Lab: Fixture De-Embedding Verification')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)
plt.legend()
plt.savefig('de_embedding_verification.png', dpi=300)
plt.show()

print("Reference plane shift successfully locked onto sample face.")