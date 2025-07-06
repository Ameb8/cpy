from pathlib import Path
from treelib import Tree
import glob
from .command import resolve_command

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
        files = glob.glob(path_pattern, recursive=True)

        count = 0
        for f in files:
            path = Path(f)
            if path.is_file():
                try:
                    file_map[str(path)] = path.read_text(encoding=encoding)
                    count += 1
                    if count >= max_files:
                        print(f"Warning: Reached max file limit ({max_files}).")
                        break
                except (UnicodeDecodeError, PermissionError, OSError) as e:
                    errors[str(path)] = e

        if not file_map and not errors:
            print("Warning: No files matched or could be read.")

        return file_map, list(errors.items())

    except Exception as e:
        return {}, [(path_pattern, e)]
    
def format_output(files, delimiter_arg):
    delimiter = "\n\n" # Default separator

    if delimiter_arg: # Separator specified
        delimiter, error = resolve_command(delimiter_arg)
        
        if error: # Invalid separator
            return None, error

    return delimiter.join(files.values()), None
    
def evaluate_path(input):
    # Parse filepath and separator
    path, split = get_delimiter(input)

    if not path: # Invalid path
        return None, INVALID_PATH_ERR
    
    # Read files into memory
    files, errors = read_files(path)

    if errors: # Error while reading
        err_str = f"File read error(s): {[f'{k}: {str(v)}' for k,v in errors]}"
        return None, err_str

    if not files: # Invalid filepath
        return None, INVALID_PATH_ERR

    return format_output(files, split)

