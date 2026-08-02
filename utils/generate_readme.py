#!/usr/bin/env python3
import yaml
import sys
import os

class OCIOLoader(yaml.SafeLoader):
    def construct_object(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            node.tag = 'tag:yaml.org,2002:map'
        elif isinstance(node, yaml.SequenceNode):
            node.tag = 'tag:yaml.org,2002:seq'
        else:
            node.tag = 'tag:yaml.org,2002:str'
        return super().construct_object(node, deep)

def generate_readme(config_file="config.ocio", output_file="README.md"):
    if not os.path.exists(config_file):
        print(f"Error: Cannot find '{config_file}' in the current directory.")
        sys.exit(1)

    print(f"Reading configuration from {config_file}...")

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.load(f, Loader=OCIOLoader)

    md = []

    title = config.get('name', 'OCIO Configuration')
    md.append(f"# {title}\n")

    if 'description' in config:
        desc = config['description'].strip()
        md.append(f"{desc}\n")

    active_displays = config.get('active_displays', [])
    if active_displays:
        md.append("### Active Displays")
        for d in active_displays:
            md.append(f"- {d}")
        md.append("")

    active_views = config.get('active_views', [])
    if active_views:
        md.append("### Active Views")
        for v in active_views:
            md.append(f"- {v}")
        md.append("")

    roles = config.get('roles', {})
    if roles:
        md.append("### Roles")
        for role, space in roles.items():
            md.append(f"- **{role}**: `{space}`")
        md.append("")

    md.append("## Displays & Views\n")
    md.append("These are available in the user interface for viewing.\n")

    displays = config.get('displays', {})
    for display_name, views in displays.items():
        md.append(f"### {display_name}")
        for view in views:
            v_name = view.get('name', 'Unknown')
            v_cs = view.get('display_colorspace', view.get('colorspace', ''))
            v_look = view.get('looks', '')
            look_str = f" | Look: `{v_look}`" if v_look else ""
            md.append(f"- **{v_name}** (Target: `{v_cs}`{look_str})")
        md.append("")

    md.append("## Color Spaces\n")

    all_colorspaces = config.get('display_colorspaces', []) + config.get('colorspaces', [])

    for cs in all_colorspaces:
        name = cs.get('name', 'Unknown')
        desc = cs.get('description', '').strip()
        aliases = cs.get('aliases', [])
        alias_str = f" *(Aliases: {', '.join(aliases)})*" if aliases else ""

        md.append(f"### {name}")

        if desc:
            desc = desc.replace('\n', '\n> ')
            md.append(f"> {desc}\n")
        else:
            md.append("> *No description provided.*\n")

        md.append(f"{alias_str}")

    md.append("## Looks\n")
    looks = config.get('looks', [])

    if not looks:
        md.append("No looks defined in the configuration.\n")
    else:
        for look in looks:
            name = look.get('name', 'Unknown')
            pspace = look.get('process_space', 'Unknown')
            desc = look.get('description', '').strip()

            md.append(f"### {name}")
            md.append(f"- **Process Space:** `{pspace}`")
            if desc:
                md.append(f"- **Description:** {desc}")
            md.append("")

    print(f"Writing Markdown to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print("Done!")

if __name__ == "__main__":
    generate_readme()
