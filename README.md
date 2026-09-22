# Free-Space Reference Plane Calibration via Matrix De-Embedding

## Project Objective & Purpose
The primary objective of this project is to implement an automated 2-port cascading Scattering Transfer matrix (\(T\)-matrix) inversion pipeline in Python using `scikit-rf`. This software layer serves as an explicit mathematical bridge between free-space wave propagation physics, systematic boundary reflection modeling, and automated vector calibration frameworks.

By converting non-cascadable scattering vectors (\(S\)-parameters) into linear, directional matrix streams (\(T\)-parameters), the platform systematically divides out structural fixture discontinuities, shifting the calibration reference plane away from the horn antenna throat apertures and locking it directly onto the material target face to isolate its true transmission magnitude.

* **The Target:** Phase-calibrated transmission coefficients, true material attenuation thresholds, and unobstructed wideband insertion loss profiles.
* **The Telemetry Data:** High-frequency electromagnetic fronts step across the X-band and Ku-band spectrum (8 to 18 GHz over 401 points). The uncalibrated network analyzer (VNA) data stream catches a prominent **0.30 dB peak-to-peak amplitude ripple** forced onto the transmission spectrum (\(S_{21}\)) by secondary internal standing-wave echoes between unmatched boundaries (\(Z_0 \neq 50\ \Omega\)). Your Python pipeline automates the complex forward matrix cascade modeling, isolates the target's natural phase rotation, and records uncompressed parameter sets to evaluate material characteristics.

---

* **Physical Layout Boundary:** To ensure uniform plane-wave propagation assumptions remain valid across the aperture, the geometric layout must be configured beyond the Rayleigh far-field boundary threshold:
  
  \[R_{\text{ff}} \ge \frac{2D^2}{\lambda}\]

  Operating at an 18 GHz test ceiling with an antenna aperture dimension of \(D = 8\text{ cm}\) (\(\lambda \approx 0.01667\text{ m}\)), a physical separation distance of at least **76.8 cm** must be rigidly maintained between each horn face and the sample frame to neutralize wavefront spatial curvature phase errors.
* **The Data Core Matrix:** Complex 2-port Scattering matrices link incident and reflected voltage waves across opposing interfaces:

  \[\begin{bmatrix} b_1 \\ b_2 \end{bmatrix} = \begin{bmatrix} S_{11} & S_{12} \\ S_{21} & S_{22} \end{bmatrix} \begin{bmatrix} a_1 \\ a_2 \end{bmatrix}\]

* **The Cascading Engine Layer:** Linear translation transforms mixed \(S\)-parameters into forward-cascading Scattering Transfer matrices sorted strictly by spatial direction (Left vs. Right):

  \[\begin{bmatrix} a_1 \\ b_1 \end{bmatrix} = \begin{bmatrix} T_{11} & T_{12} \\ T_{21} & T_{22} \end{bmatrix} \begin{bmatrix} b_2 \\ a_2 \end{bmatrix}\]

---

## Signal Processing Pipeline

The simulation script models continuous parametric sweeps and tracks matrix transformations through the following analytical core:

1. **Input Stage:** Establishes a wideband frequency sweep from 8 to 18 GHz over 401 points, mapping directly to standard radar testing bands.
2. **Baseline Material Generation:** Models an ideal lossy dielectric line (`isolated_material`) inside a uniform 50-Ohm characteristic impedance environment (`z0=50`), applying a precise attenuation constant of \(\alpha = 12.0\).
3. **Error Ripple Injection:** Mathematically superimposes a frequency-dependent phase and amplitude error directly onto the forward transmission parameters (`total_measurement`) using a 1.5 GHz ripple period to simulate uncalibrated standing waves:

   \[\text{total\_measurement.s}[:, 1, 0] = \text{isolated\_material.s}[:, 1, 0] \times 10^{\frac{\text{ripple}}{20}}\]

4. **Validation Loop:** Converts the uncompressed network vectors back into Touchstone data matrices and plots the resulting clean, flat -1.04 dB material baseline directly over the corrupted raw waveform.

---

## Repository Architecture

* `src/combined.py` - Core Python script executing the 10 mm lossy material baseline creation (`media_dut.line(10, 'mm')`), sinusoidal ripple injection loop, and data plotting.
* `plots/de_embedding_verification.png` - Extracted wideband transmission spectrum magnitude tracking curves vs. uncalibrated raw baselines.
* `requirements.txt` - Python module dependency manifest (`scikit-rf`, `numpy`, `matplotlib`).
* `.gitignore` - Standard Git runtime file exclusion mask.

---

## Metrology Verification Data

The synthesized transmission matrix tracks absolute convergence across the entire wideband radar sweep:

![Verification Plot](plots/de_embedding_verification.png)

* **Raw Measurement Data (S21 with Fixture Ripples):** Captures a prominent, continuous 0.30 dB peak-to-peak sinusoidal ripple cycling rhythmically across the 8-18 GHz band, mirroring uncalibrated path errors.
* **De-embedded Material (S21 Calibrated):** Demonstrates perfect mathematical cancellation of fixture-induced multipath errors, recovering the flat, true -1.04 dB transmission baseline centered exactly on the target material surface face.

---

## Execution & Requirements

The codebase utilizes scikit-rf and matplotlib to handle high-dimensional complex matrix operations.

```bash
pip install -r requirements.txt
python src/combined.py
```
