"""
File-specific utilities for handling file types, aliases, and filtering.
"""
import os
import xattr
from config.config import ICON_ELIMINATION, IGNORE_HIDDEN, REPO_TYPES  # Add IGNORE_HIDDEN here

def is_alias(filepath):
    """
    Check if the given file is a macOS alias by examining extended attributes.
    
    This uses the FinderInfo extended attribute and checks for the alias bit (0x8000)
    in bytes 8-9 of the attribute data.
    """
    try:
        attrs = xattr.getxattr(filepath, "com.apple.FinderInfo")
        if len(attrs) >= 10 and int.from_bytes(attrs[8:10], "big") & 0x8000:
            return True
        return False
    except (KeyError, OSError):
        return False

def is_ignored_file(filename, ignore_types):
    """
    Check if a file should be ignored based on name or extension.
    
    Args:
        filename: The name of the file to check
        ignore_types: List of file types/extensions to ignore
        
    Returns:
        True if the file should be ignored, False otherwise
    """
    # Handle hidden files (starting with .)
    if IGNORE_HIDDEN and filename.startswith('.'):
        return True, "hidden"
        
    # Handle icon files
    if ICON_ELIMINATION and filename.lower().strip() in ["icon", "icon\r", "icon?"]:
        return True, "icon"
        
    # Check if filename matches an ignored file type
    if filename.lower() in ignore_types:
        return True, "type"
        
    # Check if extension matches an ignored file type
    ext = os.path.splitext(filename)[1].lower()
    if ext in ignore_types:
        return True, "type"
        
    return False, None

def is_repo(dirpath):
    """
    Check if a directory is a repository by looking for repository markers.
    
    Args:
        dirpath: Path to the directory to check
        
    Returns:
        tuple: (is_repo, repo_type) where is_repo is True if it's a repo,
               and repo_type is the type of repository (e.g., 'git', 'hg')
    """
    if not os.path.isdir(dirpath):
        return False, None
        
    for repo_type, markers in REPO_TYPES.items():
        for marker in markers:
            marker_path = os.path.join(dirpath, marker)
            if os.path.exists(marker_path):
                return True, repo_type
                
    return False, None