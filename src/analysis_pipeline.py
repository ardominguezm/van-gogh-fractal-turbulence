"""
analysis_pipeline.py
--------------------
Global analysis script: compute MFDFA metrics for Van Gogh paintings,
compare with fBm benchmarks, and export figures/tables.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

from mfdfa2D import mfdfa2D, hurst_and_spectrum, safe_scales
from fbm_generator import generate_fbm
from plotting_tools import plot_spectra, plot_metrics_table

# Config
Q_VALS = np.linspace(-10, 10, 21)
TARGET_SIZE = 512
MIN_BOX = 10
N_BOXES = 10
DPI_FIG = 300

# Paths
FIG_DIR = "../figures"
TAB_DIR = "../tables"
DATA_DIR = "../data"
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(TAB_DIR, exist_ok=True)

PATHS = {
    "Irises (May 1889)": f"{DATA_DIR}/irises-may1889.jpg",
    "The Starry Night (June 1889)": f"{DATA_DIR}/starry-night-1889.jpg",
    "Road with Cypress and Star (May 1890)": f"{DATA_DIR}/road-cypress-star-1890.jpg",
    "Wheat Field with Crows (July 1890)": f"{DATA_DIR}/wheat-field-crows-1890.jpg",
}

def load_luminance(path):
    """Convert RGB → luminance Y (Rec.601) and normalize."""
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float64)
    Y = 0.299*rgb[...,0] + 0.587*rgb[...,1] + 0.114*rgb[...,2]
    Y = cv2.resize(Y, (TARGET_SIZE, TARGET_SIZE), interpolation=cv2.INTER_AREA)
    return (Y - Y.min()) / (Y.max() - Y.min() + 1e-12)

def compute_metrics(alpha, f_alpha, Hq, q_vals):
    """Compute H(2), Δα, ΔH, FTI, Chaos Index."""
    H2 = float(np.interp(2.0, q_vals, Hq))
    dalpha = float(np.nanmax(alpha) - np.nanmin(alpha))
    dH = float(np.nanmax(Hq) - np.nanmin(Hq))
    FTI = dalpha * (1 - H2)
    CI = dalpha * dH * (1 - H2)
    return {"H(2)": H2, "Δα": dalpha, "ΔH": dH, "FTI": FTI, "CI": CI}

def analyze_image(title, path):
    Y = load_luminance(path)
    scales = safe_scales(Y.shape, min_s=MIN_BOX, max_boxes=N_BOXES)
    Fq = mfdfa2D(Y, scales, Q_VALS)
    Hq, tau_q, alpha, f_alpha = hurst_and_spectrum(Fq, scales, Q_VALS)
    metrics = compute_metrics(alpha, f_alpha, Hq, Q_VALS)
    return {"title": title, "Hq": Hq, "alpha": alpha, "f_alpha": f_alpha, **metrics}

# Run analysis
results, spectra = [], {}
for title, path in PATHS.items():
    res = analyze_image(title, path)
    spectra[title] = res
    results.append({"Painting": title, **{k: round(v,4) for k,v in res.items() if isinstance(v,float)}})

df = pd.DataFrame(results)
df.to_csv(f"{TAB_DIR}/van_gogh_fractal_metrics.csv", index=False)
print(df)

# Plot spectra
plot_spectra(spectra, FIG_DIR, DPI_FIG)
plot_metrics_table(df, FIG_DIR)
