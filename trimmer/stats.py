# stats.py
from config.config import TOKEN_LIMIT

def print_stats(stats, tokens, output_size):
    print("Scan complete.\n")
    print("Raw Totals:")
    print(f"  Folders: {stats['raw_total_folders']}")
    print(f"  Files: {stats['raw_total_files']}")
    print("\nFiltered Totals (displayed in output):")
    print(f"  Folders: {stats['raw_total_folders']}")  # Folders aren't filtered further.
    print(f"  Files: {stats['filtered_total_files']}")
    print("Ignored:")
    print(f"  By type: {stats['ignored_by_type']}")
    print(f"  Icon files: {stats['ignored_icons']}")
    print(f"  Hidden files/folders: {stats.get('ignored_hidden', 0)}")
    
    # Display alias detection stats if available
    if 'detected_aliases' in stats:
        print(f"  Detected aliases: {stats['detected_aliases']}")
        
    print(f"Token Usage (tree format): {tokens} tokens ({round(100 * tokens / TOKEN_LIMIT, 1)}% of limit)")
    print(f"Output size: {output_size} bytes")