"""
plotting_tools.py
-----------------
Helper plotting functions for MFDFA results.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def plot_spectra(spectra, fig_dir, dpi=300):
    """Plot H(q) and f(α) spectra."""
    # H(q)
    plt.figure(figsize=(6,4), dpi=dpi)
    for title, res in spectra.items():
        plt.plot(res["Hq"], lw=2, label=title)
    plt.xlabel("q index")
    plt.ylabel("H(q)")
    plt.title("Generalized Hurst Exponents")
    plt.grid(ls=":")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "Hq_all_paintings.png"), dpi=dpi)
    plt.close()

    # f(α)
    plt.figure(figsize=(6,4), dpi=dpi)
    for title, res in spectra.items():
        plt.plot(res["alpha"], res["f_alpha"], lw=2, label=title)
    plt.xlabel(r"$\alpha$")
    plt.ylabel(r"$f(\alpha)$")
    plt.title("Singularity Spectra — Van Gogh")
    plt.grid(ls=":")
    plt.legend(fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "falpha_all_paintings.png"), dpi=dpi)
    plt.close()

def plot_metrics_table(df, fig_dir):
    """Visualize Δα, ΔH, FTI, and CI evolution."""
    metrics = ["Δα", "ΔH", "FTI", "CI"]
    fig, axes = plt.subplots(len(metrics), 1, figsize=(8,10))
    x = np.arange(len(df))
    for i, m in enumerate(metrics):
        axes[i].plot(x, df[m], "o-", lw=2)
        axes[i].set_ylabel(m)
        axes[i].set_xticks(x)
        axes[i].set_xticklabels(df["Painting"], rotation=20, ha="right")
        axes[i].grid(ls=":")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "metric_evolution.png"), dpi=300)
    plt.close()
