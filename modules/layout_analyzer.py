"""
LayoutAnalyzer - Text vs Image Region Separation
---------------------------------------------------
Analyzes document layout to identify and classify text blocks,
image regions, and whitespace using morphological operations
and connected component analysis.

DIP Concepts: Sobel edge detection, morphological dilation, connected components
"""

import cv2
import numpy as np
from utils.morph_utils import custom_kernel_dilate


class LayoutAnalyzer:
    """
    Analyzes document layout to separate text from image regions.

    Algorithm:
    1. Sobel edge detection for structure analysis
    2. Morphological dilation to connect text characters into blocks
    3. Connected component labeling to find regions
    4. Classification by aspect ratio, density, and size
    """

    # Color coding for region types (BGR format)
    COLORS = {
        'text': (0, 200, 0),        # Green
        'image': (200, 100, 0),     # Blue
        'other': (0, 0, 200),       # Red
    }

    def __init__(self, h_kernel=(25, 1), v_kernel=(1, 10),
                 min_area=500, text_ar_threshold=1.5, img_min_area=5000):
        self.h_kernel = h_kernel
        self.v_kernel = v_kernel
        self.min_area = min_area
        self.text_ar_threshold = text_ar_threshold
        self.img_min_area = img_min_area

    def detect_edges_sobel(self, image):
        """Apply Sobel edge detection for structure analysis."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
        magnitude = np.uint8(np.clip(magnitude / magnitude.max() * 255, 0, 255))
        return magnitude

    def find_text_blocks(self, binary_image):
        """
        Find text block regions using morphological dilation + connected components.

        Steps:
        1. Invert binary image (text becomes white)
        2. Dilate with horizontal kernel to connect characters in a line
        3. Dilate with vertical kernel to connect lines in a paragraph
        4. Find contours as text block candidates
        """
        # Ensure text is white on black
        if np.mean(binary_image) > 127:
            inverted = cv2.bitwise_not(binary_image)
        else:
            inverted = binary_image.copy()

        # Horizontal dilation to connect characters
        dilated = custom_kernel_dilate(inverted, self.h_kernel)
        # Vertical dilation to connect lines
        dilated = custom_kernel_dilate(dilated, self.v_kernel)

        # Find connected components
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            if area < self.min_area:
                continue

            aspect_ratio = w / max(h, 1)
            density = cv2.countNonZero(inverted[y:y+h, x:x+w]) / max(area, 1)

            regions.append({
                'bbox': (x, y, w, h),
                'area': area,
                'aspect_ratio': aspect_ratio,
                'density': density,
                'contour': contour,
            })

        return regions

    def classify_regions(self, regions):
        """
        Classify detected regions as text, image, or other.

        Classification rules:
        - Text: high aspect ratio (wide), moderate density
        - Image: large area, lower aspect ratio (squarish)
        - Other: everything else
        """
        classified = {'text': [], 'image': [], 'other': []}

        for region in regions:
            ar = region['aspect_ratio']
            area = region['area']
            density = region['density']

            if ar >= self.text_ar_threshold and 0.05 < density < 0.8:
                region['type'] = 'text'
                classified['text'].append(region)
            elif area >= self.img_min_area and ar < self.text_ar_threshold:
                region['type'] = 'image'
                classified['image'].append(region)
            else:
                # Small regions or unusual shapes
                if area >= self.min_area:
                    region['type'] = 'text'  # Default small regions to text
                    classified['text'].append(region)
                else:
                    region['type'] = 'other'
                    classified['other'].append(region)

        return classified

    def visualize_layout(self, original, classified_regions):
        """Draw color-coded bounding boxes on image."""
        if len(original.shape) == 2:
            vis = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
        else:
            vis = original.copy()

        counts = {'text': 0, 'image': 0, 'other': 0}

        for region_type, regions in classified_regions.items():
            color = self.COLORS.get(region_type, (128, 128, 128))
            for region in regions:
                x, y, w, h = region['bbox']
                cv2.rectangle(vis, (x, y), (x + w, y + h), color, 2)

                # Label
                label = f"{region_type.upper()}"
                cv2.putText(vis, label, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                counts[region_type] += 1

        # Add legend at bottom
        h_img = vis.shape[0]
        legend_y = h_img - 30
        for i, (rtype, color) in enumerate(self.COLORS.items()):
            x_pos = 10 + i * 180
            cv2.rectangle(vis, (x_pos, legend_y), (x_pos + 15, legend_y + 15), color, -1)
            cv2.putText(vis, f"{rtype}: {counts[rtype]}", (x_pos + 20, legend_y + 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)

        return vis, counts

    def process(self, binary_image, original_color):
        """
        Full layout analysis pipeline.

        Returns: (annotated_image, classified_regions, region_counts)
        """
        print("\n" + "=" * 50)
        print("  STAGE 5: Layout Analysis")
        print("=" * 50)

        # Step 1: Edge detection for structure
        print("\n  -> Sobel edge detection...")
        edges = self.detect_edges_sobel(binary_image)

        # Step 2: Find text block candidates
        print("  -> Finding text blocks (morphological dilation + CC)...")
        regions = self.find_text_blocks(binary_image)
        print(f"  -> Found {len(regions)} candidate regions")

        # Step 3: Classify regions
        print("  -> Classifying regions...")
        classified = self.classify_regions(regions)

        # Step 4: Visualize
        print("  -> Creating layout visualization...")
        layout_vis, counts = self.visualize_layout(original_color, classified)

        print(f"\n  [+] Layout Analysis Results:")
        print(f"      Text blocks:  {counts['text']}")
        print(f"      Image blocks: {counts['image']}")
        print(f"      Other:        {counts['other']}")

        debug_info = {
            'edges': edges,
            'regions': regions,
            'classified': classified,
            'counts': counts,
        }

        return layout_vis, debug_info
