import skrf as rf

# 1. Define an 8 to 18 GHz sweep with enough points to resolve ripples
freq = rf.Frequency(8, 18, 401, 'ghz')

# 2. Left/Right Adapters: Mismatched 60-ohm lossless transmission lines
# By default, gamma is purely imaginary (lossless) if not specified
media_fixture = rf.media.DefinedGammaZ0(freq, z0=60)
adapter_l = media_fixture.line(15, 'mm', name='left_fixture_profile')
adapter_r = media_fixture.line(15, 'mm', name='right_fixture_profile')

# 3. Material Sample (DUT): 35-ohm line with explicit loss (alpha = 15 Np/m)
# We calculate gamma = alpha + j*beta, where beta = omega / c
alpha = 15.0 
beta = freq.w / 3e8  # freq.w is angular frequency (omega)
complex_gamma = alpha + 1j * beta

media_dut = rf.media.DefinedGammaZ0(freq, z0=35, gamma=complex_gamma)
dut = media_dut.line(8, 'mm', name='isolated_material_output')

# 4. Cascade the components together
total_meas = adapter_l * dut * adapter_r

# 5. Export all files to your working directory
adapter_l.write_touchstone(r'RF Labs\python_scripts\s2ps\left_fixture_profile.s2p')
adapter_r.write_touchstone(r'RF Labs\python_scripts\s2ps\right_fixture_profile.s2p')
total_meas.write_touchstone(r'RF Labs\python_scripts\s2ps\raw_measured_sample.s2p')

print("Virtual hardware data synthesized successfully!")
