"""
File system utilities for directory traversal and path manipulation.
Focused on directory structure generation.
"""
import os
from config.config import COLLAPSE_CHAINS, MAX_FILES_DISPLAY, IGNORE_HIDDEN, MAX_SCAN_DEPTH, REPO_TYPES

# Import functionality from other modules
from .sorting import finder_sort_key
from .files import is_alias, is_ignored_file, is_repo, is_repo_archive

def collapse_dirs(path, ignore_types, chain_so_far=None):
    """Collapse chains of single-folder directories."""
    if chain_so_far is None:
        chain_so_far = []

    # Skip hidden directories if IGNORE_HIDDEN is set
    basename = os.path.basename(path)
    if IGNORE_HIDDEN and basename.startswith('.'):
        # Return the path so far without the hidden directory
        if chain_so_far:
            collapsed = "/".join(chain_so_far)
            return collapsed, os.path.dirname(path)
        else:
            # If this is the first directory and it's hidden, return empty
            return "", path

    try:
        entries = os.listdir(path)
    except PermissionError:
        entries = []

    # Count subdirectories and files.
    subdirs = [d for d in entries if os.path.isdir(os.path.join(path, d))]
    files = [f for f in entries if os.path.isfile(os.path.join(path, f))]
    
    # Check each file against ignore rules
    non_ignored_files = []
    for f in files:
        should_ignore, _ = is_ignored_file(f, ignore_types)
        if not should_ignore:
            non_ignored_files.append(f)

    # If this directory has exactly one subdirectory and no non-ignored files, recurse.
    if len(subdirs) == 1 and len(non_ignored_files) == 0:
        subdir = os.path.join(path, subdirs[0])
        chain_so_far.append(os.path.basename(path))
        return collapse_dirs(subdir, ignore_types, chain_so_far)

    # If we got here, we hit a directory that either has multiple subdirs or has files.
    # Append the current directory to the chain.
    chain_so_far.append(os.path.basename(path))
    
    # Format the collapsed path
    collapsed = "/".join(chain_so_far)
    return collapsed, path


