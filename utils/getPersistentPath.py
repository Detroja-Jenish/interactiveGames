import os
import sys

def getPersistentPath(filepath):
    if getattr(sys, 'frozen', False):  # If running in a PyInstaller bundle
        # Use user's home directory or a specific application data folder
        base_path = os.path.expanduser("~")  # Home directory
        app_dir = os.path.join(base_path, ".ClimbBall")  # Hidden folder for your app
    else:  # If running in development
        app_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Combine the base directory with the provided file path
    full_path = os.path.join(app_dir, filepath)
    
    # Ensure all parent directories in the file path exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Return the full path to the file
    return full_path
