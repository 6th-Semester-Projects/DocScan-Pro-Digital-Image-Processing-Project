"""
OutputFormatter - Save Results, Metrics & Reports
----------------------------------------------------
Saves all pipeline stage outputs, computes quality metrics,
generates comparison figures and text reports.

DIP Concepts: PSNR, MSE, SSIM computation, result visualization
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from modules.metrics import MetricsCalculator
from utils.histogram_utils import plot_histogram_comparison


class OutputFormatter:
    """
    Handles saving results and generating reports for the pipeline.
    """

    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.metrics_calc = MetricsCalculator()

    def save_image(self, image, filename):
        """Save a single image to the output directory."""
        path = os.path.join(self.output_dir, filename)
        cv2.imwrite(path, image)
        print(f"  [+] Saved -> {path}")
        return path

    def save_pipeline_results(self, results_dict, prefix=""):
        """
        Save all pipeline stage images.

        Parameters
        ----------
        results_dict : dict
            {stage_name: image} pairs
        prefix : str
            Filename prefix (e.g., image name)
        """
        saved_paths = {}
        for stage_name, image in results_dict.items():
            if image is None:
                continue
            filename = f"{prefix}_{stage_name}.png" if prefix else f"{stage_name}.png"
            path = self.save_image(image, filename)
            saved_paths[stage_name] = path
        return saved_paths

    def create_comparison_figure(self, stages_dict, save_path=None, title="Processing Pipeline"):
        """
        Create a side-by-side comparison of all pipeline stages.

        Parameters
        ----------
        stages_dict : dict
            Ordered dict of {stage_name: image} pairs.
        save_path : str or None
            Save path. If None, auto-generates in output_dir.
        """
        n = len(stages_dict)
        if n == 0:
            return None

        cols = min(3, n)
        rows = (n + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(7 * cols, 6 * rows))
        if rows == 1 and cols == 1:
            axes = np.array([axes])
        axes = np.array(axes).flatten()

        for idx, (name, img) in enumerate(stages_dict.items()):
            if len(img.shape) == 3:
                axes[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            else:
                axes[idx].imshow(img, cmap='gray')

            axes[idx].set_title(name, fontsize=11, fontweight='bold')
            axes[idx].axis('off')

        for idx in range(n, len(axes)):
            axes[idx].axis('off')

        plt.suptitle(title, fontsize=16, fontweight='bold', y=1.01)
        plt.tight_layout()

        if save_path is None:
            save_path = os.path.join(self.output_dir, "pipeline_comparison.png")

        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  [+] Pipeline comparison saved -> {save_path}")
        plt.close(fig)
        return fig

    def compute_and_save_metrics(self, original, processed, stage_name="Final"):
        """Compute quality metrics between original and processed image."""
        metrics = self.metrics_calc.compute_all(original, processed)
        report = self.metrics_calc.format_report(metrics, title=f"{stage_name} Quality Metrics")
        return metrics, report

    def generate_text_report(self, doc_info, all_metrics, pipeline_stages,
                             save_path=None):
        """
        Generate a comprehensive text report with all metrics.

        Parameters
        ----------
        doc_info : dict
            Document metadata from ScannedDocument.get_info()
        all_metrics : dict
            {stage_name: metrics_dict} pairs
        pipeline_stages : list
            List of stage names in order
        """
        if save_path is None:
            save_path = os.path.join(self.output_dir, "metrics_report.txt")

        lines = []
        lines.append("=" * 60)
        lines.append("  DOCUMENT SCANNER & OCR PRE-PROCESSOR")
        lines.append("  Quality Metrics Report")
        lines.append("=" * 60)
        lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # Document info
        lines.append("-" * 60)
        lines.append("  INPUT DOCUMENT INFORMATION")
        lines.append("-" * 60)
        for key, value in doc_info.items():
            if key == 'filesize_kb':
                lines.append(f"  {key:20s}: {value:.1f} KB")
            else:
                lines.append(f"  {key:20s}: {value}")
        lines.append("")

        # Processing pipeline
        lines.append("-" * 60)
        lines.append("  PROCESSING PIPELINE")
        lines.append("-" * 60)
        for i, stage in enumerate(pipeline_stages, 1):
            lines.append(f"  Stage {i}: {stage}")
        lines.append("")

        # Quality metrics for each stage
        lines.append("-" * 60)
        lines.append("  QUALITY METRICS")
        lines.append("-" * 60)

        for stage_name, metrics in all_metrics.items():
            lines.append(f"\n  --- {stage_name} ---")
            lines.append(f"  MSE  : {metrics['MSE']:.4f}")
            lines.append(f"  PSNR : {metrics['PSNR']:.2f} dB")
            lines.append(f"  SSIM : {metrics['SSIM']:.4f}")
        lines.append("")

        # Interpretation guide
        lines.append("-" * 60)
        lines.append("  METRIC INTERPRETATION GUIDE")
        lines.append("-" * 60)
        lines.append("  MSE  -> Lower is better (0 = identical images)")
        lines.append("  PSNR -> Higher is better (>30 dB = excellent)")
        lines.append("  SSIM -> Higher is better (1.0 = identical)")
        lines.append("")
        lines.append("=" * 60)
        lines.append("  Air University Multan Campus - Spring 2026")
        lines.append("  CS 345: Digital Image Processing")
        lines.append("=" * 60)

        report_text = "\n".join(lines)

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"  [+] Metrics report saved -> {save_path}")
        return report_text

    def save_histogram_comparison(self, before, after, save_path=None):
        """Save before/after histogram comparison figure."""
        if save_path is None:
            save_path = os.path.join(self.output_dir, "histogram_comparison.png")

        plot_histogram_comparison(before, after, save_path=save_path)
        return save_path

    def save_spectrum_visualization(self, freq_debug_info, save_path=None):
        """Save frequency spectrum visualization from FrequencyFilter debug info."""
        if save_path is None:
            save_path = os.path.join(self.output_dir, "frequency_spectrum.png")

        fig, axes = plt.subplots(1, 3, figsize=(18, 5))

        axes[0].imshow(freq_debug_info['magnitude_before'], cmap='gray')
        axes[0].set_title("Original Spectrum", fontweight='bold')
        axes[0].axis('off')

        axes[1].imshow(freq_debug_info['filter_mask'], cmap='jet')
        axes[1].set_title("Filter Mask", fontweight='bold')
        axes[1].axis('off')

        axes[2].imshow(freq_debug_info['magnitude_after'], cmap='gray')
        axes[2].set_title("Filtered Spectrum", fontweight='bold')
        axes[2].axis('off')

        plt.suptitle("Frequency Domain Analysis", fontsize=14, fontweight='bold')
        plt.tight_layout()
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"  [+] Spectrum visualization saved -> {save_path}")
        return save_path

    def create_edge_comparison(self, image, save_path=None):
        """Create comparison of different edge detection methods."""
        from utils.edge_utils import canny_edges, sobel_edges, laplacian_edges

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        canny = canny_edges(gray)
        sobel = sobel_edges(gray)
        laplacian = laplacian_edges(gray)

        fig, axes = plt.subplots(1, 4, figsize=(20, 5))

        axes[0].imshow(gray, cmap='gray')
        axes[0].set_title("Original", fontweight='bold')
        axes[0].axis('off')

        axes[1].imshow(canny, cmap='gray')
        axes[1].set_title("Canny Edges", fontweight='bold')
        axes[1].axis('off')

        axes[2].imshow(sobel, cmap='gray')
        axes[2].set_title("Sobel Edges", fontweight='bold')
        axes[2].axis('off')

        axes[3].imshow(laplacian, cmap='gray')
        axes[3].set_title("Laplacian Edges", fontweight='bold')
        axes[3].axis('off')

        plt.suptitle("Edge Detection Comparison", fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path is None:
            save_path = os.path.join(self.output_dir, "edge_comparison.png")

        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"  [+] Edge comparison saved -> {save_path}")
        return save_path
