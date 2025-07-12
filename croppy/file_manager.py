"""
File Manager - Handles file operations and directory management
Cross-platform file and directory handling with proper path separators
"""
import os
import platform
from tkinter import filedialog, messagebox


class FileManager:
    def __init__(self):
        self.input_dir = None
        self.save_directory = None
        self.destination_set = False
        self.platform = platform.system().lower()
        
    def choose_directory(self):
        """Open directory selection dialog with platform-specific options"""
        dialog_options = self.get_dialog_options()
        selected_dir = filedialog.askdirectory(**dialog_options)
        
        if selected_dir:
            # Normalize path for current platform
            self.input_dir = os.path.normpath(selected_dir)
            # Reset destination for new project
            self.destination_set = False
            self.save_directory = None
            return self.get_image_files()
        return []
    
    def get_dialog_options(self):
        """Get platform-specific dialog options"""
        options = {
            'title': 'Select folder containing images'
        }
        
        if self.platform == "windows":
            options.update({
                'mustexist': True
            })
        elif self.platform == "darwin":
            # macOS specific options
            options.update({
                'title': 'Choose Image Folder'
            })
        
        return options
    
    def get_image_files(self):
        """Get list of image files from the selected directory with better extension handling"""
        if not self.input_dir:
            return []
        
        # More comprehensive image extensions
        image_extensions = (
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', 
            '.webp', '.ico', '.ppm', '.pgm', '.pbm'
        )
        image_files = []
        
        try:
            for filename in os.listdir(self.input_dir):
                if filename.lower().endswith(image_extensions):
                    full_path = os.path.join(self.input_dir, filename)
                    # Ensure the file exists and is readable
                    if os.path.isfile(full_path) and os.access(full_path, os.R_OK):
                        image_files.append(full_path)
        except (PermissionError, OSError) as e:
            messagebox.showerror("Directory Error", f"Cannot access directory:\n{str(e)}")
            return []
        except Exception as e:
            print(f"Error reading directory: {e}")
            messagebox.showerror("Error", f"Error reading directory:\n{str(e)}")
            return []
            
        # Sort files naturally (handle numbers in filenames properly)
        image_files.sort(key=self.natural_sort_key)
        return image_files
    
    def natural_sort_key(self, filename):
        """Create a natural sorting key that handles numbers in filenames properly"""
        import re
        # Extract numbers and text separately for natural sorting
        parts = re.split(r'(\d+)', os.path.basename(filename).lower())
        return [int(part) if part.isdigit() else part for part in parts]
    
    def setup_save_directory(self, show_help_dialogs=True):
        """Setup save directory for cropped images"""
        if not show_help_dialogs:
            # For experienced users, use cropped subfolder by default if not set
            if not self.destination_set:
                cropped_folder = os.path.join(self.input_dir, "cropped")
                try:
                    os.makedirs(cropped_folder, exist_ok=True)
                    self.save_directory = cropped_folder
                    self.destination_set = True
                    return True
                except Exception as e:
                    messagebox.showerror("Error", f"Could not create cropped folder:\n{str(e)}")
                    return False
        else:
            # For new users, ask for destination only if not already set for this project
            if not self.destination_set:
                # Default to cropped subfolder in the input directory
                default_save_dir = os.path.join(self.input_dir, "cropped")
                current_dir_name = os.path.basename(self.input_dir)
                
                result = messagebox.askyesnocancel(
                    "Save Location", 
                    f"Cropped images will be saved to: {current_dir_name}/cropped\n\n• OK (Yes) = Save to 'cropped' subfolder in current directory\n• Change (No) = Choose different location\n• Cancel = Cancel crop operation\n\nNote: This choice will be remembered for all images in this project.",
                    icon='question'
                )
                
                if result is None:  # Cancel was pressed
                    return False
                elif result:  # "Yes" (OK) was pressed - use cropped subfolder in current directory
                    try:
                        os.makedirs(default_save_dir, exist_ok=True)
                        self.save_directory = default_save_dir
                        self.destination_set = True
                        return True
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not create cropped folder:\n{str(e)}")
                        return False
                else:  # "No" (Change) was pressed - choose folder
                    selected_dir = filedialog.askdirectory(title="Choose directory to save cropped images for this project")
                    if not selected_dir:  # User cancelled folder selection
                        return False
                    self.save_directory = selected_dir
                    self.destination_set = True
                    return True
            # If destination already set, show current save location with option to change
            elif show_help_dialogs:
                # Show the current save location for better readability
                if self.save_directory.startswith(self.input_dir):
                    # If it's a subfolder of input directory, show relative path
                    relative_path = os.path.relpath(self.save_directory, self.input_dir)
                    if relative_path == ".":
                        save_location_display = f"{os.path.basename(self.input_dir)} (current directory)"
                    else:
                        save_location_display = f"{os.path.basename(self.input_dir)}/{relative_path}"
                else:
                    # If it's a different directory, show just the folder name
                    save_location_display = os.path.basename(self.save_directory)
                
                result = messagebox.askyesno(
                    "Save Location Confirmation",
                    f"Cropped images will be saved to: {save_location_display}\n\n• OK (Yes) = Continue with this location\n• Change (No) = Choose different location"
                )
                
                if not result:  # User wants to change location
                    selected_dir = filedialog.askdirectory(title="Choose directory to save cropped images for this project")
                    if not selected_dir:  # User cancelled folder selection
                        return False
                    self.save_directory = selected_dir
                    return True
        
        return True
    
    def save_cropped_image(self, cropped_image, original_filename):
        """Save the cropped image to the selected directory"""
        try:
            # Generate filename - same name, no timestamp (will overwrite)
            name_without_ext = os.path.splitext(os.path.basename(original_filename))[0]
            extension = os.path.splitext(os.path.basename(original_filename))[1]
            
            # Use consistent filename - no timestamp (overwrites previous crops)
            new_filename = f"{name_without_ext}_cropped{extension}"
            
            save_path = os.path.join(self.save_directory, new_filename)
            cropped_image.save(save_path)
            
            return new_filename
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save cropped image:\n{str(e)}")
            return None
