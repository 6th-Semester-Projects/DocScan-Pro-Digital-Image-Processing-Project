"""
Document Scanner & OCR Pre-processor - Utility Functions
"""

from .histogram_utils import (
    compute_histogram,
    plot_histogram,
    plot_histogram_comparison,
    histogram_equalization,
)
from .edge_utils import canny_edges, sobel_edges, laplacian_edges
from .morph_utils import erode, dilate, opening, closing
