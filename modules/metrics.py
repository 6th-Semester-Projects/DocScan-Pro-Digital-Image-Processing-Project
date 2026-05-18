"""
Quality Metrics Calculator
----------------------------
Computes PSNR, MSE, and SSIM for quantitative evaluation of image processing.

DIP Concepts: Quantitative evaluation metrics
"""

import cv2
import numpy as np


def _ensure_grayscale(image):
    """Convert to grayscale if needed."""
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image.copy()


def _ensure_same_size(img1, img2):
    """Resize img2 to match img1's dimensions if they differ."""
    if img1.shape[:2] != img2.shape[:2]:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]),
                          interpolation=cv2.INTER_AREA)
    return img2


class MetricsCalculator:
    """
    Compute quality metrics between two images.

    Metrics:
    - MSE (Mean Squared Error): Average of squared pixel differences.
      Lower is better. MSE = 0 means identical images.

    - PSNR (Peak Signal-to-Noise Ratio): Ratio of peak signal power to noise.
      Higher is better. Measured in decibels (dB).
      PSNR = 10 * log10(MAX^2 / MSE)

    - SSIM (Structural Similarity Index): Measures structural similarity
      considering luminance, contrast, and structure.
      Range: [-1, 1], where 1 = identical images.
    """

    @staticmethod
    def compute_mse(original, processed):
        """
        Compute Mean Squared Error between two images.

        Parameters
        ----------
        original : np.ndarray
            Reference image.
        processed : np.ndarray
            Processed/output image.

        Returns
        -------
        float
            MSE value. Lower is better.
        """
        img1 = _ensure_grayscale(original).astype(np.float64)
        img2 = _ensure_grayscale(processed).astype(np.float64)
        img2 = _ensure_same_size(img1, img2)

        mse = np.mean((img1 - img2) ** 2)
        return float(mse)

    @staticmethod
    def compute_psnr(original, processed, max_pixel=255.0):
        """
        Compute Peak Signal-to-Noise Ratio between two images.

        Parameters
        ----------
        original : np.ndarray
            Reference image.
        processed : np.ndarray
            Processed/output image.
        max_pixel : float
            Maximum pixel value (255 for 8-bit images).

        Returns
        -------
        float
            PSNR value in dB. Higher is better.
            Returns float('inf') if images are identical (MSE = 0).
        """
        mse = MetricsCalculator.compute_mse(original, processed)

        if mse == 0:
            return float('inf')

        psnr = 10.0 * np.log10((max_pixel ** 2) / mse)
        return float(psnr)

    @staticmethod
    def compute_ssim(original, processed):
        """
        Compute Structural Similarity Index (SSIM) between two images.

        Uses the Wang et al. (2004) formula with default constants:
          C1 = (K1 * L)^2, C2 = (K2 * L)^2
          where K1=0.01, K2=0.03, L=255

        Parameters
        ----------
        original : np.ndarray
            Reference image.
        processed : np.ndarray
            Processed/output image.

        Returns
        -------
        float
            SSIM value in range [-1, 1]. Higher is better.
        """
        try:
            from skimage.metrics import structural_similarity as ssim
            img1 = _ensure_grayscale(original)
            img2 = _ensure_grayscale(processed)
            img2 = _ensure_same_size(img1, img2)
            score = ssim(img1, img2)
            return float(score)
        except ImportError:
            # Fallback: manual SSIM computation
            return MetricsCalculator._manual_ssim(original, processed)

    @staticmethod
    def _manual_ssim(original, processed, C1=6.5025, C2=58.5225):
        """
        Manual SSIM computation (fallback if scikit-image not available).

        Parameters
        ----------
        C1, C2 : float
            Stabilization constants. Default values use K1=0.01, K2=0.03, L=255.
        """
        img1 = _ensure_grayscale(original).astype(np.float64)
        img2 = _ensure_grayscale(processed).astype(np.float64)
        img2 = _ensure_same_size(img1, img2)

        # Compute means
        mu1 = cv2.GaussianBlur(img1, (11, 11), 1.5)
        mu2 = cv2.GaussianBlur(img2, (11, 11), 1.5)

        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2

        # Compute variances and covariance
        sigma1_sq = cv2.GaussianBlur(img1 ** 2, (11, 11), 1.5) - mu1_sq
        sigma2_sq = cv2.GaussianBlur(img2 ** 2, (11, 11), 1.5) - mu2_sq
        sigma12 = cv2.GaussianBlur(img1 * img2, (11, 11), 1.5) - mu1_mu2

        # SSIM formula
        numerator = (2 * mu1_mu2 + C1) * (2 * sigma12 + C2)
        denominator = (mu1_sq + mu2_sq + C1) * (sigma1_sq + sigma2_sq + C2)

        ssim_map = numerator / denominator
        return float(np.mean(ssim_map))

    @staticmethod
    def compute_all(original, processed):
        """
        Compute all quality metrics at once.

        Parameters
        ----------
        original : np.ndarray
            Reference image.
        processed : np.ndarray
            Processed/output image.

        Returns
        -------
        dict
            Dictionary with keys 'MSE', 'PSNR', 'SSIM' and their values.
        """
        metrics = {
            'MSE': MetricsCalculator.compute_mse(original, processed),
            'PSNR': MetricsCalculator.compute_psnr(original, processed),
            'SSIM': MetricsCalculator.compute_ssim(original, processed),
        }
        return metrics

    @staticmethod
    def format_report(metrics, title="Quality Metrics"):
        """
        Format metrics as a readable string report.

        Parameters
        ----------
        metrics : dict
            Dictionary from compute_all().
        title : str
            Report section title.

        Returns
        -------
        str
            Formatted report string.
        """
        lines = [
            f"{'=' * 50}",
            f"  {title}",
            f"{'=' * 50}",
            f"  MSE  (Mean Squared Error)     : {metrics['MSE']:.4f}",
            f"  PSNR (Peak Signal-to-Noise)   : {metrics['PSNR']:.2f} dB",
            f"  SSIM (Structural Similarity)  : {metrics['SSIM']:.4f}",
            f"{'=' * 50}",
            "",
            "  Interpretation:",
            f"    MSE  -> Lower is better (0 = identical)",
            f"    PSNR -> Higher is better (>30 dB = good quality)",
            f"    SSIM -> Higher is better (1.0 = identical)",
            f"{'=' * 50}",
        ]
        return "\n".join(lines)
