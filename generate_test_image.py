"""
Generate a synthetic test document image for pipeline testing.
Creates a realistic-looking document with text, noise, and slight skew.
"""

import cv2
import numpy as np
import os

def create_test_document():
    """Create a synthetic document image with text-like content."""
    # Create white page (A4-ish proportions)
    height, width = 1200, 900
    doc = np.ones((height, width, 3), dtype=np.uint8) * 245  # slightly off-white

    # Add title
    cv2.putText(doc, "DOCUMENT SCANNER TEST", (80, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (10, 10, 10), 3)
    
    # Add horizontal line under title
    cv2.line(doc, (80, 100), (width - 80, 100), (50, 50, 50), 2)

    # Add paragraphs of text-like content
    y_pos = 150
    lines = [
        "Digital Image Processing is a fascinating field that",
        "deals with the manipulation of images using computers.",
        "This project implements a Document Scanner system",
        "that can correct perspective, remove noise, enhance",
        "contrast, and binarize documents for OCR processing.",
        "",
        "The system uses multiple DIP techniques including:",
        "  1. Canny edge detection for boundary finding",
        "  2. FFT-based frequency domain filtering",
        "  3. Otsu and Sauvola adaptive binarization",
        "  4. Morphological operations for cleanup",
        "  5. Histogram equalization for enhancement",
        "",
        "Air University Multan Campus - Spring 2026",
        "Course: CS 345 - Digital Image Processing",
        "Instructor: Sir Muhammad Faisal Idrees",
    ]

    for line in lines:
        if line:
            cv2.putText(doc, line, (80, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 1)
        y_pos += 35

    # Add a rectangular "image" region
    cv2.rectangle(doc, (80, y_pos + 20), (400, y_pos + 200), (180, 180, 180), -1)
    cv2.putText(doc, "[FIGURE 1]", (160, y_pos + 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 80, 80), 2)

    # Add more text after image
    y_pos += 240
    more_lines = [
        "The results demonstrate significant improvement in",
        "document readability after processing through our",
        "complete six-stage pipeline implementation.",
        "",
        "Quality metrics: PSNR, MSE, and SSIM are computed",
        "at each stage to quantify the improvement.",
    ]
    for line in more_lines:
        if line:
            cv2.putText(doc, line, (80, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 1)
        y_pos += 35

    # Add footer
    cv2.line(doc, (80, height - 60), (width - 80, height - 60), (100, 100, 100), 1)
    cv2.putText(doc, "Page 1 of 1", (width // 2 - 60, height - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)

    # --- Add realistic distortions ---

    # 1. Add slight rotation (skew)
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, 2.5, 1.0)  # 2.5 degree tilt
    doc = cv2.warpAffine(doc, M, (width, height),
                         borderMode=cv2.BORDER_CONSTANT,
                         borderValue=(200, 200, 200))

    # 2. Add Gaussian noise
    noise = np.random.normal(0, 12, doc.shape).astype(np.int16)
    doc = np.clip(doc.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # 3. Add slight uneven lighting (gradient)
    gradient = np.linspace(0.85, 1.0, width).reshape(1, -1, 1)
    gradient = np.tile(gradient, (height, 1, 3))
    doc = np.clip(doc * gradient, 0, 255).astype(np.uint8)

    # 4. Add some salt & pepper noise
    sp_mask = np.random.random(doc.shape[:2])
    doc[sp_mask < 0.002] = 0       # salt
    doc[sp_mask > 0.998] = 255     # pepper

    return doc


if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(__file__), "input_images")
    os.makedirs(output_dir, exist_ok=True)

    print("Generating synthetic test document...")
    test_doc = create_test_document()

    path = os.path.join(output_dir, "test_document.jpg")
    cv2.imwrite(path, test_doc)
    print(f"Saved: {path}")
    print(f"Size: {test_doc.shape[1]}x{test_doc.shape[0]} px")
    print("\nYou can now run: python main.py --input input_images/test_document.jpg")
