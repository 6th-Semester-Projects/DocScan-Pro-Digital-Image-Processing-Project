"""
Histogram Utility Functions
----------------------------
Provides histogram computation, visualization, comparison, and equalization.

DIP Concepts: Histogram analysis, contrast enhancement
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def compute_histogram(image, bins=256):
    """
    Compute the grayscale histogram of an image.

    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color). If color, it is converted to grayscale.
    bins : int
        Number of histogram bins (default 256 for full 8-bit range).

    Returns
    -------
    hist : np.ndarray
        1D array of shape (bins,) with pixel frequency counts.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    hist = cv2.calcHist([gray], [0], None, [bins], [0, 256])
    hist = hist.flatten()
    return hist


def plot_histogram(image, title="Histogram", save_path=None):
    """
    Plot the grayscale histogram of an image.

    Parameters
    ----------
    image : np.ndarray
        Input image.
    title : str
        Plot title.
    save_path : str or None
        If provided, save the figure to this path.
    """
    hist = compute_histogram(image)

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.fill_between(range(256), hist, color='steelblue', alpha=0.7)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("Pixel Intensity", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_xlim([0, 255])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  [+] Histogram saved -> {save_path}")

    plt.close(fig)
    return fig


def plot_histogram_comparison(before, after, title_before="Before Enhancement",
                               title_after="After Enhancement", save_path=None):
    """
    Plot side-by-side histogram comparison of two images.

    Parameters
    ----------
    before : np.ndarray
        Image before processing.
    after : np.ndarray
        Image after processing.
    title_before, title_after : str
        Titles for each subplot.
    save_path : str or None
        If provided, save figure.

    Returns
    -------
    fig : matplotlib.figure.Figure
    """
    hist_before = compute_histogram(before)
    hist_after = compute_histogram(after)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Before histogram
    axes[0].fill_between(range(256), hist_before, color='#e74c3c', alpha=0.7)
    axes[0].set_title(title_before, fontsize=13, fontweight='bold')
    axes[0].set_xlabel("Pixel Intensity")
    axes[0].set_ylabel("Frequency")
    axes[0].set_xlim([0, 255])
    axes[0].grid(True, alpha=0.3)

    # After histogram
    axes[1].fill_between(range(256), hist_after, color='#27ae60', alpha=0.7)
    axes[1].set_title(title_after, fontsize=13, fontweight='bold')
    axes[1].set_xlabel("Pixel Intensity")
    axes[1].set_ylabel("Frequency")
    axes[1].set_xlim([0, 255])
    axes[1].grid(True, alpha=0.3)

    plt.suptitle("Histogram Comparison", fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  [+] Histogram comparison saved -> {save_path}")

    plt.close(fig)
    return fig


def histogram_equalization(image):
    """
    Apply histogram equalization to enhance contrast.

    For grayscale images, applies directly.
    For color images, converts to YCrCb, equalizes the Y channel, and converts back.

    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or BGR color).

    Returns
    -------
    equalized : np.ndarray
        Contrast-enhanced image.
    """
    if len(image.shape) == 3:
        # Convert to YCrCb color space
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        # Equalize the Y (luminance) channel
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        equalized = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        equalized = cv2.equalizeHist(image)

    return equalized


def clahe_enhancement(image, clip_limit=2.0, tile_size=(8, 8)):
    """
    Apply CLAHE (Contrast Limited Adaptive Histogram Equalization).

    CLAHE is more sophisticated than standard histogram equalization - it operates
    on local tiles and limits contrast amplification to avoid noise enhancement.

    Parameters
    ----------
    image : np.ndarray
        Input grayscale image.
    clip_limit : float
        Threshold for contrast limiting.
    tile_size : tuple
        Size of the grid for local equalization.

    Returns
    -------
    enhanced : np.ndarray
        CLAHE-enhanced image.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    enhanced = clahe.apply(gray)
    return enhanced
