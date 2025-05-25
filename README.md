# LMbridge Tree Trimmer

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

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

Modern LLMs like ChatGPT or Grok can help organize your life, but they struggle with the complexity of large file systems built over decades of projects. With thousands of folders and files, token limits make direct analysis impossible. This Python tool, designed for macOS, trims your file structure into a simplified YAML export, focusing on folders while ignoring unnecessary files, so you can use an LLM to reorganize or analyze your directory hierarchy.

**Purpose:** Enable LLMs to recommend file system reorganization by providing a token-efficient snapshot of your directory structure, reducing the cognitive overhead of managing decades of complex project data.

Note: This repository starts with a single commit to provide a clean, focused version of the project for public sharing.

## Quick Start

```bash
# Generate directory structure with default settings
python treetrim.py

# Customize source directory in config/config_loc.py
echo 'SOURCE_DIR = "/your/target/directory"' > config/config_loc.py
python treetrim.py

# View generated YAML structure
ls _out/
# Example: 250524-1341 MyProject structure_snapshot.yaml
```

## Features

### Directory Processing

- **YAML Output**: Converts directory structures to machine-readable YAML format
- **File Filtering**: Configurable limits on files displayed per directory
- **macOS Compatibility**: Handles aliases and system-specific file types
- **Hidden File Control**: Option to exclude dot-files and system directories

### Output Structure

- **Hierarchical Format**: Preserves folder relationships in nested YAML
- **Finder Sorting**: Maintains macOS file ordering in output
- **Alias Identification**: Marks macOS aliases for clear differentiation
- **Processing Statistics**: Reports on files scanned, filtered, and token counts

### Configuration Options

- **Private Local Settings**: Git-ignored configuration for personal directory paths
- **File Type Exclusions**: Customizable lists for filtering unwanted file types
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

### Command Line Options

Currently operates via configuration file settings. See [Configuration](#configuration) for customization options.

## Configuration

### Local Paths (Recommended)

Create `config/config_loc.py` for your personal directory paths:

```python
# Local source directory
SOURCE_DIR = "/Users/yourname/Documents/ProjectFolder"

# Optional: Custom output directory (defaults to "_out")
OUTPUT_DIR = "/path/to/custom/_out"
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
```

### File Type Filtering (`config/ignore_types.txt`)

Customize which file types to exclude:

```
.ds_store
.jpg
.jpeg
.png
.heic
.gif
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

### Output Files

- **Filename Format**: `YYMMDD-HHMM <source folder name> structure_snapshot.yaml`
- **Location**: `_out/` directory (configurable)
- **Statistics**: Console output shows processing summary and token usage

### Key Features

- **Hierarchy Preservation**: Nested YAML structure mirrors directory relationships
- **File Grouping**: Files listed under parent directories as YAML arrays
- **Empty Folder Notation**: `{}` indicates folders with no visible children
- **Alias Detection**: macOS aliases marked with `.alias` extension in output

## Integration with LMbridge Suite

Tree Trimmer works as part of the LMbridge document processing ecosystem for file system analysis and organization. Other LMbridge tools like Doc Validator and Doc Stacker handle document content processing, while Tree Trimmer focuses on structural analysis to help optimize directory organization.

### Common Workflow

**File System Analysis:**

```bash
# 1. Generate structure snapshot for analysis
python treetrim.py

# 2. Review YAML output with LLM for organization recommendations
# 3. Reorganize files and directories based on insights
# 4. Re-run Tree Trimmer to verify improved structure
```

## Project Structure

```
lmb-tree-trimmer/
├── config/
│   ├── config.py           # Main configuration
│   ├── config_loc.py       # Local paths (git-ignored)
│   └── ignore_types.txt    # File types to exclude
├── trimmer/                # Core package
│   ├── __init__.py         # Package exports
│   ├── files.py            # File operations and alias detection
│   ├── filesystem.py       # Directory traversal
│   ├── formatter.py        # YAML output formatting
│   ├── scanner.py          # Main scanning functions
│   ├── sorting.py          # Finder-compatible sorting
│   ├── stats.py            # Statistics reporting
│   └── utils.py            # Utility functions
├── _out/                   # Generated snapshots
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

Tree Trimmer provides structured visibility into file system organization for LLM-assisted document management and directory optimization.
