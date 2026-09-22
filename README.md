# Free-Space Reference Plane Calibration via Matrix De-Embedding

## Objective & Purpose

This is an implementation of a 2-port cascading scattering transfer matrix inversion pipeline to achieve free-space de-embedding across an 8-18 GHz frequency sweep. By utilizing network matrix manipulation in scikit-rf, I am able to model how uncalibrated system reflections inject standing-wave-like interference anomalies onto an ideal, lossy Device Under Test (DUT).

Open-air RF material testing introduces physical propagation complexities. Chief among these is aperture phase error. Because a standard horn antenna emits energy as an expanding spherical wavefront, phase velocity vectors do not arrive simultaneously across a flat target sample. If the sample panel is positioned too close to the antenna apertures, this spatial phase gradient corrupts the scattering matrix measurements.

To ensure uniform plane-wave propagation assumptions remain valid, the testing geometry must be configured beyond the Rayleigh far-field boundary threshold:

$$R_{\text{ff}} \ge \frac{2D^2}{\lambda}$$

Operating at an 18 GHz ceiling with an antenna aperture dimension of D = 8 cm, a physical separation distance of at least **76.8 cm** must be rigidly maintained between the horn faces and the target frame.

The physical media creates characteristic impedance discontinuities ($Z_0 \neq 50\ \Omega$), producing secondary internal echoes. These waves form a periodic standing-wave-like interference pattern that superimposes a prominent **0.30 dB amplitude ripple** onto the transmission spectrum ($S_{21}$), masking true material resonance nulls across the **10 mm** dielectric substrate sample block.

---

## Signal Processing Pipeline

1. **Input Stage:** Establishes a wideband frequency sweep from 8 to 18 GHz over 401 points, mapping directly to standard X-band and Ku-band radar testing spectrums.
2. **Baseline Material Generation:** Models an ideal 10 mm lossy dielectric transmission line (`DUT`) within a uniform 50-Ohm characteristic impedance environment (`z0=50`), applying a precise attenuation constant of alpha = 12.0.
3. **Forward Cascade Execution:** Mathematically superimposes a cyclical, frequency-dependent phase and amplitude error directly onto the forward transmission parameters (`total_measurement`) using a 1.5 GHz ripple period to simulate physical standing-wave paths:


$$T_{\text{measured}} = T_{\text{adapter-left}} \times T_{\text{DUT}} \times T_{\text{adapter-right}}$$

4. **Validation Layer:** Converts the modified network structures back into standard Touchstone datasets and exports the raw .s2p files directly into the local repository layout.

---

## Repository Architecture

* `src/deEmbedSparams.py` - Core Python script executing the baseline creation, ripple injection loop, and data plotting.
* `plots/de_embedding_verification.png` - Extracted wideband transmission spectrum tracking curves vs. uncalibrated raw baselines.
* `requirements.txt` - Python module dependency manifest.
* `.gitignore` - Standard Git runtime file exclusion mask.

---

## CALIBRATION VERIFICATION DATA

The synthesized transmission matrix tracks absolute convergence across the entire wideband radar sweep:

![Verification Plot](plots/de_embedding_verification.png)

* **Transmission Magnitude ($S_{21}$):** Captures the simulated 0.30 dB peak-to-peak tracking error ripple cycling rhythmically across the 8-18 GHz band, overlaid with the perfectly flat, de-embedded -1.04 dB material baseline.

---

## Execution & Requirements

The codebase utilizes scikit-rf and matplotlib to handle high-dimensional vector loops.

```bash
pip install -r requirements.txt
python src/deEmbedSparams.py
```
