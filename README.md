# Croppy

<div align="center">
  <img src="croppy.png" alt="Croppy - Image Viewer & Cropper" width="600">
  <p><em>A modern, cross-platform image viewer and cropper</em></p>
</div>

A modern, cross-platform image viewer and cropper built with Python and Tkinter. Features adaptive theming, intuitive navigation, and efficient batch cropping capabilities.

## ✨ Features

- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Adaptive Theming**: Automatically detects and adapts to system dark/light mode
- **Intuitive Navigation**: Keyboard shortcuts and mouse controls
- **Batch Cropping**: Efficiently crop multiple images with auto-advance
- **Modern UI**: Clean, responsive interface with high-DPI support
- **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, BMP image formats
- **Smart Saving**: Automatic directory management for cropped images

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- tkinter (usually included with Python)
- Pillow (PIL) for image processing

### Installation

#### Option 1: Simple Installation
```bash
pip install Pillow>=10.0.0
python run.py
```

#### Option 2: Development Installation
```bash
git clone https://github.com/bhupenderkaushal/croppy.git
cd croppy
pip install -r requirements.txt
python run.py
```

#### Option 3: Package Installation
```bash
pip install croppy
croppy
```

### Platform-Specific Setup

#### Windows
```bash
pip install Pillow
python run.py
```

#### macOS
```bash
# If using system Python
pip3 install Pillow
python3 run.py

# If using Homebrew Python and tkinter issues
brew install python-tk
pip install Pillow
python run.py
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-pip
pip3 install Pillow
python3 run.py
```

#### Linux (Fedora/CentOS)
```bash
sudo dnf install python3-tkinter python3-pip
pip3 install Pillow
python3 run.py
```

#### Linux (Arch)
```bash
sudo pacman -S tk python-pip
pip install Pillow
python run.py
```

## 🎮 Usage

### Basic Navigation
- **📁 Button**: Select a folder containing images
- **← → Arrows**: Navigate between images (or use arrow keys)
- **✂️ Button**: Enter crop mode
- **❌ Button**: Exit crop mode
- **Escape Key**: Exit fullscreen mode

### Cropping Workflow
1. Click **📁** to select an image directory
2. Navigate to desired image using **← →** buttons or arrow keys
3. Click **✂️** to enter crop mode
4. Click and drag to select the area to crop
5. Confirm save when prompted
6. Application auto-advances to next image

### Keyboard Shortcuts
- `←` / `↑`: Previous image
- `→` / `↓`: Next image  
- `Escape`: Exit crop mode or fullscreen

## 🏗️ Architecture

Croppy is built with a modular architecture:

- **`croppy/main.py`**: Main application coordinator
- **`croppy/theme_manager.py`**: System theme detection and color management  
- **`croppy/ui_components.py`**: User interface setup and event handling
- **`croppy/image_handler.py`**: Image loading, display, and processing
- **`croppy/file_manager.py`**: File operations and directory management
- **`croppy/crop_manager.py`**: Crop mode and selection handling
- **`run.py`**: Cross-platform startup script

## 🔧 Configuration

### Theme Customization
Croppy automatically detects your system theme. Colors are defined in `croppy/theme_manager.py` and can be customized:

```python
# Dark mode colors
'button_bg': '#2a2a2a'      # Button background
'button_fg': '#ffffff'      # Button text
'canvas_bg': '#1e1e1e'      # Image canvas background
# ... more colors
```

### File Format Support
Supported image formats:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)

## 🐛 Troubleshooting

### Common Issues

#### "No module named 'tkinter'"
**Linux**: Install tkinter package
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/CentOS
sudo dnf install python3-tkinter

# Arch Linux
sudo pacman -S tk
```

#### "No module named 'PIL'"
Install Pillow:
```bash
pip install Pillow>=10.0.0
```

#### High-DPI Display Issues
Croppy automatically handles DPI scaling on Windows 10+. For older systems or manual control, DPI awareness is set in `run.py`.

#### macOS Permission Issues
If you encounter permission issues accessing directories:
```bash
# Grant Terminal full disk access in System Preferences > Security & Privacy
```

### Performance Tips
- For large image directories, Croppy loads images on-demand
- Crop operations use the original image resolution for quality
- Memory usage is optimized with image buffering

## 🧪 Development

### Setting up Development Environment
```bash
git clone <repository-url>
cd croppy
pip install -r requirements.txt

# Optional: Install development tools
pip install black mypy flake8 pytest
```

### Code Style
The project uses modern Python practices:
- Type hints (Python 3.8+ compatible)
- Black code formatting
- Mypy type checking
- Flake8 linting

### Running Tests
```bash
python -m pytest tests/
```

### Building Distribution
```bash
python -m build
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux (modern distributions)
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 50MB for application, additional space for images
- **Display**: Any resolution, optimized for high-DPI displays

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Image processing powered by Pillow (PIL)
- Cross-platform compatibility testing
- Modern UI design principles
