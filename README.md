# Free-Space Reference Plane Calibration & Matrix De-Embedding Engine

This repository houses an automated Python processing engine designed to shift VNA calibration reference planes away from antenna apertures and lock them directly onto a target material's surface face. By utilizing cascading Scattering Transfer parameters (\(T\)-matrices) derived from 2-port complex scattering metrics (\(S_{11}, S_{21}\)), the engine programmatically divides out systematic fixture reflections and phase velocity sags.

---

## Objective & Purpose
When conducting open-air RF material testing, moving beyond perfect coaxial cables introduces immediate physical propagation complexities. Chief among these is aperture phase error; because a standard horn antenna launches energy as an expanding spherical wavefront, phase velocity vectors do not arrive simultaneously across a flat target sample. If the sample panel is positioned too close to the antenna apertures, this spatial phase gradient corrupts the scattering matrix measurements.

To ensure uniform plane-wave propagation assumptions remain valid, the testing geometry must be configured beyond the Rayleigh far-field boundary:

\[R_{ff} \ge \frac{2D^2}{\lambda}\]

Operating at an 18 GHz ceiling with an antenna aperture dimension of \(D = 8\text{ cm}\), a physical separation distance of at least **76.8 cm** must be rigidly maintained between the horn faces and the target frame. 

Furthermore, the intervening physical media constraints (air gaps, specimen holders, and structural adapters) create characteristic impedance discontinuities (\(Z_0 \neq 50\ \Omega\)), giving rise to secondary internal echoes. These waves form a periodic standing-wave interference pattern that superimposes a prominent **0.30 dB amplitude ripple** onto the transmission spectrum (\(S_{21}\)), masking true material resonance nulls. 

---

## Signal Processing Pipeline

The engine converts standard, non-cascadable Scattering matrices (\(S\)-parameters) into linear, non-commutative Scattering Transfer matrices (\(T\)-parameters) to execute fixture isolation through the following analytical architecture:

1. **Input Stage:** Ingests raw, uncalibrated complex \(S\)-parameter datasets spanning the 8–18 GHz band.
2. **Matrix Transformation Core:** 
   * Maps standard 2-port \(S\)-matrices to forward-cascading \(T\)-matrices.
   * Pulls the hard-coded calibration fixture boundaries (\(T_{adapter\_left}\) and \(T_{adapter\_right}\)).
3. **De-Embedding Execution:** Computes the true, unshielded parameters of the Device Under Test (\(T_{DUT}\)) by applying network inversion matrix multiplication:
   \[T_{DUT} = T_{adapter\_left}^{-1} \times T_{measured} \times T_{adapter\_right}^{-1}\]
4. **Validation Layer:** Automatically maps the clean \(T_{DUT}\) matrix back into standard S-parameters, completely stripping away the cyclical 0.30 dB amplitude ripple and outputting the true insertion loss profile of the substrate.

---

## Repository Architecture

* `deEmbedEngine.py` - Core object-oriented Python pipeline executing the \(T\)-matrix cascading inversions.
* `plots/fixture_verification_plot.png` - Extracted, ripple-free transmission spectrum curves vs. uncalibrated raw baselines.
* `requirements.txt` - Python module dependency manifest (`scikit-rf`, `numpy`, `matplotlib`).
* `.gitignore` - Standard Git runtime file exclusion mask.

---

## Core Competencies Demonstrated
* **Microwave Physics:** S-parameter translation, complex matrix inversion loops, and free-space wave propagation geometry.
* **Instrumentation Foundations:** Programmatic data normalization workflows replicating high-end hardware vector calibration runs.
* **Signal Integrity:** Advanced filtering of standing-wave reflection anomalies without introducing digital phase distortions.
