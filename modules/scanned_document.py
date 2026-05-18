"""
ScannedDocument - Image I/O & Metadata
-----------------------------------------
Handles loading images from disk, storing metadata, displaying images,
and saving processed results.

DIP Concepts: Image I/O (reading, writing, displaying images)
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


class ScannedDocument:
    """
    Represents a scanned or photographed document image.

    This class handles all image I/O operations:
    - Loading images from disk (supports JPG, PNG, BMP, TIFF)
    - Extracting metadata (dimensions, channels, file size)
    - Displaying images using matplotlib
    - Saving processed images to disk

    Attributes
    ----------
    filepath : str
        Absolute path to the source image file.
    filename : str
        Base filename without extension.
    extension : str
        File extension (e.g., '.jpg').
    image : np.ndarray or None
        Loaded image in BGR format (OpenCV default).
    """

    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

    def __init__(self, filepath):
        """
        Initialize ScannedDocument with a file path.

        Parameters
        ----------
        filepath : str
            Path to the image file on disk.

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist.
        ValueError
            If the file format is not supported.
        """
        self.filepath = os.path.abspath(filepath)
        self.filename = os.path.splitext(os.path.basename(filepath))[0]
        self.extension = os.path.splitext(filepath)[1].lower()
        self.image = None

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Image file not found: {self.filepath}")

        if self.extension not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format '{self.extension}'. "
                f"Supported: {', '.join(self.SUPPORTED_FORMATS)}"
            )

    def load(self):
        """
        Load the image from disk using OpenCV.

        Returns
        -------
        np.ndarray
            Loaded image in BGR color format.

        Raises
        ------
        IOError
            If OpenCV fails to read the image.
        """
        self.image = cv2.imread(self.filepath, cv2.IMREAD_COLOR)

        if self.image is None:
            raise IOError(f"Failed to load image: {self.filepath}")

        print(f"  [+] Loaded: {self.filepath}")
        print(f"      Dimensions: {self.image.shape[1]}x{self.image.shape[0]} px")
        print(f"      Channels: {self.image.shape[2] if len(self.image.shape) == 3 else 1}")
        print(f"      File size: {os.path.getsize(self.filepath) / 1024:.1f} KB")

        return self.image

    def get_info(self):
        """
        Get metadata about the loaded image.

        Returns
        -------
        dict
            Dictionary containing:
            - 'filepath': absolute path
            - 'filename': base name without extension
            - 'width': image width in pixels
            - 'height': image height in pixels
            - 'channels': number of color channels
            - 'dtype': pixel data type
            - 'filesize_kb': file size in kilobytes
            - 'total_pixels': total number of pixels
        """
        if self.image is None:
            self.load()

        info = {
            'filepath': self.filepath,
            'filename': self.filename,
            'width': self.image.shape[1],
            'height': self.image.shape[0],
            'channels': self.image.shape[2] if len(self.image.shape) == 3 else 1,
            'dtype': str(self.image.dtype),
            'filesize_kb': os.path.getsize(self.filepath) / 1024,
            'total_pixels': self.image.shape[0] * self.image.shape[1],
        }
        return info

    def to_grayscale(self):
        """
        Convert the loaded image to grayscale.

        Returns
        -------
        np.ndarray
            Grayscale version of the image.
        """
        if self.image is None:
            self.load()

        if len(self.image.shape) == 2:
            return self.image.copy()

        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def display(self, title="Document Image", figsize=(10, 8)):
        """
        Display the image using matplotlib.

        Parameters
        ----------
        title : str
            Window/figure title.
        figsize : tuple
            Figure size in inches.
        """
        if self.image is None:
            self.load()

        fig, ax = plt.subplots(1, 1, figsize=figsize)

        if len(self.image.shape) == 3:
            # Convert BGR to RGB for matplotlib display
            rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            ax.imshow(rgb)
        else:
            ax.imshow(self.image, cmap='gray')

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        plt.close(fig)
        return fig

    @staticmethod
    def save(image, output_path):
        """
        Save an image to disk.

        Parameters
        ----------
        image : np.ndarray
            Image to save (BGR or grayscale).
        output_path : str
            Destination file path.

        Returns
        -------
        bool
            True if save was successful.
        """
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        success = cv2.imwrite(output_path, image)

        if success:
            print(f"  [+] Saved -> {output_path}")
        else:
            print(f"  [x] Failed to save -> {output_path}")

        return success

    @staticmethod
    def display_multiple(images_dict, figsize=(16, 10), save_path=None):
        """
        Display multiple images in a grid layout.

        Parameters
        ----------
        images_dict : dict
            Dictionary of {title: image} pairs.
        figsize : tuple
            Figure size.
        save_path : str or None
            If provided, save the figure.

        Returns
        -------
        fig : matplotlib.figure.Figure
        """
        n = len(images_dict)
        cols = min(3, n)
        rows = (n + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        if n == 1:
            axes = [axes]
        else:
            axes = axes.flatten()

        for idx, (title, img) in enumerate(images_dict.items()):
            if len(img.shape) == 3:
                axes[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            else:
                axes[idx].imshow(img, cmap='gray')
            axes[idx].set_title(title, fontsize=11, fontweight='bold')
            axes[idx].axis('off')

        # Hide unused axes
        for idx in range(n, len(axes)):
            axes[idx].axis('off')

        plt.suptitle("Document Processing Pipeline", fontsize=15, fontweight='bold')
        plt.tight_layout()

        if save_path:
            fig.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"  [+] Comparison figure saved -> {save_path}")

        plt.close(fig)
        return fig
