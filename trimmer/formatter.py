# formatter.py
from .sorting import finder_sort_key  # Import the Finder sort key function

def format_tree_as_yaml(tree_lines):
    """Format tree lines as YAML."""
    yaml_header = [
        "# This YAML represents a trimmed, structured export of a macOS file system folder.",
        "# Files may be omitted due to TreeTrimmer config settings (e.g., MAX_FILES_DISPLAY = 0, ignored file types).",
        "# Folders shown with {} are not necessarily empty — they simply have no visible children in this export.",
        ""
    ]
    
    # Build a directory structure with folders and files
    structure = {}
    current_path = []
    
    for line in tree_lines:
        stripped = line.lstrip()
        indent_count = len(line) - len(stripped)
        level = indent_count // 2
        
        # Adjust current path based on indentation level
        current_path = current_path[:level]
        
        # Determine if it's a folder or file
        is_folder = stripped.endswith('/')
        item_name = stripped.rstrip('/') if is_folder else stripped
        
        # Navigate to current position in structure
        pos = structure
        for path_part in current_path:
            if isinstance(pos[path_part], dict):
                pos = pos[path_part]
            else:
                # If current position is a list, this means the folder
                # already has files, so we need to convert to a dict
                pos[path_part] = {}
                pos = pos[path_part]
        
        # Add the new item
        if is_folder:
            if item_name not in pos:
                pos[item_name] = {}
            current_path.append(item_name)
        else:
            if not isinstance(pos.get("files"), list):
                pos["files"] = []
            pos["files"].append(item_name)
    
    # Convert structure to YAML lines
    yaml_lines = []
    
    def build_yaml(obj, prefix="", level=0):
        indent = "  " * level
        
        if isinstance(obj, dict):
            if "files" in obj:
                files = obj.pop("files")
            else:
                files = None
                
            # Process folders first - USE FINDER SORT ORDER
            items = sorted(obj.items(), key=lambda x: finder_sort_key(x[0]))
            for name, contents in items:
                if contents:
                    yaml_lines.append(f"{indent}{prefix}{name}:")
                    build_yaml(contents, "", level + 1)
                else:
                    yaml_lines.append(f"{indent}{prefix}{name}: {{}}")
            
            # Add files as a list under the current level - USE FINDER SORT ORDER
            if files:
                yaml_lines.append(f"{indent}files:")
                for file in sorted(files, key=finder_sort_key):
                    yaml_lines.append(f"{indent}  - {file}")
    
    # Start with the root folder
    if structure:
        root_name = next(iter(structure))
        yaml_lines.append(f"{root_name}:")
        build_yaml(structure[root_name], "", 1)
    
    return '\n'.join(yaml_header + yaml_lines)

def format_tree_output(tree_lines):
    """Converts a list of tree-format lines into a YAML string."""
    return format_tree_as_yaml(tree_lines)

def format_flat_output(flat_lines):
    """Converts a list of flat path lines into a single string."""
    return '\n'.join(flat_lines)

def estimate_tokens(text):
    """Rough estimate: 1 token ≈ 4 characters."""
    return int(len(text) / 4.0)