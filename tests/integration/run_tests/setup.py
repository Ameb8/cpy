import yaml
import os
import tempfile
from pathlib import Path
from ..file_setup.file_setup import setup_temp_structure


def create_project_structure(project_name, yaml_file="file_structures.yaml", base_dir=None):
    yaml_path = Path(__file__).parent / yaml_file

    # Load the YAML file
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    if project_name not in data:
        raise ValueError(f"Project '{project_name}' not found in YAML")

    project = data[project_name]

    # Set location for file creation
    base = Path(base_dir) if base_dir else Path(tempfile.gettempdir())
    tmp_dir = base / project_name
    tmp_dir.mkdir(parents=True, exist_ok=True)

    def create_tree(base_path, tree_dict):
        for name, content in tree_dict.items():
            path = base_path / name
            if isinstance(content, dict):
                path.mkdir(parents=True, exist_ok=True)
                create_tree(path, content)
            else: # File with default empty content
                path.write_text(content or "")

    # Create directory/file structure from 'tree'
    if "tree" in project:
        create_tree(tmp_dir, project["tree"])

    # Write content to specified files in 'files'
    if "files" in project:
        for rel_path, file_content in project["files"].items():
            file_path = tmp_dir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(file_content)

    return tmp_dir

SETUP_FUNCTIONS = {
    "setup_files": create_project_structure
}

def run_setup(setup_block, temp_dir_path=None):
    if not setup_block:
        return

    for action, args in setup_block.items():
        if action not in SETUP_FUNCTIONS:
            return

        func = SETUP_FUNCTIONS[action]

        # DEBUG *******
        print(f"Action: {action}\tArgs: {args}")
        # END DEBUG ***

        # Normalize to list if single instance
        if not isinstance(args, list):
            args = [args]

        func(*args, base_dir=temp_dir_path)