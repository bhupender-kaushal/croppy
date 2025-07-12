#!/usr/bin/env python3
"""
Setup script for Image Viewer & Cropper
Compatible with Python 3.8+ through Python 3.12+
"""
from setuptools import setup, find_packages
import sys
import platform

# Check Python version
if sys.version_info < (3, 8):
    print("Error: Python 3.8 or higher is required")
    sys.exit(1)

# Read requirements
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [
        line.strip() 
        for line in f 
        if line.strip() and not line.startswith('#')
    ]

# Platform-specific requirements
platform_requirements = []
if platform.system().lower() == 'windows':
    platform_requirements.append('pywin32>=306')

setup(
    name="image-viewer-cropper",
    version="2.0.0",
    description="A cross-platform image viewer and cropper with modern UI",
    long_description=open('README.md', 'r', encoding='utf-8').read() if 
                    __import__('os').path.exists('README.md') else 
                    "A modular Tkinter-based image viewer with cropping functionality",
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/image-viewer-cropper",
    packages=find_packages(),
    py_modules=[
        'main',
        'theme_manager',
        'ui_components', 
        'image_handler',
        'file_manager',
        'crop_manager',
        'run'
    ],
    install_requires=requirements + platform_requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11", 
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    keywords="image viewer cropper tkinter gui cross-platform",
    entry_points={
        'console_scripts': [
            'image-viewer=run:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
