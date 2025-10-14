"""
local_maps.py
-----------------
Compute and visualize local multifractal features (Δα, ΔH, FTI, CI)
across multiple spatial scales for luminance images.

Author: Andy R. Domínguez-Monterroza
Date: 2025
Reference: Gu & Zhou (Phys. Rev. E 82, 011136, 2010)
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

from mfdfa2D import mfdfa2D, hurst_and_spectrum, safe_scales

# ----------------------------------------------------
# 1. Patch-based local feature computation
# ----------------------------------------------------

def make_patches(img, n_patches):
    """
    Split an image into n_patches × n_patches tiles.
    Returns list of patches and patch dimensions.
    """
    h, w = img.shape
    step_y, step_x = h // n_patches, w // n_patches
    patches = [
        img[i*step_y:(i+1)*step_y, j*step_x:(j+1)*step_x]
        for i in range(n_patches)
        for j in range(n_patches)
    ]
    return patches, step_y, step_x


def compute_local_features(img, q_vals, min_s=8, max_boxes=9, divisor=3):
    """
    Compute local Δα, ΔH, FTI, and CI for each patch of the image.
    Returns 4 maps (each n_patches × n_patches).
    """
    def local_metrics(Hq, alpha, H2):
        """Compute Δα, ΔH, FTI, CI for one patch."""
        if np.isnan(Hq).any() or np.isnan(alpha).any():
            return np.nan, np.nan, np.nan, np.nan
        dalpha = np.max(alpha) - np.min(alpha)
        dH = np.max(Hq) - np.min(Hq)
        FTI = dalpha * (1 - H2)
        CI = dalpha * dH * (1 - H2)
        return dalpha, dH, FTI, CI

    scales = safe_scales(img.shape, min_s=min_s, max_boxes=max_boxes, divisor=divisor)
    return local_metrics, scales


def patchwise_local_maps(img, n_patches, q_vals):
    """
    Compute Δα, ΔH, FTI, CI maps for an image divided in n_patches² tiles.
    """
    patches, step_y, step_x = make_patches(img, n_patches)
    local_metrics, scales = compute_local_features(img, q_vals)
    
    dalpha_vals, dH_vals, fti_vals, ci_vals = [], [], [], []

    for patch in patches:
        Fq = mfdfa2D(patch, scales, q_vals)
        Hq, tau_q, alpha, f_alpha = hurst_and_spectrum(Fq, scales, q_vals)
        H2 = float(np.interp(2.0, q_vals, Hq))
        da, dh, fti, ci = local_metrics(Hq, alpha, H2)
        dalpha_vals.append(da)
        dH_vals.append(dh)
        fti_vals.append(fti)
        ci_vals.append(ci)

    def reshape(v): return np.array(v).reshape(n_patches, n_patches)
    return reshape(dalpha_vals), reshape(dH_vals), reshape(fti_vals), reshape(ci_vals)

# ----------------------------------------------------
# 2. Visualization
# ----------------------------------------------------

def plot_multiscale_maps(img, q_vals, fig_dir, levels=None, dpi=200):
    """
    Plot multiscale maps (Δα, ΔH, FTI, CI) for defined grid levels.
    """
    if levels is None:
        levels = {"Macro 4×4": 4, "Meso 6×6": 6, "Micro 8×8": 8, "Fine 10×10": 10}

    gray_bg = cv2.resize(img, (512, 512), interpolation=cv2.INTER_AREA)
    features = ["Δα (width)", "ΔH (range)", "FTI", "CI"]
    cmap = "jet"

    for feat_idx, feat_name in enumerate(features):
        fig, axs = plt.subplots(len(levels), 1, figsize=(6, 10), dpi=dpi)
        plt.subplots_adjust(hspace=0.15)
        
        for (scale_name, npatch), ax in zip(levels.items(), axs):
            dalpha_map, dH_map, fti_map, ci_map = patchwise_local_maps(img, npatch, q_vals)
            maps = [dalpha_map, dH_map, fti_map, ci_map]
            data_map = maps[feat_idx]
            res_map = cv2.resize(data_map, (gray_bg.shape[1], gray_bg.shape[0]), interpolation=cv2.INTER_CUBIC)

            ax.imshow(gray_bg, cmap="gray", alpha=0.85)
            im = ax.imshow(res_map, cmap=cmap, alpha=0.75)
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_title(f"{scale_name}", fontsize=9)

        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        fig.colorbar(im, cax=cbar_ax, label=feat_name)
        fig.suptitle(f"{feat_name} Multiscale Maps", fontsize=12)
        plt.tight_layout(rect=[0,0,0.9,0.95])
        path = os.path.join(fig_dir, f"LocalMap_{feat_name.replace(' ','_')}.png")
        plt.savefig(path, dpi=dpi, bbox_inches="tight")
        plt.close()
        print("Saved:", path)

# from local_maps import plot_multiscale_maps
# from analysis_pipeline import load_luminance, Q_VALS, FIG_DIR

# # Example for The Starry Night
# img = load_luminance("../data/starry-night-1889.jpg")
# plot_multiscale_maps(img, Q_VALS, fig_dir=FIG_DIR)
