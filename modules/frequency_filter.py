"""
FrequencyFilter - FFT-Based Noise Removal
--------------------------------------------
Removes noise using frequency domain filtering (2D DFT/FFT).
Implements Butterworth and Gaussian low-pass filters.

DIP Concepts: 2D DFT/FFT, frequency domain filtering, spectrum visualization
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


class FrequencyFilter:
    """
    Frequency domain image filter using 2D FFT.

    Pipeline: image -> FFT -> shift -> apply filter -> inverse shift -> inverse FFT
    """

    def __init__(self, filter_type='butterworth', cutoff=60, order=2):
        self.filter_type = filter_type
        self.cutoff = cutoff
        self.order = order

    def compute_dft(self, image):
        """
        Compute 2D DFT and shift zero-frequency to center.

        Returns: (shifted_spectrum, magnitude_spectrum)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
        gray = gray.astype(np.float64)

        # 2D FFT
        f_transform = np.fft.fft2(gray)
        # Shift zero-frequency component to center
        f_shift = np.fft.fftshift(f_transform)
        # Magnitude spectrum (log scale for visualization)
        magnitude = np.log1p(np.abs(f_shift))

        return f_shift, magnitude

    def butterworth_lpf(self, shape, cutoff, order=2):
        """
        Create Butterworth Low-Pass Filter mask.

        H(u,v) = 1 / (1 + (D(u,v)/D0)^(2n))
        where D(u,v) = distance from center, D0 = cutoff frequency
        """
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2

        u = np.arange(rows).reshape(-1, 1) - crow
        v = np.arange(cols).reshape(1, -1) - ccol
        D = np.sqrt(u ** 2 + v ** 2)

        # Butterworth formula
        H = 1 / (1 + (D / cutoff) ** (2 * order))
        return H

    def gaussian_lpf(self, shape, cutoff):
        """
        Create Gaussian Low-Pass Filter mask.

        H(u,v) = exp(-D(u,v)^2 / (2 * D0^2))
        """
        rows, cols = shape
        crow, ccol = rows // 2, cols // 2

        u = np.arange(rows).reshape(-1, 1) - crow
        v = np.arange(cols).reshape(1, -1) - ccol
        D_sq = u ** 2 + v ** 2

        H = np.exp(-D_sq / (2 * cutoff ** 2))
        return H

    def apply_filter(self, f_shift, filter_mask):
        """Apply frequency filter and compute inverse DFT."""
        # Apply filter in frequency domain
        filtered_shift = f_shift * filter_mask
        # Inverse shift
        f_ishift = np.fft.ifftshift(filtered_shift)
        # Inverse FFT
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)
        # Clip to valid range without changing relative brightness
        img_back = np.clip(img_back, 0, 255).astype(np.uint8)
        return img_back

    def visualize_spectrum(self, magnitude_before, magnitude_after,
                           filter_mask, save_path=None):
        """Visualize frequency spectrums before and after filtering."""
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        axes[0].imshow(magnitude_before, cmap='gray')
        axes[0].set_title("Original Spectrum", fontsize=12, fontweight='bold')
        axes[0].axis('off')

        axes[1].imshow(filter_mask, cmap='gray')
        axes[1].set_title(f"{self.filter_type.title()} LPF (D0={self.cutoff})",
                          fontsize=12, fontweight='bold')
        axes[1].axis('off')

        axes[2].imshow(magnitude_after, cmap='gray')
        axes[2].set_title("Filtered Spectrum", fontsize=12, fontweight='bold')
        axes[2].axis('off')

        plt.suptitle("Frequency Domain Analysis", fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  [+] Spectrum visualization saved -> {save_path}")

        plt.close(fig)
        return fig

    def process(self, image, filter_type=None, cutoff=None):
        """
        Full frequency domain filtering pipeline.

        Steps:
        1. Compute 2D DFT
        2. Create filter mask (Butterworth or Gaussian LPF)
        3. Apply filter in frequency domain
        4. Inverse DFT to get filtered image
        """
        f_type = filter_type or self.filter_type
        d0 = cutoff or self.cutoff

        print("\n" + "=" * 50)
        print("  STAGE 2: Frequency Domain Filtering")
        print("=" * 50)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()

        # Step 1: Compute DFT
        print(f"\n  -> Computing 2D FFT...")
        f_shift, mag_before = self.compute_dft(gray)

        # Step 2: Create filter
        print(f"  -> Creating {f_type} LPF (cutoff={d0})...")
        if f_type == 'butterworth':
            H = self.butterworth_lpf(gray.shape, d0, self.order)
        else:
            H = self.gaussian_lpf(gray.shape, d0)

        # Step 3: Apply filter
        print(f"  -> Applying filter in frequency domain...")
        filtered = self.apply_filter(f_shift, H)

        # Compute filtered spectrum for visualization
        filtered_shift = f_shift * H
        mag_after = np.log1p(np.abs(filtered_shift))

        print(f"  [+] Frequency filtering complete")

        debug_info = {
            'magnitude_before': mag_before,
            'magnitude_after': mag_after,
            'filter_mask': H,
        }

        return filtered, debug_info
