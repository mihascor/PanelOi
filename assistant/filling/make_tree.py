from pathlib import Path

EXCLUDE_DIRS = {"venv", "__pycache__", ".git", "build", "dist", "assistant", "backups"}
EXCLUDE_FILES = set()


def build_tree(dir_path: Path, prefix: str = "") -> list[str]:
    lines = []

    entries = sorted(
        [e for e in dir_path.iterdir()
         if e.name not in EXCLUDE_DIRS and e.name not in EXCLUDE_FILES],
        key=lambda e: (not e.is_dir(), e.name.lower())
    )

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if index == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))

    return lines


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    # C:\Users\PC\PanelOi\assistant\filling

    root = script_dir.parent.parent
    # C:\Users\PC\PanelOi  

    # папка assistant внутри проекта
    assistant_dir = root / "assistant"

    output_file = assistant_dir / "tree.txt"

    assistant_dir.mkdir(exist_ok=True)

    tree_lines = [root.name]
    tree_lines.extend(build_tree(root))

    output_file.write_text("\n".join(tree_lines), encoding="utf-8")

    print(f"Готово: {output_file}")