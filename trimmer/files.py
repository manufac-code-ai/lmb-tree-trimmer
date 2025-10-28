"""
File-specific utilities for handling file types, aliases, and filtering.
"""
import os
import zipfile
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

def is_repo_archive(filepath):
    """
    Check if a zip archive contains a repository by scanning for repo markers.

    This function inspects the contents of a zip archive without extracting files,
    looking for version control system markers (e.g., .git, .hg, .svn) that indicate
    the archive contains a repository.

    Args:
        filepath: Absolute path to potential zip archive file

    Returns:
        tuple: (is_repo_archive, repo_type)
            - is_repo_archive (bool): True if archive contains repository markers
            - repo_type (str|None): Type of repository ('git', 'mercurial', etc.) or None

    Examples:
        >>> is_repo_archive('/path/to/my-project.zip')
        (True, 'git')

        >>> is_repo_archive('/path/to/regular-archive.zip')
        (False, None)

    Notes:
        - Only reads archive metadata (namelist), does not extract files
        - Checks for markers at root level or within first-level folders
        - Returns (False, None) for corrupted zips or permission errors
        - Uses REPO_TYPES config for marker definitions
    """
    # Validate file extension - quick filter before attempting zip operations
    if not filepath.lower().endswith('.zip'):
        return False, None

    try:
        # Open zip and read file list (reads only central directory, not file contents)
        with zipfile.ZipFile(filepath, 'r') as zf:
            namelist = zf.namelist()

            # Check for repository markers in same order as is_repo()
            for repo_type, markers in REPO_TYPES.items():
                for marker in markers:
                    # Search for marker in archive paths
                    # Examples that should match:
                    #   - ".git/" (root-level marker)
                    #   - ".git/config" (marker with contents)
                    #   - "my-repo/.git/" (marker in subfolder)
                    #   - "my-repo/.git/HEAD" (marker in subfolder with contents)
                    for entry in namelist:
                        # Split path into components
                        parts = entry.split('/')

                        # Check if marker appears in path components
                        # This handles both "marker/" and "folder/marker/" cases
                        if marker in parts:
                            return True, repo_type

            # No markers found
            return False, None

    except zipfile.BadZipFile:
        # File is not a valid zip or is corrupted
        return False, None
    except OSError:
        # File access error (doesn't exist, permission denied, etc.)
        return False, None
    except PermissionError:
        # Explicit permission denial
        return False, None