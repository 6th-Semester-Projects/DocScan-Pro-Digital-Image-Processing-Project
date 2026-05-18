"""
BinarizationEngine - Adaptive Thresholding
---------------------------------------------
Converts document images to clean binary (black & white).
Implements Otsu's global and Sauvola local adaptive binarization.

DIP Concepts: Histogram analysis, Otsu thresholding, adaptive binarization, morphology
"""

import cv2
import numpy as np
from utils.morph_utils import opening, closing


class BinarizationEngine:
    """
    Adaptive binarization engine for document images.

    Methods:
    - Otsu: Global threshold using histogram-based optimization
    - Sauvola: Local adaptive threshold for uneven lighting
    """

    def __init__(self, method='sauvola', window_size=25, k=0.2, R=128,
                 morph_kernel=3, morph_iterations=1):
        self.method = method
        self.window_size = window_size
        self.k = k
        self.R = R
        self.morph_kernel = morph_kernel
        self.morph_iterations = morph_iterations

    def compute_histogram(self, image):
        """Compute grayscale histogram (used by Otsu internally)."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
        return hist

    def otsu_threshold(self, image):
        """
        Apply Otsu's binarization.

        Otsu's method finds the optimal threshold that minimizes
        the weighted sum of intra-class variances of foreground and
        background pixels. It uses the image histogram to compute this.

        Returns: (binary_image, optimal_threshold)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()

        # Apply Gaussian blur to reduce noise before thresholding
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Otsu's thresholding
        threshold_val, binary = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        print(f"  [+] Otsu threshold: {threshold_val:.0f}")
        return binary, threshold_val

    def sauvola_threshold(self, image, window_size=None, k=None):
        """
        Apply Sauvola's local adaptive binarization.

        For each pixel, the threshold is computed from local statistics:
          T(x,y) = mean(x,y) * (1 + k * (std(x,y) / R - 1))

        where:
          mean = local mean intensity in window
          std  = local standard deviation
          k    = sensitivity parameter (typically 0.2)
          R    = dynamic range of standard deviation (128 for 8-bit)

        This handles uneven lighting much better than global methods.
        """
        w = window_size or self.window_size
        k_val = k or self.k

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
        gray = gray.astype(np.float64)

        # Compute local mean using box filter
        mean = cv2.blur(gray, (w, w))

        # Compute local standard deviation
        mean_sq = cv2.blur(gray ** 2, (w, w))
        std = np.sqrt(np.maximum(mean_sq - mean ** 2, 0))

        # Sauvola threshold formula
        threshold = mean * (1.0 + k_val * (std / self.R - 1.0))

        # Apply threshold
        binary = np.zeros_like(gray, dtype=np.uint8)
        binary[gray >= threshold] = 255

        print(f"  [+] Sauvola binarization (window={w}, k={k_val})")
        return binary.astype(np.uint8)

    def morphological_cleanup(self, binary_image):
        """
        Clean binary image using morphological opening and closing.

        - Opening (erosion->dilation): removes small noise dots
        - Closing (dilation->erosion): fills small gaps in text
        """
        print(f"  -> Morphological cleanup (kernel={self.morph_kernel})...")

        # Opening to remove small noise
        cleaned = opening(binary_image, kernel_size=self.morph_kernel)
        # Closing to fill small gaps
        cleaned = closing(cleaned, kernel_size=self.morph_kernel)

        print(f"  [+] Morphological cleanup complete")
        return cleaned

    def process(self, image, method=None):
        """
        Full binarization pipeline.

        Steps:
        1. Apply chosen binarization method (Otsu or Sauvola)
        2. Morphological cleanup (opening + closing)
        """
        binarization_method = method or self.method

        print("\n" + "=" * 50)
        print("  STAGE 3: Adaptive Binarization")
        print("=" * 50)

        # Display histogram info
        hist = self.compute_histogram(image)
        mean_intensity = np.average(range(256), weights=hist)
        print(f"\n  -> Image mean intensity: {mean_intensity:.1f}")
        print(f"  -> Using {binarization_method.upper()} method...")

        if binarization_method == 'otsu':
            binary, threshold = self.otsu_threshold(image)
        elif binarization_method == 'sauvola':
            binary = self.sauvola_threshold(image)
            threshold = None
        else:
            raise ValueError(f"Unknown method: {binarization_method}")

        # Morphological cleanup
        cleaned = self.morphological_cleanup(binary)

        debug_info = {
            'histogram': hist,
            'raw_binary': binary,
            'method': binarization_method,
            'threshold': threshold,
        }

        return cleaned, debug_info
