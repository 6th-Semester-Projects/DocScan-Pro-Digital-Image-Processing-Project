"""
Noise Simulator - Add various types of noise to images for demonstration
--------------------------------------------------------------------------
Implements 6 noise types as required by the DIP curriculum.

DIP Concepts: Noise models (Gaussian, Rayleigh, Erlang, Exponential, Uniform, Salt & Pepper)
"""

import cv2
import numpy as np


class NoiseSimulator:
    """Add various types of noise to images for testing/demonstration."""

    @staticmethod
    def add_gaussian(image, mean=0, sigma=25):
        """Add Gaussian noise. Most common noise model."""
        noise = np.random.normal(mean, sigma, image.shape).astype(np.float64)
        noisy = np.clip(image.astype(np.float64) + noise, 0, 255)
        return noisy.astype(np.uint8)

    @staticmethod
    def add_salt_pepper(image, amount=0.02):
        """Add salt & pepper (impulse) noise."""
        noisy = image.copy()
        # Salt
        num_salt = int(amount * image.size / 2)
        coords = [np.random.randint(0, i, num_salt) for i in image.shape[:2]]
        if len(image.shape) == 3:
            noisy[coords[0], coords[1], :] = 255
        else:
            noisy[coords[0], coords[1]] = 255
        # Pepper
        coords = [np.random.randint(0, i, num_salt) for i in image.shape[:2]]
        if len(image.shape) == 3:
            noisy[coords[0], coords[1], :] = 0
        else:
            noisy[coords[0], coords[1]] = 0
        return noisy

    @staticmethod
    def add_uniform(image, low=-30, high=30):
        """Add uniform noise."""
        noise = np.random.uniform(low, high, image.shape)
        noisy = np.clip(image.astype(np.float64) + noise, 0, 255)
        return noisy.astype(np.uint8)

    @staticmethod
    def add_rayleigh(image, scale=20):
        """Add Rayleigh noise."""
        noise = np.random.rayleigh(scale, image.shape)
        noisy = np.clip(image.astype(np.float64) + noise, 0, 255)
        return noisy.astype(np.uint8)

    @staticmethod
    def add_exponential(image, scale=20):
        """Add exponential noise."""
        noise = np.random.exponential(scale, image.shape)
        noisy = np.clip(image.astype(np.float64) + noise, 0, 255)
        return noisy.astype(np.uint8)

    @staticmethod
    def add_erlang(image, shape=2, scale=10):
        """Add Erlang (Gamma) noise."""
        noise = np.random.gamma(shape, scale, image.shape)
        noisy = np.clip(image.astype(np.float64) + noise, 0, 255)
        return noisy.astype(np.uint8)

    @staticmethod
    def add_poisson(image):
        """Add Poisson noise."""
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(max(vals, 1)))
        noisy = np.random.poisson(np.maximum(image.astype(np.float64) / 255.0 * vals, 0.001))
        noisy = np.clip(noisy / vals * 255, 0, 255)
        return noisy.astype(np.uint8)

    @staticmethod
    def apply_noise(image, noise_type='gaussian', **kwargs):
        """Apply specified noise type."""
        methods = {
            'gaussian': NoiseSimulator.add_gaussian,
            'salt_pepper': NoiseSimulator.add_salt_pepper,
            'uniform': NoiseSimulator.add_uniform,
            'rayleigh': NoiseSimulator.add_rayleigh,
            'exponential': NoiseSimulator.add_exponential,
            'erlang': NoiseSimulator.add_erlang,
            'poisson': NoiseSimulator.add_poisson,
        }
        if noise_type not in methods:
            raise ValueError(f"Unknown noise type: {noise_type}")
        return methods[noise_type](image, **kwargs)

    @staticmethod
    def get_available_types():
        """Return list of available noise types."""
        return ['gaussian', 'salt_pepper', 'uniform', 'rayleigh',
                'exponential', 'erlang', 'poisson']
