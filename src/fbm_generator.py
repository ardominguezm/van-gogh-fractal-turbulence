"""
fbm_generator.py
-----------------
Generate 2D fractional Brownian motion (fBm) textures
via spectral synthesis method.

Reference:
Peitgen, H.-O., Jürgens, H., & Saupe, D. (2004).
Chaos and Fractals: New Frontiers of Science.
"""

import numpy as np

def generate_fbm(size=512, H=0.5, seed=None):
    """
    Generate 2D fractional Brownian motion surface.
    Parameters
    ----------
    size : int
        Image dimension (square).
    H : float
        Hurst exponent (0 < H < 1).
    Returns
    -------
    fbm : np.ndarray
        2D fractal surface normalized to [0,1].
    """
    if seed is not None:
        np.random.seed(seed)

    N = size
    kx = np.fft.fftfreq(N).reshape(-1, 1)
    ky = np.fft.fftfreq(N).reshape(1, -1)
    k = np.sqrt(kx**2 + ky**2)
    k[0, 0] = 1.0  # avoid singularity

    # Spectral amplitude ∝ |k|^{-(H + 1)}
    amplitude = np.power(k, -(H + 1.0))
    amplitude[0, 0] = 0.0
    phase = np.random.uniform(0, 2*np.pi, (N, N))
    spectrum = amplitude * (np.cos(phase) + 1j*np.sin(phase))

    field = np.fft.ifft2(spectrum).real
    field = (field - field.min()) / (field.max() - field.min() + 1e-12)
    return field
