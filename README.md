# Free-Space Reference Plane Calibration & Matrix De-Embedding Engine

## Objective & Purpose

This repository houses an automated Python processing pipeline designed to shift VNA calibration reference planes away from antenna apertures and lock them directly onto a target material's surface face. By utilizing cascading Scattering Transfer parameters (T-matrices) derived from 2-port complex scattering metrics (S11, S21), the engine programmatically divides out systematic fixture reflections and phase velocity sags.

When conducting open-air RF material testing, moving beyond perfect coaxial cables introduces immediate physical propagation complexities. Chief among these is aperture phase error; because a standard horn antenna launches energy as an expanding spherical wavefront, phase velocity vectors do not arrive simultaneously across a flat target sample. If the sample panel is positioned too close to the antenna apertures, this spatial phase gradient corrupts the scattering matrix measurements.

To ensure uniform plane-wave propagation assumptions remain valid, the testing geometry must be configured beyond the Rayleigh far-field boundary threshold:

$$R_{ff} \ge \frac{2D^2}{\lambda}$$

Operating at an 18 GHz ceiling with an antenna aperture dimension of D = 8 cm, a physical separation distance of at least **76.8 cm** must be rigidly maintained between the horn faces and the target frame.

Furthermore, the intervening physical media constraints (air gaps, specimen holders, and structural adapters) create characteristic impedance discontinuities ( $Z_0 \neq 50\ \Omega$ ), giving rise to secondary internal echoes. These waves form a periodic standing-wave interference pattern that superimposes a prominent **0.30 dB amplitude ripple** onto the transmission spectrum (S21), masking true material resonance nulls.

---

## Signal Processing Pipeline

Processes complex scattering network matrices through the following analytical architecture:

1. **Input Stage:** Ingests raw, uncalibrated complex S-parameter datasets spanning the 8-18 GHz band.
2. **Matrix Transformation Core:**
   * Maps standard 2-port S-matrices to forward-cascading T-matrices.
   * Pulls the hard-coded calibration fixture boundaries (`T_adapter-left` and `T_adapter-right`).
3. **De-Embedding Execution:** Computes the true, unshielded parameters of the Device Under Test (`T_DUT`) by applying network inversion matrix multiplication:

$$T_{\text{DUT}} = T_{\text{adapter\ left}}^{-1} \times T_{\text{measured}} \times T_{\text{adapter\ right}}^{-1}$$

4. **Validation Layer:** Automatically maps the clean `T_DUT` matrix back into standard S-parameters, completely stripping away the cyclical 0.30 dB amplitude ripple and outputting the true insertion loss profile of the substrate.

---

## Repository Architecture

* `deEmbedSparams.py` - Core Python processing script implementing the inversion.
* `plots/verification_plot.png` - Extracted material parameters vs. target specification baselines.
* `requirements.txt` - Python module dependency manifest.
* `.gitignore` - Standard Git runtime file exclusion mask.

---

## CALIBRATION VERIFICATION DATA

The inverted scattering matrix tracks absolute convergence across the entire wideband radar sweep:

![Fixture Verification Plot](plots/de_embedding_verification.png)

* **Top Panel (Transmission Magnitude S21):** Captures stable transmission tracking locked onto the baseline matrix, proving zero phase ambiguity divergence.
* **Bottom Panel (Phase Extraction):** Verifies tightly constrained material phase alignment tracking centered cleanly on the target specification window.

---

## Execution & Requirements

The codebase utilizes numpy and matplotlib to handle high-dimensional vector loops.

