import os
import fnmatch
from pathlib import Path
from typing import Set, List

def load_ignore_list(root_dir: Path) -> Set[str]:
    """Loads rules from a .ctxignore file in the specified directory."""
    ignore_file = root_dir / ".ctxignore"
    ignore_list = set()
    if not ignore_file.is_file():
        return ignore_list

    with open(ignore_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = line.rstrip("/\\")
            ignore_list.add(line)
    return ignore_list

def build_structure_tree(
    dir_path: Path,
    root_dir: Path,
    ignore_list: Set[str],
    files_to_read: List[Path],
    prefix: str = ""
) -> str:
    try:
        entries = sorted(list(dir_path.iterdir()), key=lambda e: e.name.lower())
    except (FileNotFoundError, PermissionError):
        return f"{prefix}\\-- [ERROR: Cannot access]\n"

    visible_entries = []
    for entry in entries:
        relative_path = entry.relative_to(root_dir).as_posix()
        is_ignored = False
        for pattern in ignore_list:
            if pattern.startswith('/'):
                if fnmatch.fnmatch(relative_path, pattern.lstrip('/')):
                    is_ignored = True
                    break
            else:
                if fnmatch.fnmatch(entry.name, pattern):
                    is_ignored = True
                    break
        
        if not is_ignored:
            visible_entries.append(entry)

    tree_output = []
    for i, entry in enumerate(visible_entries):
        is_last = (i == len(visible_entries) - 1)
        branch = "\\-- " if is_last else "|-- "
        line_prefix = prefix + branch

        if entry.is_dir():
            tree_output.append(f"{line_prefix}{entry.name}/\n")
            next_prefix = prefix + ("    " if is_last else "|   ")
            subtree = build_structure_tree(entry, root_dir, ignore_list, files_to_read, next_prefix)
            tree_output.append(subtree)
        else:
            tree_output.append(f"{line_prefix}{entry.name}\n")
            files_to_read.append(entry)

    return "".join(tree_output)

def is_binary_file(path: Path) -> bool:
    """
    Checks if a file is likely binary by looking for NUL bytes in the first 1024 bytes.
    """
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return False

def append_file_contents(files_to_read: List[Path]) -> str:
    """Appends the content of all specified files to a single string."""
    content_output = ["\n---\n", "## File Contents\n"]
    for path in files_to_read:
        content_output.append(f"\n### File: {path.as_posix()}\n")
        content_output.append("---\n")
        
        if is_binary_file(path):
            content_output.append("[Skipped binary file]")
        else:
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content_output.append(f.read())
            except Exception:
                content_output.append("[Error: Could not open file to read.]")
        content_output.append("\n")
    return "".join(content_output)

def main():
    """Main function to run the script."""
    current_dir = Path.cwd()
    ignore_rules = load_ignore_list(current_dir)
    files_to_read = []

    tree_str = build_structure_tree(current_dir, current_dir, ignore_rules, files_to_read)

    contents_str = append_file_contents(files_to_read)

    output_filename = "prompt_context.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("## Project Structure\n\n")
        f.write(f"{current_dir.name}/\n")
        f.write(tree_str)
        f.write("\n")
        f.write(contents_str)

    print(f"Success! Project context written to {output_filename}")
    
if __name__ == "__main__":
    main()