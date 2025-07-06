from pathlib import Path
from treelib import Tree

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

