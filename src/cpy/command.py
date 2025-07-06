import re
import os
import platform
import random
import uuid
import subprocess
import glob
from pathlib import Path
from treelib import Tree
from datetime import datetime, date


def get_file_tree(path):
    try:
        path = Path(path).resolve(strict=True)

        tree = Tree()
        root_id = path.as_posix()
        tree.create_node(path.name, root_id)

        if path.is_dir():
            def build_tree(current_path: Path, parent_id: str):
                try:
                    for item in sorted(current_path.iterdir()):
                        item_id = item.as_posix()
                        tree.create_node(item.name, item_id, parent=parent_id)
                        if item.is_dir():
                            build_tree(item, item_id)
                except PermissionError as e:
                    tree.create_node(f"[Permission Denied]", f"{parent_id}/__denied__", parent=parent_id)

            build_tree(path, root_id)

        return tree.show(stdout=False), None

    except FileNotFoundError:
        return None, f"Path '{path}' not found."
    except PermissionError:
        return None, f"Permission denied accessing '{path}'."
    except Exception as e:
        return None, f"Unexpected error: {e}"

def _missing_arg(command):
    return None, f"Missing argument for '{command}'"

def _bad_arg(command):
    return None, f"Invalid syntax for '{command}'"

def get_commands(arg):
    return {
        "now": lambda: (datetime.now().isoformat(sep=' ', timespec='seconds'), None),
        "today": lambda: (date.today().isoformat(), None),
        "time": lambda: (datetime.now().strftime("%H:%M:%S"), None),
        "year": lambda: (str(date.today().year), None),
        "month": lambda: (f"{date.today().month:02d}", None),
        "weekday": lambda: (date.today().strftime('%A'), None),
        "uuid": lambda: (str(uuid.uuid4()), None),
        "user": lambda: ((os.environ.get("USER") or os.getlogin()), None),
        "hostname": lambda: (platform.node(), None),
        "cwd": lambda: (os.getcwd(), None),
        "os": lambda: (platform.system(), None),
        "git_branch": lambda: (subprocess.getoutput("git rev-parse --abbrev-ref HEAD"), None),
        "git_commit": lambda: (subprocess.getoutput("git rev-parse HEAD"), None),
        "upper": lambda: (arg.upper(), None) if arg else _missing_arg("upper"),
        "lower": lambda: (arg.lower(), None) if arg else _missing_arg("lower"),
        "reverse": lambda: (arg[::-1], None) if arg else _missing_arg("reverse"),
        "repeat": lambda: (arg.split(',', 1)[1] * int(arg.split(',', 1)[0]), None) if arg and ',' in arg else _bad_arg("repeat"),
        "random": lambda: (random.choice(arg.split('|')), None) if arg else _missing_arg("random"),
        "tree": lambda: get_file_tree(arg or '.'),
    }

def resolve_command(command_text):
    if ':' in command_text:
        cmd, arg = map(str.strip, command_text.split(':', 1))
    else:
        cmd, arg = command_text, None

    if cmd == "env" and arg:
        if arg in os.environ:
            return os.environ[arg], None
        return None, f"Environment variable '{arg}' not set"

    commands = get_commands(arg)

    if cmd in commands:
        return commands[cmd]()
    
    return None, None  # Command not found

