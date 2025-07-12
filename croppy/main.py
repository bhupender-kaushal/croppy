"""
Croppy - Main Application
A modern, cross-platform image viewer and cropper with adaptive theming
"""
import tkinter as tk
from tkinter import messagebox
import os

# Import custom modules
from .theme_manager import ThemeManager
from .ui_components import UIComponents
from .image_handler import ImageHandler
from .file_manager import FileManager
from .crop_manager import CropManager


class Croppy:
    """Main application class that coordinates all modules."""
    
    def __init__(self, master):
        self.master = master
        self.master.title("Croppy")
        
        # Initialize application state
        self.initialize_variables()
        
        # Initialize all managers
        self.theme_manager = ThemeManager()
        self.file_manager = FileManager()
        
        # Set up UI with temporary command handlers
        temp_handlers = self.get_temp_command_handlers()
        self.ui = UIComponents(master, self.theme_manager.colors, temp_handlers)
        
        # Initialize image and crop handlers
        self.image_handler = ImageHandler(self.ui.canvas, self.theme_manager.colors, self.theme_manager)
        self.crop_manager = CropManager(self.ui.canvas, self.theme_manager.colors, self.image_handler)
        
        # Update UI with final command handlers that include crop_manager
        self.ui.update_command_handlers(self.get_command_handlers())

    def initialize_variables(self):
        """Initialize all instance variables"""
        self.image_paths = []
        self.current_index = 0
        
        # User experience tracking
        self.images_processed = 0
        self.images_cropped = 0
        self.show_help_dialogs = True
        self.suppression_prompt_shown = False

    def get_temp_command_handlers(self):
        """Return temporary command handlers for initial UI setup"""
        return {
            'choose_directory': self.choose_directory,
            'show_previous': self.show_previous,
            'show_next': self.show_next,
            'crop_image': self.crop_image,
            'exit_crop_mode': self.exit_crop_mode,
            'start_crop': lambda e: None,  # Temporary placeholder
            'update_crop': lambda e: None,  # Temporary placeholder
            'end_crop': self.end_crop,
            'on_mouse_motion': lambda e: None,  # Temporary placeholder
            'resize_image': self.resize_image,
            'handle_escape': self.handle_escape,
            'key_next_image': self.key_next_image,
            'key_previous_image': self.key_previous_image
        }

    def get_command_handlers(self):
        """Return dictionary of command handlers for UI components"""
        return {
            'choose_directory': self.choose_directory,
            'show_previous': self.show_previous,
            'show_next': self.show_next,
            'crop_image': self.crop_image,
            'exit_crop_mode': self.exit_crop_mode,
            'start_crop': self.crop_manager.start_crop,
            'update_crop': self.crop_manager.update_crop,
            'end_crop': self.end_crop,
            'on_mouse_motion': self.crop_manager.on_mouse_motion,
            'resize_image': self.resize_image,
            'handle_escape': self.handle_escape,
            'key_next_image': self.key_next_image,
            'key_previous_image': self.key_previous_image
        }

    # =====================================
    # DIRECTORY AND FILE MANAGEMENT
    # =====================================

    def choose_directory(self):
        """Handle directory selection and setup new project"""
        image_files = self.file_manager.choose_directory()
        
        if image_files:
            self.reset_project_state()
            self.image_paths = image_files
            self.current_index = 0
            
            # Exit crop mode if active
            if self.crop_manager.crop_mode:
                self.exit_crop_mode()
            
            # Show help and load first image
            self.show_initial_help_dialog()
            self.load_first_image()
            self.enable_navigation_buttons()
        else:
            self.handle_no_images()

    def reset_project_state(self):
        """Reset state for new project"""
        self.images_processed = 0
        self.images_cropped = 0
        self.show_help_dialogs = True
        self.suppression_prompt_shown = False

    def load_first_image(self):
        """Load the first image without counting as processed"""
        self.image_handler.load_image_without_counting(
            self.image_paths[self.current_index], 
            self.crop_manager.crop_mode, 
            self.update_title
        )

    def enable_navigation_buttons(self):
        """Enable all navigation and action buttons"""
        self.ui.prev_button.config(state=tk.NORMAL)
        self.ui.next_button.config(state=tk.NORMAL)
        self.ui.crop_button.config(state=tk.NORMAL)

    def handle_no_images(self):
        """Handle case when no images found or selection cancelled"""
        self.image_handler.show_no_images_message()
        self.ui.prev_button.config(state=tk.DISABLED)
        self.ui.next_button.config(state=tk.DISABLED)
        self.ui.crop_button.config(state=tk.DISABLED)

    # =====================================
    # USER EXPERIENCE METHODS
    # =====================================

    def show_initial_help_dialog(self):
        """Show initial help dialog for new users"""
        if self.show_help_dialogs:
            messagebox.showinfo("Welcome to Croppy", 
                               "Welcome to Croppy!\n\n"
                               "• Click 📁 to select a folder with images\n"
                               "• Use ← → buttons or arrow keys to navigate\n"
                               "• Click ✂️ to enable crop mode\n"
                               "• In crop mode: click and drag to select areas\n"
                               "• Save cropped images to your chosen location\n\n"
                               "Ready to start cropping!")

    def check_suppression_prompt(self):
        """Check if user wants to disable help dialogs"""
        if (self.images_cropped >= 3 and self.show_help_dialogs and 
            not self.suppression_prompt_shown):
            self.suppression_prompt_shown = True
            choice = messagebox.askyesno(
                "Experience Mode", 
                f"You've successfully cropped {self.images_cropped} images! "
                "Would you like to disable help dialogs for faster workflow?\n\n"
                "• Yes = Disable dialogs (use current directory by default)\n"
                "• No = Keep showing dialogs",
                icon='question'
            )
            if choice:
                self.show_help_dialogs = False
                messagebox.showinfo("Experience Mode", 
                                  "Help dialogs disabled. Cropped images will be "
                                  "saved to the current directory by default.")

    # =====================================
    # NAVIGATION METHODS
    # =====================================

    def show_previous(self):
        """Navigate to previous image"""
        if not self.image_paths:
            return
            
        if self.current_index == 0:
            self.check_directory_traversal_complete("previous")
        else:
            self.current_index -= 1
            self.load_current_image()

    def show_next(self):
        """Navigate to next image"""
        if not self.image_paths:
            return
            
        if self.current_index == len(self.image_paths) - 1:
            self.check_directory_traversal_complete("next")
        else:
            self.current_index += 1
            self.load_current_image()

    def check_directory_traversal_complete(self, direction):
        """Handle end/beginning of directory traversal"""
        messages = {
            "next": ("You've reached the end of the directory. "
                    "Would you like to start over from the beginning?", 
                    "End of Directory"),
            "previous": ("You're at the beginning of the directory. "
                        "Would you like to go to the last image?", 
                        "Beginning of Directory")
        }
        
        message, title = messages[direction]
        choice = messagebox.askyesno(title, message)
        
        if choice:
            self.current_index = 0 if direction == "next" else len(self.image_paths) - 1
            self.load_current_image()

    def load_current_image(self):
        """Load current image and update processed count"""
        self.image_handler.load_image(
            self.image_paths[self.current_index], 
            self.crop_manager.crop_mode, 
            self.update_title
        )
        self.images_processed += 1

    def auto_move_to_next(self):
        """Auto-advance to next image after cropping"""
        if self.current_index == len(self.image_paths) - 1:
            self.check_directory_traversal_complete("next")
        else:
            self.current_index += 1
            self.load_current_image()

    # =====================================
    # EVENT HANDLING METHODS
    # =====================================

    def key_next_image(self, event):
        """Handle right/down arrow keys"""
        if self.image_paths and not self.image_handler.loading:
            self.show_next()
        return "break"

    def key_previous_image(self, event):
        """Handle left/up arrow keys"""
        if self.image_paths and not self.image_handler.loading:
            self.show_previous()
        return "break"

    def handle_escape(self, event):
        """Handle escape key - exit fullscreen if active"""
        if self.master.attributes('-fullscreen'):
            self.master.attributes('-fullscreen', False)
        return "break"

    def resize_image(self):
        """Handle window resize events"""
        if self.image_paths:
            self.image_handler.load_image_without_counting(
                self.image_paths[self.current_index], 
                self.crop_manager.crop_mode, 
                self.update_title
            )

    # =====================================
    # CROP FUNCTIONALITY METHODS
    # =====================================

    def crop_image(self):
        """Handle crop mode activation"""
        if not self.image_paths:
            return
        
        # Setup save directory through file manager
        if not self.file_manager.setup_save_directory(self.show_help_dialogs):
            return
        
        # Enter crop mode
        self.crop_manager.enter_crop_mode(self.ui, self.show_help_dialogs)
        self.update_title(self.image_paths[self.current_index], crop_mode=True)

    def exit_crop_mode(self):
        """Exit crop mode"""
        current_image = self.image_paths[self.current_index] if self.image_paths else None
        self.crop_manager.exit_crop_mode(self.ui, self.update_title, current_image)

    def end_crop(self, event):
        """Handle crop completion and saving"""
        cropped_image = self.crop_manager.end_crop(event, self.show_help_dialogs)
        
        if cropped_image:
            self.save_and_advance(cropped_image)

    def save_and_advance(self, cropped_image):
        """Save cropped image and advance to next"""
        filename = self.file_manager.save_cropped_image(
            cropped_image, 
            self.image_paths[self.current_index]
        )
        
        if filename:
            self.images_cropped += 1
            self.check_suppression_prompt()
            self.show_save_success(filename)
            self.auto_move_to_next()

    def show_save_success(self, filename):
        """Show save success message"""
        if self.show_help_dialogs:
            messagebox.showinfo("Success", f"Cropped image saved as:\n{filename}")
        else:
            self.master.title(f"Croppy - Saved: {filename}")
            self.master.after(1000, lambda: self.update_title(
                self.image_paths[self.current_index], 
                self.crop_manager.crop_mode
            ))

    # =====================================
    # UTILITY METHODS
    # =====================================

    def update_title(self, image_path, crop_mode=False):
        """Update window title with current image info"""
        filename = os.path.basename(image_path)
        base_title = f"Croppy - {filename} ({self.current_index + 1}/{len(self.image_paths)})"
        
        if crop_mode:
            self.master.title(f"Croppy - CROP MODE ACTIVE - {filename} ({self.current_index + 1}/{len(self.image_paths)})")
        else:
            self.master.title(base_title)


def main():
    """Main function to initialize and run Croppy"""
    root = tk.Tk()
    app = Croppy(root)
    root.mainloop()


if __name__ == '__main__':
    main()