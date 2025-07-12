"""
Image Handler - Manages image loading, display, and processing
Cross-platform image handling with robust error handling and format support
"""
from PIL import Image, ImageTk, __version__ as pil_version
import os
import platform

# Define resampling filter based on PIL/Pillow version for maximum compatibility
try:
    # Pillow 10.0.0+ uses Resampling enum
    from PIL.Image import Resampling
    LANCZOS = Resampling.LANCZOS
except (ImportError, AttributeError):
    try:
        # Pillow 9.x and earlier
        LANCZOS = Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS
    except AttributeError:
        # Very old PIL versions
        LANCZOS = Image.ANTIALIAS


class ImageHandler:
    def __init__(self, canvas, colors, theme_manager):
        self.canvas = canvas
        self.colors = colors
        self.theme_manager = theme_manager
        self.buffer_size = 20  # 20 pixel buffer around image
        self.loading = False
        self.platform = platform.system().lower()
        
        # Image display properties
        self.display_width = 0
        self.display_height = 0
        self.image_x = 0
        self.image_y = 0
        self.original_image = None
        self.img_tk = None
        
        # Initialize PIL with better error handling
        self._initialize_pil()

    def _initialize_pil(self):
        """Initialize PIL with platform-specific optimizations"""
        try:
            # Enable better text rendering on Windows
            if self.platform == "windows":
                from PIL import ImageFont
                # Windows might need specific font handling
                pass
            elif self.platform == "darwin":
                # macOS specific PIL optimizations
                pass
            elif self.platform == "linux":
                # Linux specific PIL optimizations
                pass
        except ImportError:
            pass  # PIL components might not be available

    def load_image_without_counting(self, image_path, crop_mode=False, title_callback=None):
        """Load image without incrementing the processed count (for initial load)"""
        if self.loading:
            return
            
        self.loading = True
        
        try:
            self.original_image = self._safe_image_open(image_path)
            if self.original_image:
                self._display_image(image_path, crop_mode, title_callback)
            
        except Exception as e:
            self._show_error(f"Error loading image: {e}")
            print(f"Error loading image: {e}")
        finally:
            self.loading = False

    def load_image(self, image_path, crop_mode=False, title_callback=None):
        """Load image and increment processed count"""
        if self.loading:
            return
            
        self.loading = True
        
        try:
            self.original_image = self._safe_image_open(image_path)
            if self.original_image:
                self._display_image(image_path, crop_mode, title_callback)
            
        except Exception as e:
            self._show_error(f"Error loading image: {e}")
            print(f"Error loading image: {e}")
        finally:
            self.loading = False

    def _safe_image_open(self, image_path):
        """Safely open an image with cross-platform error handling"""
        try:
            # Normalize the path for the current platform
            normalized_path = os.path.normpath(image_path)
            
            # Check if file exists and is readable
            if not os.path.exists(normalized_path):
                raise FileNotFoundError(f"Image file not found: {normalized_path}")
            
            if not os.access(normalized_path, os.R_OK):
                raise PermissionError(f"Cannot read image file: {normalized_path}")
            
            # Open the image with PIL
            image = Image.open(normalized_path)
            
            # Convert to RGB if necessary (handles various formats)
            if image.mode not in ('RGB', 'RGBA'):
                if image.mode == 'P' and 'transparency' in image.info:
                    # Handle palette images with transparency
                    image = image.convert('RGBA')
                else:
                    image = image.convert('RGB')
            
            return image
            
        except (FileNotFoundError, PermissionError) as e:
            raise e
        except Exception as e:
            raise Exception(f"Failed to open image: {str(e)}")
        
        try:
            self.original_image = Image.open(image_path)
            self._display_image(image_path, crop_mode, title_callback)
            
        except Exception as e:
            self._show_error(f"Error loading image: {e}")
            print(f"Error loading image: {e}")
        finally:
            self.loading = False

    def _display_image(self, image_path, crop_mode, title_callback):
        """Internal method to handle image display logic"""
        # Get canvas dimensions with better fallbacks
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 600
            
        # Calculate aspect ratio to maintain image proportions
        img_width, img_height = self.original_image.size
        aspect_ratio = img_width / img_height
        
        # Reserve space for buffer on all sides
        available_width = canvas_width - (2 * self.buffer_size)
        available_height = canvas_height - (2 * self.buffer_size)
        
        # Calculate new dimensions while maintaining aspect ratio
        if available_width / available_height > aspect_ratio:
            # Available space is wider than image aspect ratio
            self.display_height = available_height
            self.display_width = int(available_height * aspect_ratio)
        else:
            # Available space is taller than image aspect ratio
            self.display_width = available_width
            self.display_height = int(available_width / aspect_ratio)
        
        # Calculate image position to center it (including buffer)
        self.image_x = (canvas_width - self.display_width) // 2
        self.image_y = (canvas_height - self.display_height) // 2
        
        # Get opposite color for buffer
        buffer_color = self.theme_manager.get_opposite_color(self.original_image)
        
        # Resize image for display
        display_image = self.original_image.resize((self.display_width, self.display_height), LANCZOS)
        self.img_tk = ImageTk.PhotoImage(display_image)
        
        # Clear canvas and set buffer background
        self.canvas.delete("all")
        self.canvas.configure(bg=buffer_color)
        self.canvas.create_image(self.image_x, self.image_y, anchor='nw', image=self.img_tk)
        
        # Add a subtle border around the image for better visibility
        border_color = self.colors['image_border_color']
        self.canvas.create_rectangle(
            self.image_x - 1, self.image_y - 1,
            self.image_x + self.display_width + 1, self.image_y + self.display_height + 1,
            outline=border_color, width=1
        )
        
        # Update window title if callback provided
        if title_callback:
            title_callback(image_path, crop_mode)

    def _show_error(self, error_message):
        """Show error message on canvas"""
        canvas_width = self.canvas.winfo_width() or 400
        canvas_height = self.canvas.winfo_height() or 300
        self.canvas.delete("all")
        self.canvas.create_text(
            canvas_width//2, canvas_height//2, 
            text=error_message, 
            fill=self.colors['error_text_color'], 
            font=("Arial", 12)
        )

    def show_no_images_message(self):
        """Show 'no images found' message on canvas"""
        canvas_width = self.canvas.winfo_width() or 400
        canvas_height = self.canvas.winfo_height() or 300
        self.canvas.delete("all")
        self.canvas.create_text(
            canvas_width//2, canvas_height//2, 
            text="No images found in the directory.", 
            fill=self.colors['text_color'], 
            font=("Arial", 12)
        )

    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
