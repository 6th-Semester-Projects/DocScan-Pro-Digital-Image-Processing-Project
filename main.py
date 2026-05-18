"""
================================================================================
    DOCUMENT SCANNER & OCR PRE-PROCESSOR
    Digital Image Processing - Semester Project
    Air University Multan Campus, Spring 2026
    
    Course: CS 345 - Digital Image Processing
    Instructor: Sir Muhammad Faisal Idrees
================================================================================

This is the main entry point that runs the complete document processing pipeline:
    1. Load scanned/photographed document image
    2. Perspective correction & deskewing
    3. Frequency domain noise removal (FFT + Butterworth/Gaussian LPF)
    4. Contrast enhancement (histogram equalization)
    5. Adaptive binarization (Otsu / Sauvola)
    6. Layout analysis (text vs image separation)
    7. Save results + quality metrics report

Usage:
    python main.py
    python main.py --input input_images/sample1.jpg
    python main.py --input input_images/sample1.jpg --method otsu
    python main.py --all
"""

import os
import sys
import argparse
import glob
import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving figures

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *
from modules.scanned_document import ScannedDocument
from modules.deskew_corrector import DeskewCorrector
from modules.frequency_filter import FrequencyFilter
from modules.binarization_engine import BinarizationEngine
from modules.layout_analyzer import LayoutAnalyzer
from modules.output_formatter import OutputFormatter
from modules.metrics import MetricsCalculator
from utils.histogram_utils import (
    histogram_equalization, clahe_enhancement,
    plot_histogram_comparison, compute_histogram
)
from utils.edge_utils import canny_edges, sobel_edges


def print_banner():
    """Print the project banner."""
    print("\n" + "=" * 60)
    print("  DOCUMENT SCANNER & OCR PRE-PROCESSOR")
    print("  Digital Image Processing - Semester Project")
    print("  Air University Multan Campus, Spring 2026")
    print("=" * 60)


