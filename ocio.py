#!/usr/bin/env python3
import os

def generate_qrc(output_filename="ocio.qrc", prefix="/ocio"):
    script_name = os.path.basename(__file__)
    ignore_files = {output_filename, script_name, 'README.py'}
    base_dir = os.path.abspath(os.path.dirname(__file__))

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

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Generated '{output_filename}' with {len(lines) - 4} files using prefix '{prefix}'.")

if __name__ == "__main__":
    generate_qrc()
