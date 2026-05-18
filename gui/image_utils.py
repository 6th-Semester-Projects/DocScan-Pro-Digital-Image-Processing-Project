"""
Image display utilities for the GUI.
Handles converting OpenCV images to Tkinter-compatible format and rendering.
"""
import cv2
import numpy as np
from PIL import Image, ImageTk


def cv2_to_tk(image, max_size=(600, 500)):
    """Convert OpenCV image to Tkinter PhotoImage, resized to fit."""
    if image is None:
        return None
    if len(image.shape) == 2:
        rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    # Resize maintaining aspect ratio
    pil_img.thumbnail(max_size, Image.LANCZOS)
    return ImageTk.PhotoImage(pil_img)


def cv2_to_pil(image):
    """Convert OpenCV image to PIL Image."""
    if image is None:
        return None
    if len(image.shape) == 2:
        rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def resize_for_display(image, max_w=600, max_h=500):
    """Resize image for display while keeping aspect ratio."""
    if image is None:
        return None
    h, w = image.shape[:2]
    scale = min(max_w / w, max_h / h, 1.0)
    if scale < 1.0:
        new_w, new_h = int(w * scale), int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return image.copy()
