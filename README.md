# 🎨 Fractal Turbulence in Van Gogh’s Paintings

> *"The structure of turbulence and the structure of beauty are both born from chaos."*  

This repository contains the full analysis pipeline, figures, and data supporting the paper:  
**“Fractal Turbulence and Aesthetic Complexity in Van Gogh’s Late Paintings”**,  
prepared for submission to *Chaos* (AIP Publishing).
van-gogh-fractal-turbulence/

---

## 🧩 Overview

We apply **2D Multifractal Detrended Fluctuation Analysis (MFDFA)** to luminance maps of four late paintings by Vincent van Gogh (1889–1890).  
By quantifying **generalized Hurst exponents**, **singularity spectra**, and **turbulence-derived fractal metrics**, the study explores how **aesthetic complexity evolves in Van Gogh’s final creative period**.

A benchmark ensemble of **fractional Brownian motion (fBm, H = 0.5)** is used as a *neutral model of isotropic fractal roughness*, with 100 surrogate realizations defining a confidence band for comparison.

---

## 🧮 Methods

1. **Image preprocessing**
   - Convert RGB images to luminance (Rec. 601).
   - Resize to 512×512 px.
   - Normalize to [0, 1].

2. **Multifractal analysis**
   - 2D-MFDFA following Gu & Zhou (PRE 2010).
   - Exponents computed for `q ∈ [-10, 10]`.
   - Extracted descriptors:
     - `H(2)` – generalized Hurst exponent  
     - `Δα` – singularity spectrum width  
     - `ΔH(q)` – range of H(q)  
     - `FTI` – Fractal Turbulence Index = Δα × (1 − H(2))  
     - `CI` – Chaos Index = Δα × ΔH × (1 − H(2))

3. **Benchmark ensemble**
   - 100 synthetic fBm(H = 0.5) textures generated via spectral synthesis.
   - Mean ±1σ bands computed for H(q) and f(α) spectra.
   - Used as statistical baseline for structured multifractality.

4. **Visualization**
   - Global spectra: H(q) and f(α)
   - Evolution of fractal metrics (H(2), Δα, FTI, CI)
   - Multiscale Δα maps (Macro–Fine grids)

---

## 📊 Results Summary

| Painting | Year | H(2) | Δα | FTI | CI | Notes |
|-----------|------|------|----|-----|----|-------|
| *Irises* | 1889 | 0.14 | 0.68 | 0.58 | 0.23 | Calm period, structured flow |
| *The Starry Night* | 1889 | 0.23 | 0.96 | 0.74 | 0.52 | Turbulent aesthetic complexity |
| *Road with Cypress and Star* | 1890 | 0.15 | 0.48 | 0.41 | 0.20 | Transitional composition |
| *Wheat Field with Crows* | 1890 | 0.16 | 0.91 | 0.76 | 0.49 | Emotional turbulence, end of life |

---

## 🖥️ Running the Analysis

### 1️⃣ Installation
```bash
git clone https://github.com/andyrdm/van-gogh-fractal-turbulence.git
cd van-gogh-fractal-turbulence
pip install -r requirements.txt

---
van-gogh-fractal-turbulence/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── data/
│   ├── irises-may1889.jpg
│   ├── starry-night-1889.jpg
│   ├── road-cypress-star-1890.jpg
│   └── wheat-field-crows-1890.jpg
│
├── figures/
│   ├── Fig_Hq_all_paintings.png
│   ├── Fig_falpha_grid.png
│   ├── Fig_Hq_comparison_fbm05_surrogates.png
│   ├── Fig_falpha_comparison_fbm05_surrogates.png
│   ├── Fig_local_multiscale_delta_alpha_maps.png
│   └── Fig_evolution_metrics.png
│
├── tables/
│   ├── van_gogh_global_fractal_metrics.csv
│   └── van_gogh_global_fractal_metrics.tex
│
├── src/
│   ├── mfdfa2D.py
│   ├── fbm_generator.py
│   ├── analysis_pipeline.py
│   └── plotting_tools.py
│
└── notebooks/
    └── van_gogh_fractal_analysis.ipynb
---