def process_directory(path, ignore_types, ignore_patterns, current_indent=0, parent_path="", enable_repo=False, inside_repo=False):  # Add enable_repo and inside_repo parameters
    """Process a directory and return formatted lines for tree output."""
    # Get the directory name
    basename = os.path.basename(path)
    
    # Skip hidden directories if IGNORE_HIDDEN is set
    if IGNORE_HIDDEN and basename.startswith('.'):
        return [], [], {"ignored_hidden": 1}
    
    lines = []
    flat_lines = []
    norm_path = os.path.normpath(path)
    
    # Update raw folder count
    stats = {"raw_total_folders": 1}
    
    # Process collapsing if enabled.
    if COLLAPSE_CHAINS:
        collapsed_label, final_dir = collapse_dirs(path, ignore_types)
        indent = '  ' * current_indent
        if os.path.normpath(final_dir) != norm_path:
            lines.append(f"{indent}{collapsed_label}/")
            flat_lines.append(os.path.normpath(final_dir) + '/')
            path = final_dir  # Continue from the collapsed end.
        else:
            if not inside_repo:
                folder_name = os.path.basename(path)
                lines.append(f"{indent}{folder_name}/")
                flat_lines.append(norm_path + '/')
    else:
        indent = '  ' * current_indent
        if not inside_repo:
            folder_name = os.path.basename(path)
            lines.append(f"{indent}{folder_name}/")
            flat_lines.append(norm_path + '/')

    # Process files in this directory.
    try:
        entries = sorted(os.listdir(path), key=finder_sort_key)
    except PermissionError:
        entries = []

    # Create separate lists for regular files, aliases, and repo archives
    regular_files = []
    alias_files = []
    repo_archive_files = []

    for entry in entries:
        full_entry = os.path.join(path, entry)
        if os.path.isfile(full_entry):
            stats['raw_total_files'] = stats.get('raw_total_files', 0) + 1

            # Check if file should be ignored
            should_ignore, ignore_reason = is_ignored_file(entry, ignore_types)
            if should_ignore:
                if ignore_reason == "icon":
                    stats['ignored_icons'] = stats.get('ignored_icons', 0) + 1
                elif ignore_reason == "type":
                    stats['ignored_by_type'] = stats.get('ignored_by_type', 0) + 1
                continue

            # Check for repo archives when repo detection is enabled
            # This happens BEFORE alias detection to prioritize repo status
            if enable_repo and entry.lower().endswith('.zip'):
                is_archive, repo_type = is_repo_archive(full_entry)
                if is_archive:
                    # Mark as repo archive with .repo.zip suffix
                    repo_archive_name = entry + ".repo.zip"
                    repo_archive_files.append(repo_archive_name)

                    # Update statistics
                    stats['repo_archives_detected'] = stats.get('repo_archives_detected', 0) + 1

                    # Skip further processing (don't check as alias or regular file)
                    continue

            # Check if the file is a macOS alias
            if is_alias(full_entry):
                alias_name = entry + ".alias"
                alias_files.append(alias_name)
                # Count detected aliases in our stats
                stats['detected_aliases'] = stats.get('detected_aliases', 0) + 1
            else:
                # Regular non-alias file
                regular_files.append(entry)
    
    # Always display all aliases (they're important navigation elements)
    for alias in alias_files:
        lines.append(f"{indent}  {alias}")
        # For flat_lines, we don't want to add the .alias suffix
        original_name = alias.replace('.alias', '')
        flat_lines.append(os.path.normpath(os.path.join(path, original_name)))
        stats['filtered_total_files'] = stats.get('filtered_total_files', 0) + 1

    # Always display all repo archives (like aliases, they're important markers)
    # Only shown when enable_repo=True (controlled by --repo flag)
    for repo_archive in repo_archive_files:
        lines.append(f"{indent}  {repo_archive}")
        # For flat_lines, strip the .repo.zip suffix to show original filename
        original_name = repo_archive.replace('.repo.zip', '')
        flat_lines.append(os.path.normpath(os.path.join(path, original_name)))
        stats['filtered_total_files'] = stats.get('filtered_total_files', 0) + 1

    # Only apply MAX_FILES_DISPLAY limit to regular files
    if MAX_FILES_DISPLAY == 0:
        # If MAX_FILES_DISPLAY is 0, don't show regular files at all (folders-only mode)
        pass
    elif len(regular_files) > MAX_FILES_DISPLAY:
        # Show summary for regular files if they exceed the limit
        lines.append(f"{indent}  [omitted {len(regular_files)} files]")
        stats['filtered_total_files'] = stats.get('filtered_total_files', 0) + len(regular_files)
    else:
        # Show all regular files if under the limit
        for entry in regular_files:
            lines.append(f"{indent}  {entry}")
            flat_lines.append(os.path.normpath(os.path.join(path, entry)))
            stats['filtered_total_files'] = stats.get('filtered_total_files', 0) + 1

    # Process subdirectories - ADD DEPTH CHECK HERE
    if MAX_SCAN_DEPTH == 0 or current_indent < MAX_SCAN_DEPTH:
        try:
            subdirs = sorted([d for d in entries if os.path.isdir(os.path.join(path, d)) and 
                             not (IGNORE_HIDDEN and d.startswith('.'))], 
                             key=finder_sort_key)
        except PermissionError:
            subdirs = []
        for sub in subdirs:
            sub_path = os.path.join(path, sub)
            
            # Check if repo detection is enabled and this is a repository
            if enable_repo:
                is_repository, repo_type = is_repo(sub_path)
                if is_repository:
                    # Mark as repository and continue recursing to find nested repos
                    repo_name = f"{sub}.repo"
                    lines.append(f"{indent}  {repo_name}/")
                    flat_lines.append(os.path.normpath(sub_path) + '/')
                    stats['repos_detected'] = stats.get('repos_detected', 0) + 1
                    
                    # Recurse into the repo to detect nested repos, with inside_repo=True
                    sub_lines, sub_flat, sub_stats = process_directory(sub_path, ignore_types, ignore_patterns, current_indent + 1, path, enable_repo, inside_repo=True)
                    lines.extend(sub_lines)
                    flat_lines.extend(sub_flat)
                    for key, value in sub_stats.items():
                        stats[key] = stats.get(key, 0) + value
                    continue
            
            # Not a repo (or repo detection disabled), check ignore patterns
            if any(pattern in sub for pattern in ignore_patterns):
                continue  # Skip this directory
            
            # Recurse normally
            sub_lines, sub_flat, sub_stats = process_directory(sub_path, ignore_types, ignore_patterns, current_indent + 1, path, enable_repo, inside_repo)
            lines.extend(sub_lines)
            flat_lines.extend(sub_flat)
            for key, value in sub_stats.items():
                stats[key] = stats.get(key, 0) + value
    return lines, flat_lines, stats