# Changelog

All notable changes to Croppy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-07

### Added
- Cross-platform compatibility (Windows, macOS, Linux)
- Adaptive theming (automatic dark/light mode detection)
- Modular architecture with separate managers
- High-DPI display support
- Batch cropping with auto-advance
- Keyboard navigation shortcuts
- Platform-specific UI optimizations
- Comprehensive error handling
- Modern Python packaging (pyproject.toml)

### Features
- 📁 Directory selection with image filtering
- ◀ ▶ Image navigation with keyboard support
- ✂️ Crop mode with visual selection
- 🎨 Automatic theme adaptation
- 💾 Smart save directory management
- ⌨️ Keyboard shortcuts (arrow keys, escape)
- 🖼️ Multiple image format support (PNG, JPG, GIF, BMP)

### Technical
- Python 3.8+ compatibility
- Type hints throughout codebase
- Comprehensive documentation
- Cross-platform startup script
- Proper package structure for PyPI
- Git repository ready

### Architecture
- `croppy/main.py` - Main application coordinator
- `croppy/theme_manager.py` - Theme detection and color management
- `croppy/ui_components.py` - Cross-platform UI setup
- `croppy/image_handler.py` - Image loading and display
- `croppy/file_manager.py` - File operations and directory management
- `croppy/crop_manager.py` - Crop functionality

## [1.0.0] - Previous Version
- Basic image viewing and cropping functionality
