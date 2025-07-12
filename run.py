#!/usr/bin/env python3
"""
Cross-platform startup script for Image Viewer & Cropper
Handles platform-specific initialization and dependency checking
"""
import sys
import platform
import os

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    # Check Python version - support Python 3.8+ for better compatibility
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required for optimal compatibility")
        print(f"Current version: {sys.version}")
        return False
    
    # Check tkinter with better error handling
    try:
        import tkinter
        import tkinter.ttk  # Check themed widgets support
        import tkinter.filedialog
        import tkinter.messagebox
    except ImportError as e:
        missing_deps.append(f"tkinter ({e})")
    
    # Check PIL/Pillow with version compatibility
    try:
        from PIL import Image, ImageTk
        import PIL
        # Check if PIL version is compatible
        pil_version = getattr(PIL, '__version__', '0.0.0')
        print(f"PIL/Pillow version: {pil_version}")
    except ImportError:
        missing_deps.append("Pillow")
    
    # Check for additional modules used in the app
    try:
        import subprocess
        import threading
        import pathlib
    except ImportError as e:
        missing_deps.append(f"standard library module ({e})")
    
    if missing_deps:
        print("Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        
        print("\nTo install missing dependencies:")
        if "Pillow" in str(missing_deps):
            print("  pip install Pillow>=8.0.0")
        if "tkinter" in str(missing_deps):
            system = platform.system().lower()
            if system == "linux":
                print("  # Ubuntu/Debian:")
                print("  sudo apt-get install python3-tk python3-dev")
                print("  # CentOS/RHEL/Fedora:")
                print("  sudo dnf install python3-tkinter")
                print("  # Arch Linux:")
                print("  sudo pacman -S tk")
            elif system == "darwin":
                print("  # macOS with Homebrew:")
                print("  brew install python-tk")
            else:
                print("  tkinter should be included with Python on your system")
        
        return False
    
    return True

def main():
    """Main startup function with cross-platform compatibility"""
    print("Croppy - Starting...")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Platform-specific setup
    system = platform.system().lower()
    
    if system == "windows":
        # Windows-specific setup with better error handling
        try:
            import ctypes
            from ctypes import wintypes
            
            # Set DPI awareness for better scaling on high-DPI displays
            try:
                # Try the newer method first (Windows 10 v1703+)
                ctypes.windll.shcore.SetProcessDpiAwarenessContext(-4)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
            except (AttributeError, OSError):
                try:
                    # Fallback to older method
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                except (AttributeError, OSError):
                    try:
                        # Final fallback
                        ctypes.windll.user32.SetProcessDPIAware()
                    except (AttributeError, OSError):
                        pass
            
            # Set console output encoding for better Unicode support
            try:
                import locale
                locale.setlocale(locale.LC_ALL, '')
            except (locale.Error, AttributeError):
                pass
                
        except ImportError:
            print("Warning: Could not set up Windows-specific features")
            pass
    
    elif system == "darwin":
        # macOS-specific setup
        try:
            # Ensure proper app behavior on macOS
            import subprocess
            subprocess.run(["defaults", "write", "-g", "NSRequiresAquaSystemAppearance", "-bool", "false"], 
                         capture_output=True)
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
    
    # Import and run the main application
    try:
        from croppy.main import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == '__main__':
    main()
