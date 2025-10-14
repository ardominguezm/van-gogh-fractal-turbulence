"""
src package — Fractal Turbulence in Van Gogh’s Paintings
=========================================================

Modular implementation of the multifractal analysis pipeline
for the paper:

    "Fractal Turbulence and Aesthetic Complexity in Van Gogh’s Late Paintings"
    (Domínguez-Monterroza, A. R., 2025)

This package provides:
----------------------
- mfdfa2D       → core 2D MFDFA computation
- fbm_generator → synthetic fractional Brownian motion textures
- analysis_pipeline → global metrics & spectra generation
- plotting_tools → high-level visualization utilities
- local_maps    → local multiscale Δα, ΔH, FTI, CI mapping

Each module is self-contained and designed for reproducible scientific analysis.
"""

__version__ = "1.0.0"
__author__ = "Andy R. Domínguez-Monterroza"
__email__ = "ardominguezm@gmail.com"
__license__ = "MIT"

# Core imports for convenience
from .mfdfa2D import mfdfa2D, hurst_and_spectrum, safe_scales
from .fbm_generator import generate_fbm
from .analysis_pipeline import analyze_image, compute_metrics
from .plotting_tools import plot_spectra, plot_metrics_table
from .local_maps import plot_multiscale_maps

__all__ = [
    "mfdfa2D",
    "hurst_and_spectrum",
    "safe_scales",
    "generate_fbm",
    "analyze_image",
    "compute_metrics",
    "plot_spectra",
    "plot_metrics_table",
    "plot_multiscale_maps",
]
