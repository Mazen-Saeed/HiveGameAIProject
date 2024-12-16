import os
import sys

def resource_path(relative_path):
    """
    Get the absolute path to resource, works for PyInstaller executables.
    """
    if getattr(sys, 'frozen', False):  # Running as a bundled executable
        base_path = sys._MEIPASS
    else:  # Running as a normal script
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Add Src directory to the Python path
sys.path.append(resource_path(".."))