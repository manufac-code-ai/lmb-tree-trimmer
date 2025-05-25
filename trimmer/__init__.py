"""
Folder Structure to Text (LLM Optimized)

A package for generating token-efficient directory structure snapshots
optimized for use with large language models.
"""

# Import and re-export the public API
from .scanner import scan_directory, initial_count
from .formatter import format_tree_output, format_flat_output, estimate_tokens
from .stats import print_stats
from .utils import load_ignore_types
from .files import is_alias, is_ignored_file
from .sorting import finder_sort_key

# Define what gets imported with "from folderstructure import *"
__all__ = [
    'scan_directory', 
    'initial_count',
    'format_tree_output', 
    'format_flat_output', 
    'estimate_tokens',
    'print_stats',
    'load_ignore_types',
    'is_alias',
    'is_ignored_file',
    'finder_sort_key',
]

# Package metadata
__version__ = '0.1.0'
__author__ = 'manufactured'