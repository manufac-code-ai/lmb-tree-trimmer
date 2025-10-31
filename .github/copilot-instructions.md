# Copilot Instructions for LMbridge Tree Trimmer

## Project Overview
- **Purpose:** Generate token-efficient YAML snapshots of directory structures for LLM processing, focusing on folder relationships and omitting unnecessary files.
- **Architecture:**
  - Entry point: `treetrim.py` (CLI, orchestrates scan, formatting, and output)
  - Core logic: `trimmer/` package
    - `scanner.py`: Directory scanning, applies ignore rules, repo detection
    - `filesystem.py`: Traversal, chain collapsing, depth limiting
    - `files.py`: File/alias/repo/archive detection, filtering
    - `formatter.py`: YAML/flat output, Finder-style sorting
    - `sorting.py`: macOS Finder sort emulation
    - `stats.py`: Processing statistics
    - `utils.py`: Loads ignore patterns/types
  - Config: `config/config.py` (main), `config/config_loc.py` (local, git-ignored), `ignore_types.conf`, `ignore_pat.conf`
  - Output: `_output/` (auto-named snapshot files)

## Key Workflows
- **Run scan:** `python treetrim.py [--repo|--repo-files]`
  - `--repo`: Folders-only, marks repos with `.repo`/`.repo.zip`
  - `--repo-files`: Shows files in repos, respects file display limits
- **Configure source/output:** Edit `config/config_loc.py` (never commit personal paths)
- **Adjust filtering:**
  - File types: `config/ignore_types.conf`
  - Directory patterns: `config/ignore_pat.conf`
  - Main toggles: `config/config.py` (e.g., `MAX_FILES_DISPLAY`, `IGNORE_HIDDEN`, `COLLAPSE_CHAINS`)

## Project-Specific Conventions
- **macOS focus:** Handles aliases (via `xattr`), icon files, Finder sort order
- **YAML output:**
  - Folders as nested keys, files as lists under `files:`
  - `{}` for empty folders (may not be truly empty)
  - Aliases: `.alias` suffix
  - Repos: `.repo` (dirs), `.repo.zip` (archives)
- **Token management:** Output designed for LLM context windows; see `TOKEN_LIMIT` in config
- **Stats:** Console output includes raw/filtered counts, token usage

## Patterns & Integration
- **Never hardcode paths:** Always use config files for source/output
- **Ignore rules:** Use loader functions (`load_ignore_types`, `load_ignore_patterns`) for all filtering
- **Sorting:** Always use `finder_sort_key` for output order
- **Extensibility:** Add new ignore patterns/types via config, not code
- **Output location:** Always write to `_output/` unless overridden in config

## Examples
- To scan a directory with repo detection:
  ```bash
  python treetrim.py --repo
  ```
- To change the scan target:
  ```python
  # config/config_loc.py
  SOURCE_DIR = "/Users/yourname/Documents/ProjectFolder"
  ```

## References
- See `README.md` for detailed usage, configuration, and output format examples.
- Key files: `treetrim.py`, `trimmer/`, `config/`, `_output/`

---
For AI agents: Always respect user config, follow project conventions, and prefer configuration-driven changes over code edits for filtering and paths.

---



## Specialized Tools – Claude Code

When collaborating on code-adjacent or prompt-engineering tasks with Claude Code,
apply the specialized prompting rules described in the adjacent file
`claude_code_prompting_for_copilot_251031.md`.

Key guidelines:
- Lead through clarity, not control; define what to achieve, not how.
- Flag uncertainty and invite Claude Code to confirm or adjust the plan.
- Maintain a peer-level, factual, concise tone focused on truth and progress.
- Use the workflow rhythm: context → plan → confirm → execute → review → clear.
- If drift or ambiguity appears, pause for alignment before continuing.

These principles ensure Copilot’s drafts remain compatible with
Claude Code’s agentic planning model in VS Code.
