#!/bin/bash
# Unix/Linux/macOS shell script to run Image Viewer & Cropper
# Handles platform-specific setup and dependency checking

echo "Image Viewer & Cropper - Unix/Linux/macOS Startup"
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

# Check Python version
python3 -c "import sys; exit(0 if sys.version_info >= (3, 6) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Python 3.6 or higher is required"
    python3 --version
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Warning: pip3 is not available"
    echo "You may need to install dependencies manually"
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt 2>/dev/null || {
        echo "Warning: Could not install some dependencies"
        echo "You may need to install them manually:"
        echo "  pip3 install -r requirements.txt"
    }
fi

# Check for tkinter (common issue on Linux)
python3 -c "import tkinter" 2>/dev/null || {
    echo "Error: tkinter is not available"
    echo "Please install tkinter:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  CentOS/RHEL: sudo yum install tkinter"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
    exit 1
}

# Run the application
echo "Starting Image Viewer & Cropper..."
python3 run.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "Application exited with an error"
    read -p "Press Enter to continue..."
fi
