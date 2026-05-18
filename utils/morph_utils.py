"""
Morphological Operations Utility Functions
--------------------------------------------
Provides erosion, dilation, opening, and closing operations.

DIP Concepts: Morphological image processing (spatial domain)
"""

import cv2
import numpy as np


def erode(image, kernel_size=3, iterations=1):
    """
    Apply morphological erosion.

    Erosion shrinks white regions by sliding a structuring element across the image.
    A pixel is set to white only if ALL pixels under the kernel are white.

    Parameters
    ----------
    image : np.ndarray
        Input binary or grayscale image.
    kernel_size : int
        Size of the square structuring element.
    iterations : int
        Number of times erosion is applied.

    Returns
    -------
    eroded : np.ndarray
        Eroded image.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    eroded = cv2.erode(image, kernel, iterations=iterations)
    return eroded


def dilate(image, kernel_size=3, iterations=1):
    """
    Apply morphological dilation.

    Dilation expands white regions by sliding a structuring element across the image.
    A pixel is set to white if ANY pixel under the kernel is white.

    Parameters
    ----------
    image : np.ndarray
        Input binary or grayscale image.
    kernel_size : int
        Size of the square structuring element.
    iterations : int
        Number of times dilation is applied.

    Returns
    -------
    dilated : np.ndarray
        Dilated image.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilated = cv2.dilate(image, kernel, iterations=iterations)
    return dilated


def opening(image, kernel_size=3):
    """
    Apply morphological opening (erosion followed by dilation).

    Opening removes small white noise regions while preserving larger structures.
    It is useful for removing salt noise from binary images.

    Parameters
    ----------
    image : np.ndarray
        Input binary image.
    kernel_size : int
        Size of the structuring element.

    Returns
    -------
    opened : np.ndarray
        Opened image.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    opened = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opened


def closing(image, kernel_size=3):
    """
    Apply morphological closing (dilation followed by erosion).

    Closing fills small black holes/gaps in white regions while preserving the shape.
    It is useful for closing small gaps in text characters.

    Parameters
    ----------
    image : np.ndarray
        Input binary image.
    kernel_size : int
        Size of the structuring element.

    Returns
    -------
    closed : np.ndarray
        Closed image.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    closed = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closed


def custom_kernel_dilate(image, kernel_shape):
    """
    Apply dilation with a custom-shaped kernel.

    Useful for text line detection where horizontal or vertical kernels
    are needed to connect characters into text blocks.

    Parameters
    ----------
    image : np.ndarray
        Input binary image.
    kernel_shape : tuple
        (width, height) of the rectangular kernel.

    Returns
    -------
    dilated : np.ndarray
        Dilated image with custom kernel.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_shape)
    dilated = cv2.dilate(image, kernel, iterations=1)
    return dilated
