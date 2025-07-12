"""
Crop Manager - Handles all cropping functionality and crop mode management
"""
from tkinter import messagebox


class CropManager:
    def __init__(self, canvas, colors, image_handler):
        self.canvas = canvas
        self.colors = colors
        self.image_handler = image_handler
        
        # Crop mode variables
        self.crop_mode = False
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_rect_id = None
        
    def enter_crop_mode(self, ui_components, show_help_dialogs=True):
        """Enable persistent crop mode"""
        self.crop_mode = True
        self.canvas.config(cursor="crosshair")
        
        # Show exit crop button and hide crop button immediately
        ui_components.crop_button.pack_forget()
        ui_components.exit_crop_button.pack(side='left')
        
        # Force immediate UI update
        ui_components.master.update_idletasks()
        
        # Show instructions based on user experience
        if show_help_dialogs:
            messagebox.showinfo("Crop Mode", "Crop mode is now active!\n• Click and drag to select areas to crop\n• Use navigation buttons or arrow keys to move between images\n• Click ❌ to exit crop mode")
    
    def exit_crop_mode(self, ui_components, title_callback=None, current_image_path=None):
        """Exit crop mode and return to normal viewing"""
        self.crop_mode = False
        self.canvas.config(cursor="")
        
        # Show crop button and hide exit crop button immediately
        ui_components.exit_crop_button.pack_forget()
        ui_components.crop_button.pack(side='left')
        
        # Force immediate UI update
        ui_components.master.update_idletasks()
        
        # Clean up any existing crop rectangle
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)
            self.crop_rect_id = None
        
        # Reset title to normal
        if title_callback and current_image_path:
            title_callback(current_image_path, crop_mode=False)
    
    def on_mouse_motion(self, event):
        """Handle mouse motion to change cursor based on location"""
        if not self.crop_mode or not hasattr(self.image_handler, 'image_x'):
            return
        
        # Always show crosshair in crop mode
        self.canvas.config(cursor="crosshair")

    def start_crop(self, event):
        """Start cropping selection"""
        if not self.crop_mode:
            return
        
        # Allow clicking anywhere (including padding), but constrain start position to image boundaries
        self.crop_start_x = max(self.image_handler.image_x, 
                               min(event.x, self.image_handler.image_x + self.image_handler.display_width))
        self.crop_start_y = max(self.image_handler.image_y, 
                               min(event.y, self.image_handler.image_y + self.image_handler.display_height))
        
        # Remove any existing crop rectangle
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)

    def update_crop(self, event):
        """Update cropping selection rectangle"""
        if not self.crop_mode:
            return
        
        # Constrain current mouse position to image boundaries
        constrained_x = max(self.image_handler.image_x, 
                           min(event.x, self.image_handler.image_x + self.image_handler.display_width))
        constrained_y = max(self.image_handler.image_y, 
                           min(event.y, self.image_handler.image_y + self.image_handler.display_height))
            
        # Remove previous rectangle
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)
        
        # Draw new rectangle (using constrained coordinates)
        self.crop_rect_id = self.canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y, constrained_x, constrained_y,
            outline=self.colors['crop_border_color'], width=2
        )

    def end_crop(self, event, show_help_dialogs=True):
        """End cropping selection and process the crop"""
        if not self.crop_mode:
            return None
        
        # Constrain end position to image boundaries
        constrained_x = max(self.image_handler.image_x, 
                           min(event.x, self.image_handler.image_x + self.image_handler.display_width))
        constrained_y = max(self.image_handler.image_y, 
                           min(event.y, self.image_handler.image_y + self.image_handler.display_height))
            
        # Keep crosshair cursor
        self.canvas.config(cursor="crosshair")
        
        # Calculate crop coordinates relative to the original image
        crop_x1 = min(self.crop_start_x, constrained_x) - self.image_handler.image_x
        crop_y1 = min(self.crop_start_y, constrained_y) - self.image_handler.image_y
        crop_x2 = max(self.crop_start_x, constrained_x) - self.image_handler.image_x
        crop_y2 = max(self.crop_start_y, constrained_y) - self.image_handler.image_y
        
        # Ensure crop area is within image bounds
        crop_x1 = max(0, crop_x1)
        crop_y1 = max(0, crop_y1)
        crop_x2 = min(self.image_handler.display_width, crop_x2)
        crop_y2 = min(self.image_handler.display_height, crop_y2)
        
        # Check if valid crop area
        if crop_x2 - crop_x1 < 5 or crop_y2 - crop_y1 < 5:
            # Clean up rectangle and return
            if self.crop_rect_id:
                self.canvas.delete(self.crop_rect_id)
            return None
        
        # Scale coordinates to original image size
        scale_x = self.image_handler.original_image.width / self.image_handler.display_width
        scale_y = self.image_handler.original_image.height / self.image_handler.display_height
        
        orig_x1 = int(crop_x1 * scale_x)
        orig_y1 = int(crop_y1 * scale_y)
        orig_x2 = int(crop_x2 * scale_x)
        orig_y2 = int(crop_y2 * scale_y)
        
        # Crop the original image
        cropped_image = self.image_handler.original_image.crop((orig_x1, orig_y1, orig_x2, orig_y2))
        
        # Ask user what to do with the cropped image (adapt based on experience)
        should_save = True
        if show_help_dialogs:
            # Use native dialog with Yes/No buttons
            should_save = messagebox.askyesno("Crop Complete", "Crop completed! Would you like to save this cropped image?")
        
        # Clean up current crop rectangle but stay in crop mode
        if self.crop_rect_id:
            self.canvas.delete(self.crop_rect_id)
            self.crop_rect_id = None
            
        return cropped_image if should_save else None
