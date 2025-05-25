"""
Sorting utilities that mimic macOS Finder's sorting behavior.
"""
import locale

# Set the locale to match macOS default
try:
    locale.setlocale(locale.LC_COLLATE, 'en_US.UTF-8')
except locale.Error:
    # Fallback if the specific locale is not available
    try:
        locale.setlocale(locale.LC_COLLATE, '')  # Use system default locale
    except locale.Error:
        pass  # If all fails, Python's default sort will be used

def finder_sort_key(name):
    """
    Create a sort key that mimics macOS Finder's sorting behavior.
    
    This ensures special characters like brackets and underscores appear first
    and in the correct macOS Finder order.
    """
    # Guard against None values
    if name is None:
        return (3, "")
    
    # Handle empty strings
    if not name:
        return (0, "")
    
    first_char = name[0]
    
    # Special characters in macOS Finder order (higher priority characters first)
    # This order matters and follows Finder's sorting
    finder_char_order = {
        '_': 10,  # Underscore comes first in Finder
        '[': 11,  # Square bracket comes after underscore
        ']': 12,
        '.': 13,
        '-': 14,
        '~': 15,
        # Other special characters with lower priority
        '`': 20, '!': 21, '@': 22, '#': 23, '$': 24, '%': 25, '^': 26, '&': 27, 
        '*': 28, '(': 29, ')': 30, '+': 31, '{': 32, '}': 33, '|': 34, ':': 35,
        '"': 36, '<': 37, '>': 38, '?': 39, '\\': 40, ';': 41, '\'': 42, ',': 43, '/': 44, ' ': 45
    }
    
    # If it's a special character, sort by its position in the Finder order
    if first_char in finder_char_order:
        return (0, finder_char_order[first_char], name.lower())
    
    # Numbers sort next
    if first_char.isdigit():
        return (1, 0, name.lower())
    
    # Everything else (primarily letters) sorts last
    return (2, 0, name.lower())