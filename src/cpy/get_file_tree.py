from pathlib import Path
from treelib import Tree

def should_ignore(name):
    """Determine if a file/directory should be hidden like ls does by default"""
    # Ignore dot files/directories (except . and ..)
    if name.startswith('.') and name not in ('.', '..'):
        return True

    # Common hidden directories to ignore
    common_hidden_dirs = {
        '__pycache__',  # Python bytecode cache
        '__MACOSX',  # macOS archive metadata
        '.ipynb_checkpoints',  # Jupyter notebook checkpoints
        '.ruff_cache',  # Ruff lint cache
        '.mypy_cache',  # Mypy type checker cache
    }
    if name in common_hidden_dirs:
        return True

    return False

def get_tree_str(path, extensions = None):
    try:
        path = Path(path).resolve(strict=True)

        tree = Tree()
        root_id = path.as_posix()
        tree.create_node(path.name, root_id)

        if path.is_dir():
            def build_tree(current_path, parent_id):
                try:
                    for item in sorted(current_path.iterdir()):
                        # Skip hidden files/directories
                        if should_ignore(item.name):
                            continue

                        if item.is_file() and extensions:
                            if not any(item.name.endswith(ext) for ext in extensions):
                                continue
                        item_id = item.as_posix()
                        tree.create_node(item.name, item_id, parent=parent_id)
                        if item.is_dir():
                            build_tree(item, item_id)
                except PermissionError:
                    tree.create_node("[Permission Denied]", f"{parent_id}/__denied__", parent=parent_id)

            build_tree(path, root_id)

        return tree.show(stdout=False), None

    except FileNotFoundError:
        return None, f"Path '{path}' not found."
    except PermissionError:
        return None, f"Permission denied accessing '{path}'."
    except Exception as e:
        return None, f"Unexpected error: {e}"


def get_file_tree(arg):
    if not arg:
        return get_file_tree('.')
    
    path_part, _, ext_part = arg.partition('|')
    path = path_part.strip() or '.'
    extensions = [e.strip() for e in ext_part.split(',') if e.strip()] if ext_part else None

    return get_tree_str(path, extensions)

