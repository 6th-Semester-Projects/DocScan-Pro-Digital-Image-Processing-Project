"""
DeskewCorrector - Perspective Correction & Rotation Fix
---------------------------------------------------------
Corrects skewed/tilted document images using:
1. Perspective correction (4-point transform)
2. Rotation correction (Hough line detection)

DIP Concepts: Edge detection (Canny), geometric transforms, Hough Transform
"""

import cv2
import numpy as np


class DeskewCorrector:
    """
    Corrects geometric distortions in document images.

    Pipeline: detect boundary -> perspective warp -> detect skew -> rotate
    """

    def __init__(self, canny_low=50, canny_high=150, blur_kernel=(5, 5),
                 max_skew_angle=15):
        self.canny_low = canny_low
        self.canny_high = canny_high
        self.blur_kernel = blur_kernel
        self.max_skew_angle = max_skew_angle

    def detect_document_boundary(self, image):
        """Detect 4 corners of document using Canny + contour finding."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        edges = cv2.Canny(blurred, self.canny_low, self.canny_high)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        edges = cv2.dilate(edges, kernel, iterations=1)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, edges

        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        img_area = image.shape[0] * image.shape[1]
        
        for contour in contours[:5]:
            # Must be reasonably large to be the document page (at least 20% of image)
            if cv2.contourArea(contour) < 0.2 * img_area:
                continue
                
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if len(approx) == 4:
                corners = approx.reshape(4, 2)
                return self._order_corners(corners), edges
        return None, edges

    def _order_corners(self, pts):
        """Order points as: [top-left, top-right, bottom-right, bottom-left]."""
        ordered = np.zeros((4, 2), dtype=np.float32)
        s = pts.sum(axis=1)
        ordered[0] = pts[np.argmin(s)]
        ordered[2] = pts[np.argmax(s)]
        d = np.diff(pts, axis=1).flatten()
        ordered[1] = pts[np.argmin(d)]
        ordered[3] = pts[np.argmax(d)]
        return ordered

    def perspective_correct(self, image, corners):
        """Apply perspective warp to get top-down view of document."""
        tl, tr, br, bl = corners
        max_width = int(max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl)))
        max_height = int(max(np.linalg.norm(bl - tl), np.linalg.norm(br - tr)))

        dst = np.array([[0, 0], [max_width - 1, 0],
                        [max_width - 1, max_height - 1],
                        [0, max_height - 1]], dtype=np.float32)

        M = cv2.getPerspectiveTransform(corners.astype(np.float32), dst)
        warped = cv2.warpPerspective(image, M, (max_width, max_height))
        print(f"  [+] Perspective correction: {max_width}x{max_height} px")
        return warped

    def detect_skew_angle(self, image):
        """Detect skew angle using Hough Line Transform."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image.copy()
        edges = cv2.Canny(gray, self.canny_low, self.canny_high, apertureSize=3)

        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                                minLineLength=100, maxLineGap=10)

        lines_image = image.copy() if len(image.shape) == 3 else cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        if lines is None:
            print("  [!] No lines detected - skipping rotation")
            return 0.0, lines_image

        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if abs(angle) < self.max_skew_angle:
                angles.append(angle)
                cv2.line(lines_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        if not angles:
            return 0.0, lines_image

        median_angle = float(np.median(angles))
        print(f"  [+] Detected skew angle: {median_angle:.2f} deg")
        return median_angle, lines_image

    def deskew(self, image, angle=None):
        """Rotate image to correct skew."""
        if angle is None:
            angle, _ = self.detect_skew_angle(image)

        if abs(angle) < 0.5:
            print("  [i] Skew < 0.5 deg - no rotation needed")
            return image.copy()

        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        cos_val, sin_val = abs(M[0, 0]), abs(M[0, 1])
        new_w = int(h * sin_val + w * cos_val)
        new_h = int(h * cos_val + w * sin_val)
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2

        rotated = cv2.warpAffine(image, M, (new_w, new_h),
                                 borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(255, 255, 255))
        print(f"  [+] Deskew applied: {angle:.2f} deg")
        return rotated

    def process(self, image):
        """Full geometric correction pipeline."""
        print("\n" + "=" * 50)
        print("  STAGE 1: Geometric Correction")
        print("=" * 50)

        debug_info = {}

        print("\n  -> Detecting document boundary...")
        corners, edges = self.detect_document_boundary(image)
        debug_info['edges'] = edges

        if corners is not None:
            print("  -> Applying perspective correction...")
            corrected = self.perspective_correct(image, corners)
            debug_info['corners_found'] = True
        else:
            print("  [i] No boundary detected - using original")
            corrected = image.copy()
            debug_info['corners_found'] = False

        print("\n  -> Detecting skew angle...")
        angle, hough_lines = self.detect_skew_angle(corrected)
        debug_info['skew_angle'] = angle
        debug_info['hough_lines'] = hough_lines
        corrected = self.deskew(corrected, angle)

        return corrected, debug_info
