"""
Configuration Parameters for Document Scanner & OCR Pre-processor
Digital Image Processing - Semester Project
Air University Multan Campus, Spring 2026
"""

import os

# ──────────────────────────────────────────────
# Directory Paths
# ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input_images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# ──────────────────────────────────────────────
# Deskew Corrector Settings
# ──────────────────────────────────────────────
CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 150
GAUSSIAN_BLUR_KERNEL = (5, 5)
HOUGH_RHO = 1
HOUGH_THETA_RESOLUTION = 1          # in degrees
HOUGH_THRESHOLD = 100
MIN_LINE_LENGTH = 100
MAX_LINE_GAP = 10
MAX_SKEW_ANGLE = 15                  # degrees - ignore angles beyond this

# ──────────────────────────────────────────────
# Frequency Filter Settings
# ──────────────────────────────────────────────
FFT_FILTER_TYPE = "butterworth"      # "butterworth" or "gaussian"
BUTTERWORTH_CUTOFF = 60              # cutoff frequency
BUTTERWORTH_ORDER = 2                # filter order
GAUSSIAN_CUTOFF = 60                 # cutoff for Gaussian LPF

# ──────────────────────────────────────────────
# Binarization Settings
# ──────────────────────────────────────────────
BINARIZATION_METHOD = "sauvola"      # "otsu" or "sauvola"
SAUVOLA_WINDOW_SIZE = 25             # must be odd
SAUVOLA_K = 0.2                      # Sauvola sensitivity parameter
SAUVOLA_R = 128                      # dynamic range of standard deviation
MORPH_KERNEL_SIZE = 3                # for morphological cleanup
MORPH_ITERATIONS = 1

# ──────────────────────────────────────────────
# Layout Analyzer Settings
# ──────────────────────────────────────────────
TEXT_DILATE_KERNEL_H = (25, 1)       # horizontal kernel for connecting text
TEXT_DILATE_KERNEL_V = (1, 10)       # vertical kernel
MIN_REGION_AREA = 500                # minimum area to consider a region
TEXT_ASPECT_RATIO_THRESHOLD = 1.5    # width/height > this -> likely text
IMAGE_REGION_MIN_AREA = 5000         # minimum area for image regions

# ──────────────────────────────────────────────
# Output Settings
# ──────────────────────────────────────────────
COMPARISON_FIG_DPI = 150
SAVE_INTERMEDIATE_STEPS = True       # save each pipeline stage
REPORT_FILENAME = "metrics_report.txt"
COMPARISON_FILENAME = "pipeline_comparison.png"
HISTOGRAM_FILENAME = "histogram_comparison.png"
SPECTRUM_FILENAME = "frequency_spectrum.png"
