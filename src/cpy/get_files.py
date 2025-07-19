from pathlib import Path
from treelib import Tree
import glob
from .command import resolve_command
from .cmd_parser import Cmd




INVALID_PATH_ERR = "Command not recognized:"

def get_delimiter(input):
    split_token = '--split:'
    
    # Check if split_token exists
    if split_token in input:
        parts = input.split(split_token, 1)
        path = parts[0].strip()
        delimiter = parts[1].strip()
        
        # Return tuple of two parts only if both sides have content
        if path and delimiter:
            return path, delimiter
        return None, None
    else:
        # No split_token, return entire string as single-element tuple if not empty
        stripped = input.strip()
        if stripped:
            return stripped, None
        else:
            return None, None

def read_files(path_pattern, encoding = "utf-8", max_files = 1000):
    errors = {}
    file_map = {}


    try:
        #files = glob.glob(path_pattern, recursive=True)

        # Set filepath as relative to working directory
        base_path = Path().resolve()
        absolute_pattern = str(base_path / path_pattern)
        files = glob.glob(absolute_pattern, recursive=True)

        # DEBUG *********
        if path_pattern == "blog/views.py":
            base_path = Path().resolve()
            absolute_pattern = str(base_path / path_pattern)
            print(f"File Map: {file_map}")
            print(f"Reading from cwd: {base_path}")
            print(f"Matched files with relative pattern: {glob.glob(path_pattern, recursive=True)}")
            print(f"Matched files with absolute pattern: {glob.glob(absolute_pattern, recursive=True)}")
        # END DEBUG *****

        count = 0
        for f in files:
            path = Path(f)
            if path.is_file():
                try:
                    #file_map[str(path)] = path.read_text(encoding=encoding)
                    file_map[f] = path.read_text(encoding=encoding)
                    count += 1
                    if count >= max_files:
                        print(f"Warning: Reached max file limit ({max_files}).")
                        break
                except (UnicodeDecodeError, PermissionError, OSError) as e:
                    # errors[str(path)] = e
                    continue

        if not file_map and not errors:
            print("Warning: No files matched or could be read.")

        return file_map, list(errors.items())

    except Exception as e:
        return {}, [(path_pattern, e)]

def get_name(path: str) -> str:
    components = path.strip().split("/")
    return components[-1]

def format_output(cmd: Cmd, files: dict[str, str]):
    if "path" in cmd.flags or "name" in cmd.flags:
        for path, content in files:
            header: list[str] = []
            if "path" in cmd.flags:
                header.append(path)
            if "name" in cmd.flags:
                header.append(get_name(path))
            if path in files:
                join = "\n".join(header)
                files[path] = f"{join}\n\n{content}"

    if "--split" in cmd.flags:
        split_token: list[str] = []
        for delimiter in cmd.flags["--split"]:
            # split_token.append(eval_cmd(delimiter))
            split_token.append(delimiter)

        join: str = "\n".join(split_token)
        return f"\n{join}\n".join(files)

    return "\n\n".join(files)


def evaluate_path(input: str):
    cmd: Cmd = Cmd.get_cmd(input)

    # Parse filepath and separator
    #path, split = get_delimiter(input)

    if not cmd or not cmd.cmd: # Invalid path
        return None, INVALID_PATH_ERR
    
    # Read files into memory
    files, errors = read_files(cmd.cmd)

    if errors: # Error while reading
        err_str = f"File read error(s): {[f'{k}: {str(v)}' for k,v in errors]}"
        return None, err_str

    if not files: # Invalid filepath
        return None, INVALID_PATH_ERR

    return format_output(cmd, files)

