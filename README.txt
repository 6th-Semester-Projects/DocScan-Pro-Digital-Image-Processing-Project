================================================================================
    DOCUMENT SCANNER & OCR PRE-PROCESSOR
    Digital Image Processing — Semester Project
    Air University Multan Campus, Spring 2026
================================================================================

PROJECT OVERVIEW
----------------
This project implements a complete Document Scanner & OCR Pre-processor pipeline
that takes messy, skewed, noisy scanned or photographed document images and 
produces clean, perfectly aligned, binarized output images ready for OCR.

The system covers 5+ core DIP concepts:
  - Spatial domain operations (filtering, morphology)
  - Frequency domain operations (FFT-based noise removal)
  - Histogram analysis (Otsu thresholding, histogram equalization)
  - Edge detection (Canny, Sobel)
  - Quantitative evaluation (PSNR, MSE, SSIM)


INSTALLATION
------------
1. Make sure Python 3.8 or later is installed on your system.

2. Open a terminal/command prompt and navigate to the project folder:
   cd path\to\DIP-Project

3. Install required libraries:
   pip install -r requirements.txt


HOW TO RUN
----------
1. Place your input document images in the "input_images" folder.
   - Supported formats: JPG, PNG, BMP, TIFF
   - You can use photos taken from a phone camera or scanned documents

2. Run the main pipeline:
   python main.py

3. To process a specific image:
   python main.py --input input_images/your_image.jpg

4. To change settings (binarization method, filter type, etc.):
   Edit "config.py" and adjust parameters as needed.


EXPECTED OUTPUT
---------------
After running, check the "output" folder. For each input image, you will find:
  - *_corrected.png      : Perspective-corrected and deskewed image
  - *_filtered.png        : Frequency-domain filtered image
  - *_enhanced.png        : Contrast-enhanced image
  - *_binarized.png       : Final binarized (black & white) document
  - *_layout.png          : Layout analysis with color-coded regions
  - pipeline_comparison.png  : Side-by-side comparison of all stages
  - histogram_comparison.png : Before/after histogram visualization
  - frequency_spectrum.png   : FFT magnitude spectrum visualization
  - metrics_report.txt       : PSNR, MSE, SSIM quality metrics


PROJECT STRUCTURE
-----------------
DIP-Project/
  main.py                 - Entry point, runs full pipeline
  config.py               - All configurable parameters
  requirements.txt        - Python dependencies
  README.txt              - This file
  modules/                - Core processing modules
    scanned_document.py   - Image I/O and metadata
    deskew_corrector.py   - Perspective & rotation correction
    frequency_filter.py   - FFT-based noise removal
    binarization_engine.py- Otsu & Sauvola binarization
    layout_analyzer.py    - Text vs image region separation
    output_formatter.py   - Save results, metrics, and reports
    metrics.py            - PSNR, MSE, SSIM computation
  utils/                  - Utility functions
    histogram_utils.py    - Histogram operations
    edge_utils.py         - Edge detection (Canny, Sobel)
    morph_utils.py        - Morphological operations
  input_images/           - Place input images here
  output/                 - Processed results (auto-created)


LIBRARIES USED
--------------
  - OpenCV (cv2)    : Image processing operations
  - NumPy           : Numerical computations
  - Matplotlib      : Visualization and plotting
  - SciPy           : Scientific computing (FFT)
  - Pillow (PIL)    : Image file handling
  - scikit-image    : SSIM metric computation


AUTHOR
------
  Name    : Muhammad Maauz Mansoor
  Roll No : 233599
  Course  : CS 345 — Digital Image Processing
  Section : A
  Instructor : Sir Muhammad Faisal Idrees
================================================================================
