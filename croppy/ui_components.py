"""
UI Components - Handles UI setup and component creation
Cross-platform compatible UI components for Windows, macOS, and Linux
"""
import tkinter as tk
import platform
import sys


class UIComponents:
    def __init__(self, master, colors, command_handlers):
        self.master = master
        self.colors = colors
        self.handlers = command_handlers
        self.platform = platform.system().lower()
        self.setup_window()
        self.setup_ui_components()
        self.setup_event_bindings()
    
    def setup_window(self):
        """Set up the main window properties with OS-specific adjustments"""
        # Get system DPI for better cross-platform compatibility
        dpi = self.get_system_dpi()
        
        # Set window size to 15x15 cm, adjusted for DPI
        width_pixels = int(15 * dpi / 2.54)  # Convert cm to pixels
        height_pixels = int(15 * dpi / 2.54)  # Convert cm to pixels
        
        # Ensure minimum reasonable window size
        min_width = max(600, width_pixels)
        min_height = max(600, height_pixels)
        
        self.master.geometry(f"{min_width}x{min_height}")
        self.master.minsize(min_width, min_height)
        
        # Apply theme to main window
        self.master.configure(bg=self.colors['window_bg'])
        
        # Platform-specific window settings
        self.apply_platform_specific_settings()
    
    def get_system_dpi(self):
        """Get system DPI with cross-platform compatibility"""
        try:
            if self.platform == "windows":
                # Windows DPI awareness
                try:
                    import ctypes
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per-monitor DPI aware
                    dpi = self.master.winfo_fpixels('1i')
                    return int(dpi) if dpi > 0 else 96
                except (AttributeError, OSError):
                    return 96
            elif self.platform == "darwin":
                # macOS Retina display handling
                dpi = self.master.winfo_fpixels('1i')
                return int(dpi) if dpi > 0 else 72
            else:
                # Linux/Unix
                dpi = self.master.winfo_fpixels('1i')
                return int(dpi) if dpi > 0 else 96
        except:
            return 96  # Safe fallback
    
    def apply_platform_specific_settings(self):
        """Apply platform-specific window and UI settings"""
        if self.platform == "darwin":
            # macOS specific settings
            try:
                # Enable macOS-style window controls
                self.master.tk.call('::tk::unsupported::MacWindowStyle', 'style', self.master._w, 'documentProc')
            except tk.TclError:
                pass
        elif self.platform == "windows":
            # Windows specific settings
            try:
                # Set Windows icon (if available)
                self.master.iconbitmap(default='icon.ico')
            except (tk.TclError, FileNotFoundError):
                pass
        # Linux typically doesn't need special handling

    def setup_ui_components(self):
        """Set up all UI components"""
        self.setup_frames()
        self.setup_canvas()
        self.setup_buttons()

    def setup_frames(self):
        """Set up the main frames"""
        # Bottom bar frame (pack first to keep it at bottom)
        self.bottom_bar = tk.Frame(self.master, bg=self.colors['bottom_bar_bg'], height=50)
        self.bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.bottom_bar.pack_propagate(False)  # Maintain fixed height

        # Main frame to hold image
        self.main_frame = tk.Frame(self.master, bg=self.colors['window_bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def setup_canvas(self):
        """Set up the canvas for image display"""
        self.canvas = tk.Canvas(self.main_frame, bg=self.colors['canvas_bg'])
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        
        # Bind mouse events for cropping
        self.canvas.bind("<Button-1>", self.handlers['start_crop'])
        self.canvas.bind("<B1-Motion>", self.handlers['update_crop'])
        self.canvas.bind("<ButtonRelease-1>", self.handlers['end_crop'])
        self.canvas.bind("<Motion>", self.handlers['on_mouse_motion'])

    def setup_buttons(self):
        """Set up all navigation and control buttons with cross-platform compatibility"""
        # Get platform-appropriate button configuration
        button_config = self.get_button_config()
        
        # Get platform-appropriate button icons
        icons = self.get_platform_icons()

        self.load_button = tk.Button(
            self.bottom_bar, 
            text=icons['folder'], 
            command=self.handlers['choose_directory'], 
            **button_config
        )
        self.load_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.prev_button = tk.Button(
            self.bottom_bar, 
            text=icons['previous'], 
            command=self.handlers['show_previous'], 
            state=tk.DISABLED, 
            **button_config
        )
        self.prev_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.next_button = tk.Button(
            self.bottom_bar, 
            text=icons['next'], 
            command=self.handlers['show_next'], 
            state=tk.DISABLED, 
            **button_config
        )
        self.next_button.pack(side=tk.LEFT, padx=2, pady=2)

        self.crop_button = tk.Button(
            self.bottom_bar, 
            text=icons['crop'], 
            command=self.handlers['crop_image'], 
            state=tk.DISABLED, 
            **button_config
        )
        self.crop_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Exit crop button (initially hidden)
        exit_button_config = self.get_exit_button_config()
        self.exit_crop_button = tk.Button(
            self.bottom_bar, 
            text=icons['exit'], 
            command=self.handlers['exit_crop_mode'], 
            **exit_button_config
        )
        # Don't pack initially - will be shown when crop mode is active
    
    def get_button_config(self):
        """Get platform-appropriate button configuration"""
        base_config = {
            'bg': self.colors['button_bg'],
            'fg': self.colors['button_fg'],
            'activebackground': self.colors['button_active_bg'],
            'activeforeground': self.colors['button_active_fg'],
            'relief': self.colors['button_relief'],
            'borderwidth': 1,
            'padx': 8,
            'pady': 4
        }
        
        if self.platform == "darwin":
            # macOS specific button styling
            base_config.update({
                'font': ("SF Pro Display", 16),
                'relief': 'flat',
                'borderwidth': 0,
                'padx': 12,
                'pady': 6
            })
        elif self.platform == "windows":
            # Windows specific button styling
            base_config.update({
                'font': ("Segoe UI", 14),
                'relief': 'raised',
                'borderwidth': 1,
                'padx': 10,
                'pady': 5
            })
        else:
            # Linux/Unix button styling
            base_config.update({
                'font': ("DejaVu Sans", 14),
                'relief': 'raised',
                'borderwidth': 1,
                'padx': 8,
                'pady': 4
            })
        
        return base_config
    
    def get_exit_button_config(self):
        """Get exit button specific configuration"""
        config = self.get_button_config().copy()
        config.update({
            'bg': self.colors['exit_button_bg'],
            'fg': self.colors['exit_button_fg'],
            'activebackground': self.colors['exit_button_active_bg'],
            'activeforeground': self.colors['exit_button_active_fg']
        })
        return config
    
    def get_platform_icons(self):
        """Get platform-appropriate icons/text for buttons"""
        if self.platform == "windows":
            # Windows might not support all Unicode emojis well
            return {
                'folder': "📁",
                'previous': "◀",
                'next': "▶",
                'crop': "✂",
                'exit': "✕"
            }
        elif self.platform == "darwin":
            # macOS has excellent Unicode support
            return {
                'folder': "📁",
                'previous': "◀",
                'next': "▶",
                'crop': "✂️",
                'exit': "❌"
            }
        else:
            # Linux - use safer Unicode characters
            return {
                'folder': "📁",
                'previous': "←",
                'next': "→",
                'crop': "✂",
                'exit': "✕"
            }

    def setup_event_bindings(self):
        """Set up all keyboard and window event bindings"""
        self.master.bind("<Configure>", lambda _: self.handlers['resize_image']())
        self.master.bind("<Escape>", self.handlers['handle_escape'])
        
        # Bind keyboard navigation
        self.master.bind("<Key-Right>", self.handlers['key_next_image'])
        self.master.bind("<Key-Down>", self.handlers['key_next_image'])
        self.master.bind("<Key-Left>", self.handlers['key_previous_image'])
        self.master.bind("<Key-Up>", self.handlers['key_previous_image'])
        
        self.master.focus_set()  # Make sure window can receive key events

    def update_command_handlers(self, new_handlers):
        """Update command handlers after initialization"""
        self.handlers = new_handlers
        # Re-bind mouse events with updated handlers
        self.canvas.bind("<Button-1>", self.handlers['start_crop'])
        self.canvas.bind("<B1-Motion>", self.handlers['update_crop'])
        self.canvas.bind("<ButtonRelease-1>", self.handlers['end_crop'])
        self.canvas.bind("<Motion>", self.handlers['on_mouse_motion'])
