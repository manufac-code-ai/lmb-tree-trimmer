#!/usr/bin/env python3

# Standard library imports
import os
import argparse
from datetime import datetime

# Local configuration imports
from config.config import (
    SOURCE_DIR,
    OUTPUT_DIR,
    USE_TREE_FORMAT,
)

# Package imports - organized by module
from trimmer.scanner import scan_directory, initial_count
from trimmer.formatter import format_tree_output, format_flat_output, estimate_tokens
from trimmer.stats import print_stats
from trimmer.utils import load_ignore_types, load_ignore_patterns  # Add load_ignore_patterns

def main():
    parser = argparse.ArgumentParser(description="Generate directory structure snapshots.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--repo', action='store_true',
                       help="Enable repository detection mode (folders only)")
    group.add_argument('--repo-files', action='store_true',
                       help="Enable repository detection with file display")
    args = parser.parse_args()

    # Derive internal flags
    enable_repo = args.repo or args.repo_files
    repo_show_files = args.repo_files

    # Load ignore types and patterns
    ignore_types = load_ignore_types()
    ignore_patterns = load_ignore_patterns()

    # Perform filtered scan
    tree_lines, flat_lines, filtered_stats = scan_directory(SOURCE_DIR, ignore_types, ignore_patterns, enable_repo, repo_show_files)

    # Format output
    tree_text = format_tree_output(tree_lines)
    flat_text = format_flat_output(flat_lines)
    selected_output = tree_text if USE_TREE_FORMAT else flat_text

    # Generate dynamic output filename
    timestamp = datetime.now().strftime("%y%m%d-%H%M")
    source_name = os.path.basename(os.path.normpath(SOURCE_DIR))
    output_filename = f"{timestamp} {source_name} structure_snapshot.yaml"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Write output to file
    with open(output_path, 'w') as f:
        f.write(selected_output)

    # Estimate token usage based on tree format
    tokens = estimate_tokens(tree_text)
    output_size = len(selected_output.encode('utf-8'))

    # Raw inventory (pre-filter baseline)
    raw_stats = initial_count(SOURCE_DIR)

    # Print raw inventory to console
    print()
    print("Raw Directory Inventory:")
    print(f"  Total Folders: {raw_stats['total_folders']}")
    print(f"  Total Files: {raw_stats['total_files']}")
    print(f"    - Image Files: {raw_stats['image_files']}")
    print(f"    - Markdown Files: {raw_stats['markdown_files']}")
    print(f"    - Icon Files: {raw_stats['icon_files']}")
    print()

    # Print filtered results and token usage
    print_stats(filtered_stats, tokens, output_size)

if __name__ == "__main__":
    main()