def process_document(input_path, output_dir=None, binarization_method=None,
                     filter_type=None, cutoff=None):
    """
    Process a single document image through the complete pipeline.

    Parameters
    ----------
    input_path : str
        Path to input document image.
    output_dir : str or None
        Output directory (auto-created). Defaults to config OUTPUT_DIR.
    binarization_method : str or None
        'otsu' or 'sauvola'. Defaults to config setting.
    filter_type : str or None
        'butterworth' or 'gaussian'. Defaults to config setting.
    cutoff : int or None
        Frequency filter cutoff. Defaults to config setting.

    Returns
    -------
    dict
        Dictionary with all pipeline results and metrics.
    """
    # Resolve parameters
    out_dir = output_dir or OUTPUT_DIR
    bin_method = binarization_method or BINARIZATION_METHOD
    f_type = filter_type or FFT_FILTER_TYPE
    f_cutoff = cutoff or BUTTERWORTH_CUTOFF

    os.makedirs(out_dir, exist_ok=True)

    # Initialize all modules
    doc = ScannedDocument(input_path)
    corrector = DeskewCorrector(
        canny_low=CANNY_LOW_THRESHOLD,
        canny_high=CANNY_HIGH_THRESHOLD,
        blur_kernel=GAUSSIAN_BLUR_KERNEL,
        max_skew_angle=MAX_SKEW_ANGLE,
    )
    freq_filter = FrequencyFilter(
        filter_type=f_type,
        cutoff=f_cutoff,
        order=BUTTERWORTH_ORDER,
    )
    binarizer = BinarizationEngine(
        method=bin_method,
        window_size=SAUVOLA_WINDOW_SIZE,
        k=SAUVOLA_K,
        R=SAUVOLA_R,
        morph_kernel=MORPH_KERNEL_SIZE,
    )
    analyzer = LayoutAnalyzer(
        h_kernel=TEXT_DILATE_KERNEL_H,
        v_kernel=TEXT_DILATE_KERNEL_V,
        min_area=MIN_REGION_AREA,
        text_ar_threshold=TEXT_ASPECT_RATIO_THRESHOLD,
        img_min_area=IMAGE_REGION_MIN_AREA,
    )
    formatter = OutputFormatter(output_dir=out_dir)
    metrics_calc = MetricsCalculator()

    # Store all pipeline results
    pipeline = {}
    all_metrics = {}
    prefix = doc.filename

    # -----------------------------------------
    # STAGE 0: Load Image
    # -----------------------------------------
    print("\n" + "=" * 50)
    print("  STAGE 0: Loading Document Image")
    print("=" * 50)

    original = doc.load()
    doc_info = doc.get_info()
    original_gray = doc.to_grayscale()
    pipeline['0_Original'] = original.copy()

    # -----------------------------------------
    # STAGE 1: Geometric Correction
    # -----------------------------------------
    corrected, deskew_debug = corrector.process(original)
    pipeline['1_Corrected'] = corrected.copy()

    # Save edge detection visualization
    if SAVE_INTERMEDIATE_STEPS:
        formatter.save_image(deskew_debug['edges'], f"{prefix}_edges_canny.png")

    # -----------------------------------------
    # STAGE 2: Frequency Domain Filtering
    # -----------------------------------------
    corrected_gray = cv2.cvtColor(corrected, cv2.COLOR_BGR2GRAY) if len(corrected.shape) == 3 else corrected
    filtered, freq_debug = freq_filter.process(corrected)
    pipeline['2_FFT_Filtered'] = filtered.copy()

    # Save spectrum visualization
    formatter.save_spectrum_visualization(freq_debug,
        save_path=os.path.join(out_dir, f"{prefix}_{SPECTRUM_FILENAME}"))

    # Compute metrics after filtering
    metrics_filtered = metrics_calc.compute_all(corrected_gray, filtered)
    all_metrics['After FFT Filtering'] = metrics_filtered
    print(f"  -> PSNR after filtering: {metrics_filtered['PSNR']:.2f} dB")

    # -----------------------------------------
    # STAGE 3: Contrast Enhancement
    # -----------------------------------------
    print("\n" + "=" * 50)
    print("  STAGE 3: Contrast Enhancement")
    print("=" * 50)

    print("\n  -> Applying histogram equalization...")
    enhanced = histogram_equalization(filtered)

    # Also apply CLAHE for comparison
    clahe_result = clahe_enhancement(filtered, clip_limit=2.0, tile_size=(8, 8))

    pipeline['3_Enhanced'] = enhanced.copy()

    # Save histogram comparison
    print("  -> Generating histogram comparison...")
    formatter.save_histogram_comparison(filtered, enhanced,
        save_path=os.path.join(out_dir, f"{prefix}_{HISTOGRAM_FILENAME}"))

    # Metrics after enhancement
    metrics_enhanced = metrics_calc.compute_all(corrected_gray, enhanced)
    all_metrics['After Enhancement'] = metrics_enhanced
    print(f"  [+] Contrast enhancement complete")
    print(f"  -> PSNR after enhancement: {metrics_enhanced['PSNR']:.2f} dB")

    # -----------------------------------------
    # STAGE 4: Adaptive Binarization
    # -----------------------------------------
    binarized, bin_debug = binarizer.process(enhanced, method=bin_method)
    pipeline['4_Binarized'] = binarized.copy()

    # Also produce result with the OTHER method for comparison
    other_method = 'otsu' if bin_method == 'sauvola' else 'sauvola'
    print(f"\n  -> Also producing {other_method.upper()} result for comparison...")
    other_binary, _ = binarizer.process(enhanced, method=other_method)

    if SAVE_INTERMEDIATE_STEPS:
        formatter.save_image(other_binary, f"{prefix}_binarized_{other_method}.png")

    # Metrics after binarization
    metrics_binarized = metrics_calc.compute_all(corrected_gray, binarized)
    all_metrics['After Binarization'] = metrics_binarized

    # -----------------------------------------
    # STAGE 5: Layout Analysis
    # -----------------------------------------
    layout_vis, layout_debug = analyzer.process(binarized, corrected)
    pipeline['5_Layout'] = layout_vis.copy()

    # -----------------------------------------
    # STAGE 6: Edge Detection Comparison
    # -----------------------------------------
    print("\n" + "=" * 50)
    print("  STAGE 6: Edge Detection Comparison")
    print("=" * 50)
    formatter.create_edge_comparison(corrected,
        save_path=os.path.join(out_dir, f"{prefix}_edge_comparison.png"))

    # -----------------------------------------
    # SAVE ALL RESULTS
    # -----------------------------------------
    print("\n" + "=" * 50)
    print("  SAVING RESULTS")
    print("=" * 50)

    # Save each pipeline stage
    print("\n  -> Saving pipeline stage images...")
    for stage_name, img in pipeline.items():
        formatter.save_image(img, f"{prefix}_{stage_name}.png")

    # Save pipeline comparison figure
    print("\n  -> Creating pipeline comparison figure...")
    formatter.create_comparison_figure(
        pipeline,
        save_path=os.path.join(out_dir, f"{prefix}_{COMPARISON_FILENAME}"),
        title=f"Document Processing Pipeline - {doc.filename}"
    )

    # Generate text report
    print("\n  -> Generating metrics report...")
    pipeline_stages = [
        "Load Image",
        "Geometric Correction (Perspective + Deskew)",
        f"Frequency Filtering ({f_type.title()} LPF, D0={f_cutoff})",
        "Contrast Enhancement (Histogram Equalization)",
        f"Adaptive Binarization ({bin_method.title()})",
        "Layout Analysis (Text/Image Separation)",
    ]

    report = formatter.generate_text_report(
        doc_info, all_metrics, pipeline_stages,
        save_path=os.path.join(out_dir, f"{prefix}_{REPORT_FILENAME}")
    )

    # -----------------------------------------
    # FINAL SUMMARY
    # -----------------------------------------
    print("\n" + "=" * 60)
    print("  [OK] PROCESSING COMPLETE!")
    print("=" * 60)
    print(f"  Input:  {input_path}")
    print(f"  Output: {out_dir}")
    print(f"\n  Quality Metrics (Original -> Final):")
    final_metrics = all_metrics.get('After Binarization', {})
    print(f"    MSE  : {final_metrics.get('MSE', 'N/A'):.4f}" if isinstance(final_metrics.get('MSE'), float) else "    MSE  : N/A")
    print(f"    PSNR : {final_metrics.get('PSNR', 'N/A'):.2f} dB" if isinstance(final_metrics.get('PSNR'), float) else "    PSNR : N/A")
    print(f"    SSIM : {final_metrics.get('SSIM', 'N/A'):.4f}" if isinstance(final_metrics.get('SSIM'), float) else "    SSIM : N/A")
    print("=" * 60)

    return {
        'pipeline': pipeline,
        'metrics': all_metrics,
        'doc_info': doc_info,
        'report': report,
    }


