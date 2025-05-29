# stats.py
from config.config import TOKEN_LIMIT

def print_stats(stats, tokens, output_size):
    print("Scan complete.\n")
    print("Raw Totals:")
    print(f"  Folders: {stats['raw_total_folders']}")
    print(f"  Files: {stats['raw_total_files']}")
    print("\nFiltered Totals (displayed in output):")
    print(f"  Folders: {stats['raw_total_folders']}")
    print(f"  Files: {stats.get('filtered_files', 'N/A')}")
    print("Ignored:")
    # Add safe access to prevent KeyError
    if 'ignored_by_type' in stats:
        print(f"  By type: {stats['ignored_by_type']}")
    else:
        print(f"  By type: N/A")
    
    print(f"\nEstimated tokens: {tokens:,}")
    print(f"Output size: {output_size:,} bytes")
    print(f"Token usage: {(tokens/TOKEN_LIMIT)*100:.1f}% of {TOKEN_LIMIT:,} limit")