# Contextify

A fast CLI tool that generates a comprehensive context file of your entire project — perfect for prompting LLMs like GPT, Gemini, Grok, etc.

---

## The Problem

When working with Large Language Models on a software project, providing the full context is a manual and inefficient process. Developers often have to copy-paste multiple files and describe the directory structure, which is tedious, error-prone, and often results in incomplete context for the AI.

## The Solution

**Contextify** automates this entire process. It's a Python script that scans a project directory, intelligently selects relevant files based on customizable rules, and compiles both the file structure tree and the file contents into a single, clean text file. This output can be directly pasted into an LLM prompt, giving the AI a complete and accurate snapshot of your project.

---

## Features

- **Recursive Directory Traversal:** Scans the entire project structure to build a complete file tree.
- **Intelligent File Exclusion:** Uses a `.ctxignore` file with `.gitignore`-style syntax for precise control over which files and folders to exclude.
- **Advanced Pattern Matching:** Supports standard wildcards (`*.log`, `?_file.txt`) and root-anchored paths (`/build/`) for flexible ignore rules.
- **Binary File Detection:** Automatically detects and skips binary files (images, executables, etc.) to keep the output clean and relevant.
- **Single File Output:** Consolidates all information into one `prompt_context.txt` file for easy copy-pasting.

---

## Usage

### Prerequisites
- Python 3.6 or newer.

### Step 1: Setup
Place the `ctx.py` script in the root directory of the project you want to scan.

### Step 2: Configuration (`.ctxignore`)
Create a file named `.ctxignore` in the same root directory. This file defines all the files and folders you want to exclude from the context.

**It is crucial to configure this file properly.** At a minimum, you should ignore the tool's own files to prevent them from being included in the output.

Here is a recommended template for your `.ctxignore` file:

```
# --- Self-ignore ---
# Ignore the Contextify tool's own files
ctx.py
.ctxignore
prompt_context.txt

# --- Common Ignores ---
# Version control folders
.git/
.svn/

# Language-specific dependency folders
node_modules/
venv/
__pycache__/

# Build and distribution artifacts
/build/
/dist/
/bin/

# IDE and OS-specific files
.vscode/
.idea/
*.pyc
*.swo
.DS_Store
Thumbs.db

# Log and temporary files
*.log
*.tmp
```

### Step 3: Execution
Navigate to your project's root directory in your terminal and run the script:

```bash
python ctx.py
```

### Step 4: The Output
The script will run and create a `prompt_context.txt` file in the same directory. You can now open this file, copy its entire contents, and paste it into your chat with an LLM.

---

## `.ctxignore` Syntax Guide

- **Comments:** Lines starting with `#` are ignored.

- **Directory Matches:** A rule matching a directory name (e.g., `dist` or `node_modules/`) will cause the entire directory and all of its contents to be skipped.

- **Filename Matches:** A name like `credentials.json` will ignore any file or folder with that name at any depth.

- **Wildcards:** Use `*` to match any sequence of characters and `?` to match any single character.
  - `*.log` ignores all files ending with `.log`.
  - `temp_?` ignores `temp_1`, `temp_A`, etc.

- **Root-Anchored Paths:** A pattern starting with `/` will only match files or folders in the root directory.
  - `/dist` ignores the `dist` folder at the project root but will **not** ignore a folder like `src/dist`.
---

## Limitations and Future Scope

- **Binary File Detection:** The check is based on a heuristic (presence of NUL bytes) and may not be 100% accurate for all file types.
- **Symbolic Links:** The script does not protect against infinite loops caused by recursive symbolic links.
- **Advanced Ignores:** Does not support more advanced `.gitignore` features like negation (`!`) or the `**` globstar pattern.
