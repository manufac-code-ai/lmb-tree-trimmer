"""
General utility functions for the folder structure scanner.
"""
import os
from config.config import ICON_ELIMINATION, IGNORE_TYPES_FILE, IGNORE_PATTERNS_FILE  # Add IGNORE_PATTERNS_FILE

def load_ignore_types():
    """
    Load ignore types file from disk.
    
    Returns:
        List of file types/extensions to ignore
    """
    ignore_types = []
    if os.path.exists(IGNORE_TYPES_FILE):
        with open(IGNORE_TYPES_FILE, 'r') as f:
            for line in f:
                line = line.strip().lower()
                if line and not line.startswith('#'):  # Changed from '//' to '#'
                    ignore_types.append(line)
    
    return ignore_types

def load_ignore_patterns():
    """Load ignore patterns file from disk."""
    ignore_patterns = []
    if os.path.exists(IGNORE_PATTERNS_FILE):
        with open(IGNORE_PATTERNS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    return ignore_patterns

def initial_count(source_dir):
    """Perform a raw count of files and folders, respecting ignore patterns."""
    from .utils import load_ignore_patterns  # Import here to avoid circular imports
    ignore_patterns = load_ignore_patterns()
    
    stats = {
        'total_folders': 0,
        'total_files': 0,
        'image_files': 0,
        'markdown_files': 0,
        'icon_files': 0
    }

    for root, dirs, files in os.walk(source_dir):
        # Remove ignored directories from dirs list (modifies os.walk behavior)
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in ignore_patterns)]
        
        stats['total_folders'] += len(dirs)
        stats['total_files'] += len(files)
        for file in files:
            lower_name = file.lower()
            # Count image files
            if lower_name.endswith(('.jpg', '.jpeg', '.png', '.gif', '.heic')):
                stats['image_files'] += 1
            # Count markdown files
            elif lower_name.endswith('.md'):
                stats['markdown_files'] += 1
            # Count icon files
            elif ICON_ELIMINATION and lower_name.strip() in ["icon", "icon\r", "icon?"]:
                stats['icon_files'] += 1

    return stats