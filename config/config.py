# config/config.py
"""
Configuration settings for TreeTrimmer directory structure generator.
This module centralizes all configurable parameters.

To use custom local paths, create config/config_loc.py with:
    SOURCE_DIR = "/your/path/to/directory/to/scan"  
    OUTPUT_DIR = "/your/custom/output/path"  # Optional - defaults to "_out"
"""

# Try to import local configuration (not tracked in git)
try:
    from .config_loc import *
except ImportError:
    # Default fallback if no local config exists
    SOURCE_DIR = '/path/to/your/directory'

# If OUTPUT_DIR wasn't defined in local config, use default
if 'OUTPUT_DIR' not in locals():
    OUTPUT_DIR = '_out'

# Ignore file for file types to exclude
IGNORE_TYPES_FILE = 'config/ignore_types.txt'

# Formatting and behavior toggles
USE_TREE_FORMAT = True        # True = tree view (hierarchical), False = flat path list
COLLAPSE_CHAINS = True        # If True, collapse chains of single-child folders

# Token estimation (used for percentage of ChatGPT project limit)
TOKEN_LIMIT = 75000

# Toggle for eliminating macOS invisible icon files
ICON_ELIMINATION = True

# Toggle for ignoring hidden files/folders (those starting with a dot)
IGNORE_HIDDEN = True

# Maximum files to display per directory
MAX_FILES_DISPLAY = 0         # If exceeded, output summary instead
                              # Set to 0 to show only folders (no files)