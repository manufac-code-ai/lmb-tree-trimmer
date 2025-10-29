# LMbridge Tree Trimmer - Architecture Overview

## Overview

LMbridge Tree Trimmer is a Python-based directory structure visualization tool designed to generate token-efficient YAML snapshots of file systems for Large Language Model (LLM) processing. It transforms complex directory hierarchies into structured, machine-readable output while filtering out unnecessary files and directories.

## Core Architecture

### High-Level Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   treetrim.py   │───▶│   trimmer/      │───▶│   _output/       │
│   (Entry Point) │    │   (Core Logic)  │    │   (Output)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   config/       │
                       │   (Configuration│
                       └─────────────────┘
```

### Package Structure

```
lmb-tree-trimmer/
├── treetrim.py              # Application entry point
├── trimmer/                 # Core processing package
│   ├── __init__.py         # Package initialization
│   ├── scanner.py          # Directory scanning orchestration
│   ├── filesystem.py       # Directory traversal and processing
│   ├── files.py            # File type detection and filtering
│   ├── formatter.py        # YAML output formatting
│   ├── sorter.py           # macOS Finder-compatible sorting
│   ├── stats.py            # Processing statistics and reporting
│   └── utils.py            # Configuration loading utilities
├── config/                  # Configuration files
│   ├── config.py           # Main application settings
│   ├── config_loc.py       # Local user-specific paths
│   ├── ignore_types.conf   # File extension filters
│   └── ignore_pat.conf     # Directory pattern filters
├── _docs/                   # Documentation
├── _output/                 # Generated snapshots
└── requirements.txt         # Python dependencies
```

## Data Flow

### Processing Pipeline

1. **Initialization**
   - Load configuration from `config/config.py` and `config/config_loc.py`
   - Load ignore patterns from `config/ignore_types.conf` and `config/ignore_pat.conf`
   - Parse command-line arguments (`--repo` or `--repo-files` flags, mutually exclusive)
   - Derive internal flags: `enable_repo` and `repo_show_files`

2. **Directory Scanning**
   - `treetrim.py` calls `scanner.scan_directory()`
   - `scanner.py` invokes `filesystem.process_directory()` recursively
   - Depth-first traversal with configurable limits

3. **File Processing**
   - `filesystem.py` processes each directory entry
   - `files.py` handles file type detection and alias identification
   - `files.py` detects repositories in zip archives when `enable_repo=True`
   - Determine `effective_max_files` based on mode:
     - `enable_repo=True` and `repo_show_files=False` → force 0 (folders-only)
     - Otherwise → use `MAX_FILES_DISPLAY` configuration
   - Apply filtering based on ignore patterns and configuration

4. **Repository Detection (Optional)**
   - When `enable_repo=True`, detect VCS directories and archives
   - Mark directory repositories with `.repo` suffix
   - Mark archive repositories with `.repo.zip` suffix
   - Skip repository internals for clean output
   - File visibility controlled by `repo_show_files` parameter

5. **Output Generation**
   - `formatter.py` converts processed data to YAML
   - `stats.py` calculates and reports processing metrics
   - Determine output extension based on `USE_TXT_EXTENSION` config
   - Write timestamped file to `_output/` directory (`.txt` or `.yaml`)

### Key Data Structures

- **Directory Tree**: Nested dictionary structure representing folder hierarchy
- **File Lists**: Arrays of filenames under each directory
- **Statistics**: Counters for files processed, ignored, and tokens estimated
- **Configuration**: Dictionary of settings loaded from config files

## Component Details

### Entry Point (treetrim.py)

- Command-line argument parsing
- Configuration loading
- Orchestrates the scanning process
- Handles output file generation

### Core Processing (trimmer/)

#### scanner.py
- High-level scanning coordination
- Calls filesystem processing
- Returns formatted tree and statistics

#### filesystem.py
- Recursive directory traversal
- Applies ignore patterns and filters
- Handles repository detection logic
- Manages depth limiting and hidden file control

#### files.py
- File type and extension checking
- macOS alias detection using xattr
- Repository marker identification (directories)
- Repository detection in zip archives (using Python zipfile module)
  - Metadata-only inspection (no file extraction)
  - Reuses REPO_TYPES configuration
  - Graceful error handling for corrupted/inaccessible archives

#### formatter.py
- YAML structure generation
- Hierarchical output formatting
- Empty directory notation

#### sorter.py
- macOS Finder-compatible file sorting
- Natural sorting for mixed alphanumeric names

#### stats.py
- Processing metrics calculation
- Token usage estimation
- Console output formatting

#### utils.py
- Configuration file parsing
- Ignore pattern loading
- Path utilities

### Configuration System

#### config.py
- Core application settings
- Feature toggles (IGNORE_HIDDEN, COLLAPSE_CHAINS, etc.)
- Repository type definitions
- Token and depth limits

#### config_loc.py
- User-specific paths (SOURCE_DIR, OUTPUT_DIR)
- Git-ignored for privacy

#### ignore_types.conf
- File extensions to exclude
- One pattern per line

#### ignore_pat.conf
- Directory patterns to skip
- Organized by category (build, cache, system, etc.)

## Key Features

### Directory Processing
- **Hierarchical Scanning**: Recursive traversal with depth control
- **Pattern Filtering**: Configurable directory and file type exclusions
- **Hidden File Handling**: Optional skipping of dot-files
- **Alias Detection**: macOS alias identification and marking

### Repository Detection
- **VCS Recognition**: Identifies git, mercurial, subversion repositories
- **Marker-Based Detection**: Uses standard VCS directory markers
- **Dual Format Support**: Detects repos in both directories and zip archives
  - Directory repos: Marked with `.repo` suffix
  - Archive repos: Marked with `.repo.zip` suffix
  - Archive scanning uses metadata-only inspection (no extraction)
- **Clean Output**: Marks repos without expanding internals
- **Nested Support**: Detects repositories within repositories (directories only)

### Output Optimization
- **Token Efficiency**: Designed for LLM context windows
- **YAML Format**: Machine-readable hierarchical structure
- **File Limiting**: Configurable maximum files per directory
- **Summary Fallbacks**: Handles large directories gracefully

### macOS Integration
- **Finder Sorting**: Maintains native file ordering
- **Alias Support**: Recognizes and marks macOS aliases
- **System File Handling**: Ignores macOS-specific directories

## Configuration Overrides

### Repository Mode
When `--repo` flag is used:
- Ignore patterns for VCS markers are bypassed
- Repository directories are detected and marked
- Repository internals are not expanded
- Other ignore patterns still apply

### Hidden Files
When `IGNORE_HIDDEN = True`:
- All dot-prefixed directories are skipped
- Except in repo mode, where VCS markers are detected first

## Performance Considerations

- **Depth Limiting**: `MAX_SCAN_DEPTH` prevents excessive recursion
- **Pattern Matching**: Efficient string matching for ignore rules
- **File Limiting**: `MAX_FILES_DISPLAY` controls output size
- **Caching**: No caching implemented (single-pass processing)

## Error Handling

- **Permission Errors**: Graceful handling of inaccessible directories
- **Missing Config**: Fallback to default settings
- **File System Issues**: Robust traversal with error recovery

## Dependencies

- **Python 3.7+**: Core language support
- **PyYAML**: YAML output generation
- **xattr**: macOS extended attributes for alias detection
- **zipfile**: Standard library module for archive inspection (repo detection in zips)

## Integration Points

- **LMbridge Suite**: Part of document processing ecosystem
- **LLM Processing**: Output designed for AI analysis
- **File System APIs**: Uses standard os/pathlib modules
- **Configuration System**: Extensible settings architecture

## Future Considerations

- **Plugin Architecture**: Extensible filtering system
- **Output Formats**: Additional formats beyond YAML
- **Performance Optimization**: Parallel processing for large directories
- **Cross-Platform**: Enhanced Windows/Linux support