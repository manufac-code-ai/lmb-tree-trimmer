# LMbridge Tree Trimmer

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A directory structure visualization tool that generates token-efficient YAML snapshots of file systems for Large Language Model processing. Part of the LMbridge suite for bridging local documents to Large Language Model systems.

## Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output Format](#output-format)
- [Integration with LMbridge Suite](#integration-with-lmbridge-suite)

## Overview

LMbridge Tree Trimmer generates hierarchical snapshots of directory structures for LLM processing. It filters out unnecessary files and outputs structured YAML that preserves folder relationships while minimizing token usage.

LLMs struggle with the complexity of large file systems built over decades of projects. With thousands of folders and files, token limits make direct analysis impossible. This tool trims file structure into simplified YAML exports, focusing on folders while ignoring unnecessary files, enabling LLMs to analyze and recommend directory reorganization.

**Purpose:** Analyze file system organization and provide LLMs with structured directory information for cleanup and reorganization recommendations.

_Note: This repository starts with a single commit to provide a clean, focused version of the project for public sharing._

## Quick Start

```bash
# Generate directory structure with default settings
python treetrim.py

# Enable repository detection mode to mark git repos
python treetrim.py --repo

# Customize source directory in config/config_loc.py
echo 'SOURCE_DIR = "/your/target/directory"' > config/config_loc.py
python treetrim.py

# View generated YAML structure
ls _output/
# Example: 250524-1341 MyProject structure_snapshot.yaml
```

## Features

### Directory Processing

- **YAML Output**: Converts directory structures to machine-readable YAML format
- **File Filtering**: Configurable limits on files displayed per directory
- **Pattern Exclusion**: Ignores common bloat directories (node_modules, build, dist, etc.)
- **macOS Compatibility**: Handles aliases and system-specific file types
- **Hidden File Control**: Option to exclude dot-files and system directories
- **Repository Detection**: Optional mode to identify and mark version control repositories (directories and zip archives)

### Output Structure

- **Hierarchical Format**: Preserves folder relationships in nested YAML
- **Finder Sorting**: Maintains macOS file ordering in output
- **Alias Identification**: Marks macOS aliases for clear differentiation
- **Repository Marking**: In repo mode, marks detected repositories with `.repo` suffix (directories) or `.repo.zip` suffix (archives)
- **Processing Statistics**: Reports on files scanned, filtered, and token counts

### Configuration Options

- **Private Local Settings**: Git-ignored configuration for personal directory paths
- **File Type Exclusions**: Customizable lists for filtering unwanted file types
- **Directory Pattern Exclusions**: Skip common package and build directories
- **Display Controls**: Adjustable file limits with summary fallbacks when exceeded
- **Format Options**: Tree hierarchy or flat path listing modes

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/manufac-code-ai/lmb-tree-trimmer.git
   cd lmb-tree-trimmer
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Operation

```bash
# Generate structure snapshot with default settings
python treetrim.py
```

### Repository Detection Mode

```bash
# Enable repository detection (folders-only output)
python treetrim.py --repo

# Enable repository detection with file display
python treetrim.py --repo-files
```

Repository detection identifies repos in both directories and zip archives by their VCS marker files (e.g., `.git`, `.hg`, `.svn`):

- **Directory repositories** are marked with `.repo` suffix
- **Zip archives containing repositories** are marked with `.repo.zip` suffix
- Repository internals are not expanded to keep snapshots clean and focused on structure

**Mode behaviors:**
- `--repo`: Folders-only output (files suppressed, aliases and `.repo.zip` always shown)
- `--repo-files`: Full file display following `MAX_FILES_DISPLAY` configuration

The detection scans zip archives without extracting files (metadata-only inspection), adding negligible performance overhead (~0.5ms per archive).

### Command Line Options

- `--repo`: Enable repository detection mode with folders-only output
- `--repo-files`: Enable repository detection with file display (mutually exclusive with `--repo`)

## Configuration

### Local Paths (Recommended)

Create `config/config_loc.py` for your personal directory paths:

```python
# Local source directory
SOURCE_DIR = "/Users/yourname/Documents/ProjectFolder"

# Optional: Custom output directory (defaults to "_output")
OUTPUT_DIR = "/path/to/custom/_output"
```

This file is automatically ignored by git to keep your local paths private.

### Main Configuration (`config/config.py`)

Key settings include:

```python
# Maximum files to display per directory
MAX_FILES_DISPLAY = 1000    # Set to 0 to show only folders

# File filtering options
IGNORE_HIDDEN = True        # Skip dot-files and hidden folders
ICON_ELIMINATION = True     # Skip macOS icon files

# Processing behavior
COLLAPSE_CHAINS = True      # Collapse single-child folder chains
USE_TREE_FORMAT = True      # Hierarchical vs flat output

# Token management
TOKEN_LIMIT = 75000         # Target limit for LLM context windows

# Depth limiting
MAX_SCAN_DEPTH = 0          # 0 = unlimited, 5 = stop at 5 levels deep

# Output file extension
USE_TXT_EXTENSION = True    # True = .txt, False = .yaml

# Repository detection (command-line controlled)
# REPO_TYPES defines supported version control systems
```

**Note on Repository Mode:** When using `--repo`, some configuration settings are automatically overridden for compatibility:
- Directory ignore patterns (from `ignore_pat.conf`) are bypassed for known repository markers (e.g., `.git` folders) to allow detection
- Repository internals are not displayed, regardless of `MAX_FILES_DISPLAY` settings
- Hidden file controls still apply to non-repository directories

### File Type Filtering (`config/ignore_types.conf`)

Customize which file types to exclude:

```
.ds_store
.jpg
.jpeg
.png
.heic
.gif
```

### Directory Pattern Filtering (`config/ignore_pat.conf`)

Exclude common bloat directories:

```
node_modules
dist
build
coverage
.cache
.temp
vendor
```

## Output Format

### YAML Structure

Tree Trimmer generates structured YAML that preserves directory hierarchy:

```yaml
# This YAML represents a trimmed, structured export of a macOS file system folder.
# Files may be omitted due to TreeTrimmer config settings (e.g., MAX_FILES_DISPLAY = 0, ignored file types).
# Folders shown with {} are not necessarily empty — they simply have no visible children in this export.

Projects:
  _Archive:
    "Old Projects": {}
  Documentation:
    files:
      - README.md
      - CHANGELOG.md
    # [omitted 15 files]
  "Source Code":
    Backend:
      files:
        - server.py
        - database.py
    Frontend:
      files:
        - index.html
        - styles.css
```

With repository detection enabled (`--repo`), repositories are marked:

```yaml
Projects:
  active-project.repo:           # Detected git repository (directory)
    files:
      - README.md
  archived-project.zip.repo.zip  # Detected git repository (zip archive)
  data-backup.zip                # Regular zip (no repo detected)
  docs: {}
```

### Output Files

- **Filename Format**: `YYMMDD-HHMM <source folder name> structure_snapshot.{ext}`
  - Extension: `.txt` (default) or `.yaml` (configurable via `USE_TXT_EXTENSION`)
  - Content format: YAML regardless of extension
- **Location**: `_output/` directory (configurable)
- **Statistics**: Console output shows processing summary and token usage

### Key Features

- **Hierarchy Preservation**: Nested YAML structure mirrors directory relationships
- **File Grouping**: Files listed under parent directories as YAML arrays
- **Empty Folder Notation**: `{}` indicates folders with no visible children
- **Alias Detection**: macOS aliases marked with `.alias` extension in output
- **Repository Detection**: Optional mode marks repositories with `.repo` suffix (directories) or `.repo.zip` suffix (zip archives)

## Integration with LMbridge Suite

Tree Trimmer works as part of the LMbridge document processing ecosystem for file system analysis and organization. Other LMbridge tools like Doc Validator and Doc Stacker handle document content processing, while Tree Trimmer focuses on structural analysis to help optimize directory organization.

### Common Workflow

**File System Analysis:**

```bash
# 1. Generate structure snapshot for analysis
python treetrim.py

# 2. For repository-heavy directories, use repo detection
python treetrim.py --repo

# 3. Review YAML output with LLM for organization recommendations
# 4. Reorganize files and directories based on insights
# 5. Re-run Tree Trimmer to verify improved structure
```

## Project Structure

```
lmb-tree-trimmer/
├── config/
│   ├── config.py           # Main configuration
│   ├── config_loc.py       # Local paths (git-ignored)
│   ├── ignore_types.conf   # File extensions to exclude
│   └── ignore_pat.conf     # Directory patterns to ignore
├── trimmer/                # Core package
│   ├── __init__.py         # Package exports
│   ├── files.py            # File operations, alias detection, and archive repo detection
│   ├── filesystem.py       # Directory traversal
│   ├── formatter.py        # YAML output formatting
│   ├── scanner.py          # Main scanning functions
│   ├── sorting.py          # Finder-compatible sorting
│   ├── stats.py            # Statistics reporting
│   └── utils.py            # Utility functions
├── _output/                 # Generated snapshots
├── treetrim.py             # Application entry point
├── requirements.txt        # Python dependencies
└── README.md               # Documentation (this file)
```

## Requirements

- Python 3.7+
- xattr (for macOS alias detection)
- PyYAML (for structured output)
- Standard library modules: os, pathlib, locale

## Notes

- **macOS Focused**: Some features like alias detection are macOS-specific
- **Performance**: Handles directories with thousands of files
- **Token Considerations**: Output designed for LLM context windows
- **Privacy**: Local configuration system keeps personal paths out of version control
- **Repository Mode**: Optional feature for identifying version control directories and archives; detects repos in zip files without extraction; overrides some ignore settings for detection

Tree Trimmer provides structured visibility into file system organization for LLM-assisted document management and directory optimization.
