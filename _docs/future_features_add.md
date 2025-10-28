## Future Features: Extended Repo Modes

These feature notes are intended to be integrated with any existing or future update suggestions as determined by the user. They can be merged directly into a consolidated **Future Features** document without conflict or reformatting.

**Note:** As of commit `4dcee91` (October 2025), zip archive repository detection has been implemented and is now available via the `--repo` flag. Archives containing VCS markers are detected and marked with `.repo.zip` suffix.

---

### 1. Save YAML with TXT Extension

**Config Addition:**

```python
SAVE_YAML_WITH_TXT_EXT = True
```

**Behavior:**\
When this toggle is `True`, TreeTrimmer saves its structured YAML output using the `.txt` extension instead of `.yaml`. The file contents remain YAML-style, but this avoids file-type restrictions in certain environments (such as ChatGPT Projects) that block or filter YAML uploads.

**Purpose:**\
Allows users to share and upload structure snapshots freely without triggering file-type protections while retaining YAML readability and syntax.

**Implementation Concept:**

```python
output_ext = '.txt' if SAVE_YAML_WITH_TXT_EXT else '.yaml'
output_path = f"{OUTPUT_DIR}/tree_snapshot{output_ext}"
```

---

### 2. Automatic File Suppression in Repo Modes

**Config Addition:**

```python
AUTO_SUPPRESS_FILES_IN_REPO_MODE = True
```

**Behavior:**\
When either `--repo` or `--repo_only` is active and this flag is `True`, TreeTrimmer automatically overrides `MAX_FILES_DISPLAY` to `0` during that run. This prevents file listings from inflating output size while keeping the default `MAX_FILES_DISPLAY` (e.g., `50`) intact for regular scans.

**Implementation Concept:**

```python
if (args.repo or args.repo_only) and AUTO_SUPPRESS_FILES_IN_REPO_MODE:
    effective_max_files_display = 0
else:
    effective_max_files_display = MAX_FILES_DISPLAY
```

**Purpose:**\
Ensures repo scans stay clean, structural, and efficient without requiring manual configuration edits between modes.

---

### 3. `--repo_only`

**Description:**\
Adds an additional repo scanning mode that restricts output to repositories and their ancestor folders only. Non-repo folders that have no descendant repos are omitted from the output entirely.

**CLI Example:**

```bash
python treetrim.py --repo_only
```

**Functional Intent:**\
Provides a concise, high-level view of all repos within a directory tree while preserving path context. Useful for users who maintain large repo collections and want a focused overview.

