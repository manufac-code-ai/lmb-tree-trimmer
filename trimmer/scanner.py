"""
Core scanning functionality for generating directory structures.
"""
import os

# Import from other modules
from .filesystem import process_directory
from .utils import initial_count as utils_initial_count

def scan_directory(source_dir, ignore_types, ignore_patterns, enable_repo=False):  # Add enable_repo parameter
    """
    Scan a directory and return formatted tree and flat views.
    
    Args:
        source: Source directory path
        ignore_types: List of file types/extensions to ignore
        
    Returns:
        Tuple of (tree_lines, flat_lines, stats)
    """
    stats = {}
    
    # Process the directory structure
    tree_lines, flat_lines, stats = process_directory(source_dir, ignore_types, ignore_patterns, enable_repo=enable_repo)
    
    # Return both formats and stats
    return tree_lines, flat_lines, stats


def initial_count(source_dir):
    """
    Get initial file and folder counts for the specified directory.
    
    Args:
        source_dir: Directory to count
        
    Returns:
        Dictionary with raw counts
    """
    return utils_initial_count(source_dir)