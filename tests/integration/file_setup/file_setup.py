import os
import yaml
from tempfile import TemporaryDirectory
from pathlib import Path

def create_tree(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_tree(path, content)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content if content else "")

def load_structure(name, yaml_file='file_structures.yaml'):
    # Get relative path
    yaml_path = Path(__file__).parent / yaml_file

    # Load yaml data into memory
    with open(yaml_path, 'r', encoding='utf-8') as f:
        structures = yaml.safe_load(f)

    # Invalid input
    if name not in structures:
        raise ValueError(f"Structure '{name}' not found in {yaml_file}")
    
    return structures[name]

def setup_temp_structure(structure_name, yaml_file='file_structures.yaml'):
    if not structure_name:
        return None, None
    
    structure = load_structure(structure_name, yaml_file)

    # Wrap everything in a TemporaryDirectory context manager
    temp_dir_ctx = TemporaryDirectory(prefix=f"{structure_name}_")
    temp_dir_path = Path(temp_dir_ctx.name)

    if 'tree' in structure:
        create_tree(temp_dir_path, structure['tree'])

    if 'files' in structure:
        for filepath, content in structure['files'].items():
            full_path = temp_dir_path / filepath
            os.makedirs(full_path.parent, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

    return temp_dir_ctx, temp_dir_path
