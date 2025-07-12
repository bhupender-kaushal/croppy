"""
Theme Manager - Handles system theme detection and color management
Cross-platform compatible theme detection for Windows, macOS, and Linux
"""
import os
import sys
import subprocess
import platform


class ThemeManager:
    def __init__(self):
        self.colors = {}
        self.setup_theme()
    
    def detect_system_theme(self):
        """Detect if the system is using dark mode or light mode across platforms"""
        try:
            system = platform.system().lower()
            
            if system == "darwin":  # macOS
                return self._detect_macos_theme()
            elif system == "windows":  # Windows
                return self._detect_windows_theme()
            elif system == "linux":  # Linux
                return self._detect_linux_theme()
            else:
                return "light"  # Default fallback
        except Exception as e:
            print(f"Theme detection error: {e}")
            return "light"  # Safe fallback
    
    def _detect_macos_theme(self):
        """Detect macOS dark mode"""
        try:
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "dark" if result.stdout.strip() == "Dark" else "light"
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            return "light"
    
    def _detect_windows_theme(self):
        """Detect Windows dark mode"""
        try:
            import winreg
            # Check Windows 10/11 theme setting
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return "light" if value else "dark"
        except (ImportError, OSError, FileNotFoundError, Exception):
            # Fallback for older Windows versions or import errors
            return "light"
    
    def _detect_linux_theme(self):
        """Detect Linux desktop environment theme"""
        # Try multiple detection methods for different desktop environments
        
        # Method 1: GNOME/GTK theme detection
        try:
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                capture_output=True,
                text=True,
                timeout=5
            )
            theme_name = result.stdout.strip().strip("'\"").lower()
            if "dark" in theme_name:
                return "dark"
            elif "light" in theme_name:
                return "light"
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Method 2: KDE Plasma theme detection
        try:
            result = subprocess.run(
                ["kreadconfig5", "--group", "Colors:Window", "--key", "BackgroundNormal"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Dark themes typically have darker background colors
            bg_color = result.stdout.strip()
            if bg_color and len(bg_color) >= 6:
                # Convert hex to RGB and check brightness
                try:
                    r = int(bg_color[0:2], 16) if len(bg_color) >= 2 else 128
                    g = int(bg_color[2:4], 16) if len(bg_color) >= 4 else 128
                    b = int(bg_color[4:6], 16) if len(bg_color) >= 6 else 128
                    brightness = (r + g + b) / 3
                    return "dark" if brightness < 128 else "light"
                except ValueError:
                    pass
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Method 3: Environment variables
        gtk_theme = os.environ.get('GTK_THEME', '').lower()
        if 'dark' in gtk_theme:
            return "dark"
        
        # Method 4: Check common theme files
        home = os.path.expanduser("~")
        theme_files = [
            os.path.join(home, ".config", "gtk-3.0", "settings.ini"),
            os.path.join(home, ".gtkrc-2.0")
        ]
        
        for theme_file in theme_files:
            try:
                if os.path.exists(theme_file):
                    with open(theme_file, 'r') as f:
                        content = f.read().lower()
                        if 'dark' in content:
                            return "dark"
            except (IOError, PermissionError):
                continue
        
        # Default fallback
        return "light"

    def setup_theme(self):
        """Set up theme colors based on system theme detection"""
        theme = self.detect_system_theme()
        
        if theme == "dark":
            self.colors = {
                # Window and frame colors
                'window_bg': '#2b2b2b',
                'bottom_bar_bg': '#3c3c3c',
                'canvas_bg': '#1e1e1e',
                
                # Button colors
                'button_bg': '#1a1a1a',
                'button_fg': '#ffffff',
                'button_active_bg': '#2a2a2a',
                'button_active_fg': '#ffffff',
                'button_relief': 'flat',
                
                # Exit button (special red styling)
                'exit_button_bg': '#cc4444',
                'exit_button_fg': '#ffffff',
                'exit_button_active_bg': '#dd5555',
                'exit_button_active_fg': '#ffffff',
                
                # Text colors for canvas
                'text_color': '#ffffff',
                'error_text_color': '#ff6b6b',
                
                # Border colors for crop
                'crop_border_color': '#ff4444',
                'image_border_color': '#666666'
            }
        else:  # light theme
            self.colors = {
                # Window and frame colors
                'window_bg': '#f0f0f0',
                'bottom_bar_bg': '#e0e0e0',
                'canvas_bg': '#ffffff',
                
                # Button colors
                'button_bg': '#f5f5f5',
                'button_fg': '#333333',
                'button_active_bg': '#e0e0e0',
                'button_active_fg': '#333333',
                'button_relief': 'raised',
                
                # Exit button (special red styling)
                'exit_button_bg': '#f44336',
                'exit_button_fg': '#ffffff',
                'exit_button_active_bg': '#e53935',
                'exit_button_active_fg': '#ffffff',
                
                # Text colors for canvas
                'text_color': '#333333',
                'error_text_color': '#d32f2f',
                
                # Border colors for crop
                'crop_border_color': '#ff0000',
                'image_border_color': '#cccccc'
            }

    def get_opposite_color(self, image):
        """Get an opposite color based on the image's corner pixels and app theme"""
        # Sample corner pixels to determine dominant color
        width, height = image.size
        corners = [
            image.getpixel((0, 0)),
            image.getpixel((width-1, 0)),
            image.getpixel((0, height-1)),
            image.getpixel((width-1, height-1))
        ]
        
        # Convert to RGB if needed and calculate average
        rgb_corners = []
        for corner in corners:
            if isinstance(corner, tuple) and len(corner) >= 3:
                rgb_corners.append(corner[:3])
            elif isinstance(corner, int):
                rgb_corners.append((corner, corner, corner))
            else:
                rgb_corners.append((128, 128, 128))  # Default gray
        
        # Calculate average color
        avg_r = sum(r for r, g, b in rgb_corners) // len(rgb_corners)
        avg_g = sum(g for r, g, b in rgb_corners) // len(rgb_corners)
        avg_b = sum(b for r, g, b in rgb_corners) // len(rgb_corners)
        
        # Calculate brightness
        brightness = (avg_r + avg_g + avg_b) / 3
        
        # Determine buffer color based on image brightness and app theme
        theme = self.detect_system_theme()
        
        if theme == "dark":
            # In dark theme, prefer darker buffer colors
            if brightness > 127:
                return "#1a1a1a"  # Very dark for bright images
            else:
                return "#3a3a3a"  # Medium dark for dark images
        else:
            # In light theme, use the original logic
            if brightness > 127:
                return "#2c2c2c"  # Dark gray for bright images
            else:
                return "#e0e0e0"  # Light gray for dark images
