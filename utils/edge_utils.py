"""
Edge Detection Utility Functions
---------------------------------
Provides Canny, Sobel, and Laplacian edge detection methods.

DIP Concepts: Edge detection (spatial domain)
"""

import cv2
import numpy as np


def canny_edges(image, low_threshold=50, high_threshold=150):
    """
    Apply Canny edge detection.

    The Canny detector uses a multi-stage algorithm:
    1. Gaussian smoothing to reduce noise
    2. Gradient computation (Sobel) for edge magnitude and direction
    3. Non-maximum suppression to thin edges
    4. Hysteresis thresholding with low and high thresholds

    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color).
    low_threshold : int
        Lower threshold for hysteresis.
    high_threshold : int
        Upper threshold for hysteresis.

    Returns
    -------
    edges : np.ndarray
        Binary edge map (0 or 255).
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Apply Gaussian blur first to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)

    # Canny edge detection
    edges = cv2.Canny(blurred, low_threshold, high_threshold)

    return edges


def sobel_edges(image, ksize=3, combined=True):
    """
    Apply Sobel edge detection.

    Sobel computes the gradient of image intensity in both x and y directions.
    The combined magnitude gives the overall edge strength.

    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color).
    ksize : int
        Kernel size for Sobel operator (must be 1, 3, 5, or 7).
    combined : bool
        If True, return combined magnitude of x and y gradients.
        If False, return tuple (sobel_x, sobel_y).

    Returns
    -------
    edges : np.ndarray or tuple
        Edge magnitude map, or (sobel_x, sobel_y) if combined=False.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Compute gradients in x and y directions
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

    if combined:
        # Compute gradient magnitude
        magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
        # Normalize to 0-255 range
        magnitude = np.uint8(np.clip(magnitude / magnitude.max() * 255, 0, 255))
        return magnitude
    else:
        sobel_x = np.uint8(np.clip(np.abs(sobel_x) / np.abs(sobel_x).max() * 255, 0, 255))
        sobel_y = np.uint8(np.clip(np.abs(sobel_y) / np.abs(sobel_y).max() * 255, 0, 255))
        return sobel_x, sobel_y


def laplacian_edges(image, ksize=3):
    """
    Apply Laplacian edge detection.

    The Laplacian is a second-order derivative operator that detects edges
    by finding zero-crossings. It is isotropic (rotation-invariant).

    Parameters
    ----------
    image : np.ndarray
        Input image (grayscale or color).
    ksize : int
        Aperture size for the Laplacian operator.

    Returns
    -------
    edges : np.ndarray
        Edge map (absolute values normalized to 0-255).
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Apply Gaussian blur to reduce noise sensitivity
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Laplacian edge detection
    laplacian = cv2.Laplacian(blurred, cv2.CV_64F, ksize=ksize)

    # Take absolute values and normalize
    edges = np.uint8(np.clip(np.abs(laplacian) / np.abs(laplacian).max() * 255, 0, 255))

    return edges
