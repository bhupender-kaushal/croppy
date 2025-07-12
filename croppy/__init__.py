"""
Croppy - A modern, cross-platform image viewer and cropper
A Python package for viewing and cropping images with adaptive theming.
"""

__version__ = "2.0.0"
__author__ = "Bhupender Kaushal"
__email__ = "bhupenderkaushal5@gmail.com"
__description__ = "A modern, cross-platform image viewer and cropper with adequate functionalities"
__url__ = "https://github.com/bhupenderkaushal/croppy"

# Core functionality exports
from .main import Croppy, main

__all__ = ["Croppy", "main", "__version__"]
