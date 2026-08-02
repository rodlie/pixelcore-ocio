#!/usr/bin/env python3
import os
import sys

def generate_qrc(target_dir, output_filename="ocio.qrc", prefix="/ocio"):
    base_dir = os.path.abspath(target_dir)
    if not os.path.isdir(base_dir):
        print(f"Error: The directory '{base_dir}' does not exist.")
        sys.exit(1)

    output_path = os.path.join(base_dir, output_filename)

    script_name = os.path.basename(__file__)
    ignore_files = {output_filename, script_name, 'generate_readme.py'}

    lines = []
    lines.append("<!DOCTYPE RCC>")
    lines.append('<RCC version="1.0">')
    lines.append(f'  <qresource prefix="{prefix}">')

    for root, dirs, files in os.walk(base_dir):
        dirs[:] = sorted([d for d in dirs if not d.startswith('.') and d != "__pycache__"])

        for file in sorted(files):
            if file.startswith('.') or file in ignore_files:
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, base_dir)
            rel_path = rel_path.replace(os.sep, "/")

            lines.append(f'    <file>{rel_path}</file>')

    lines.append('  </qresource>')
    lines.append('</RCC>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    file_count = len(lines) - 4
    print(f"Generated '{output_filename}' in '{base_dir}' with {file_count} files under prefix '{prefix}'.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_qrc(target)
