"""
mfdfa2D.py
----------------
2D Multifractal Detrended Fluctuation Analysis (MFDFA) implementation
for luminance images.

Reference:
Gu, G.-F., & Zhou, W.-X. (2010). Phys. Rev. E, 82, 011136.
"""

import numpy as np
import cv2

def safe_scales(shape, min_s=8, max_boxes=10, divisor=5):
    """
    Generate log-spaced scales adapted to image size.
    Ensures sufficient boxes per scale.
    """
    N, M = shape
    s_max = int(min(N, M) // divisor)
    s_max = max(s_max, min_s + 2)
    raw = np.logspace(np.log10(min_s), np.log10(s_max), max_boxes)
    scales = np.unique(raw.astype(int))
    return scales[scales >= min_s]


def mfdfa2D(Z, scales, q_vals):
    """
    Perform 2D Multifractal Detrended Fluctuation Analysis.
    Parameters
    ----------
    Z : np.ndarray
        Luminance image normalized to [0,1].
    scales : list[int]
        List of window sizes (pixels).
    q_vals : np.ndarray
        Range of q moments (e.g. np.linspace(-10, 10, 21)).

    Returns
    -------
    Fq : np.ndarray
        Fluctuation function F_q(s) for each q and scale.
    """
    N, M = Z.shape
    Fq = np.zeros((len(q_vals), len(scales)), dtype=np.float64)

    for si, s in enumerate(scales):
        Ns, Ms = N // s, M // s
        if Ns == 0 or Ms == 0:
            Fq[:, si] = np.nan
            continue

        x = np.arange(s, dtype=np.float64)
        y = np.arange(s, dtype=np.float64)
        X, Y = np.meshgrid(x, y, indexing='ij')
        A = np.c_[X.ravel(), Y.ravel(), np.ones(s*s, dtype=np.float64)]
        F2_list = []

        for vx in range(Ns):
            for vy in range(Ms):
                block = Z[vx*s:(vx+1)*s, vy*s:(vy+1)*s]
                b = block.ravel()
                coeff, *_ = np.linalg.lstsq(A, b, rcond=None)
                trend = (coeff[0]*X + coeff[1]*Y + coeff[2])
                detrended = block - trend
                var = np.mean(detrended**2)
                F2_list.append(max(var, 1e-12))

        F2 = np.array(F2_list, dtype=np.float64)
        for qi, q in enumerate(q_vals):
            if np.isclose(q, 0.0):
                Fq[qi, si] = np.exp(0.5 * np.mean(np.log(F2)))
            else:
                Fq[qi, si] = (np.mean(F2**(q/2.0)))**(1.0/q)
    return Fq


def hurst_and_spectrum(Fq, scales, q_vals, emb_dim=2):
    """
    Estimate H(q), τ(q), α, f(α) from Fq(s).
    Weighted linear regression in log2-log2 space.
    """
    log_s = np.log2(scales.astype(np.float64))
    Hq = []

    for i in range(len(q_vals)):
        valid = np.isfinite(Fq[i, :]) & (Fq[i, :] > 0)
        if np.sum(valid) < 3:
            Hq.append(np.nan)
            continue
        x = log_s[valid]
        y = np.log2(Fq[i, valid])
        w = np.linspace(1.0, 2.0, len(x))
        coeff = np.polyfit(x - np.mean(x), y, 1, w=w)
        Hq.append(coeff[0])

    Hq = np.array(Hq)
    tau_q = q_vals * Hq - emb_dim
    alpha = np.gradient(tau_q, q_vals)
    f_alpha = q_vals * alpha - tau_q
    return Hq, tau_q, alpha, f_alpha