def main():
    """Main entry point with command-line argument parsing."""
    print_banner()

    parser = argparse.ArgumentParser(
        description="Document Scanner & OCR Pre-processor - DIP Project"
    )
    parser.add_argument(
        '--input', '-i', type=str, default=None,
        help='Path to input document image'
    )
    parser.add_argument(
        '--all', '-a', action='store_true',
        help='Process all images in input_images/ folder'
    )
    parser.add_argument(
        '--method', '-m', type=str, default=None,
        choices=['otsu', 'sauvola'],
        help='Binarization method (default: from config.py)'
    )
    parser.add_argument(
        '--filter', '-f', type=str, default=None,
        choices=['butterworth', 'gaussian'],
        help='Frequency filter type (default: from config.py)'
    )
    parser.add_argument(
        '--cutoff', '-c', type=int, default=None,
        help='Frequency filter cutoff (default: from config.py)'
    )
    parser.add_argument(
        '--output', '-o', type=str, default=None,
        help='Output directory (default: output/)'
    )

    args = parser.parse_args()

    # Determine input images
    if args.all:
        # Process all images in input folder
        patterns = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
        image_files = []
        for pat in patterns:
            image_files.extend(glob.glob(os.path.join(INPUT_DIR, pat)))

        if not image_files:
            print(f"\n  [x] No images found in {INPUT_DIR}/")
            print(f"      Place your document images there and try again.")
            sys.exit(1)

        print(f"\n  Found {len(image_files)} image(s) to process:")
        for f in image_files:
            print(f"    -> {os.path.basename(f)}")

        for img_path in image_files:
            try:
                process_document(
                    img_path,
                    output_dir=args.output,
                    binarization_method=args.method,
                    filter_type=args.filter,
                    cutoff=args.cutoff,
                )
            except Exception as e:
                print(f"\n  [x] Error processing {img_path}: {e}")

    elif args.input:
        # Process single specified image
        if not os.path.exists(args.input):
            print(f"\n  [x] File not found: {args.input}")
            sys.exit(1)

        process_document(
            args.input,
            output_dir=args.output,
            binarization_method=args.method,
            filter_type=args.filter,
            cutoff=args.cutoff,
        )

    else:
        # Default: process first image in input folder, or show help
        patterns = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif']
        image_files = []
        for pat in patterns:
            image_files.extend(glob.glob(os.path.join(INPUT_DIR, pat)))

        if image_files:
            print(f"\n  No input specified. Processing first image found:")
            print(f"    -> {image_files[0]}")
            process_document(
                image_files[0],
                output_dir=args.output,
                binarization_method=args.method,
                filter_type=args.filter,
                cutoff=args.cutoff,
            )
        else:
            print(f"\n  [!] No input image specified and no images in {INPUT_DIR}/")
            print(f"\n  Usage:")
            print(f"    python main.py --input input_images/sample1.jpg")
            print(f"    python main.py --all")
            print(f"\n  Place document images in the '{INPUT_DIR}' folder and try again.")
            sys.exit(1)


if __name__ == "__main__":
    main()
