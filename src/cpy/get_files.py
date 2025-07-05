from pathlib import Path
from typing import Tuple
from command import resolve_command

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

def read_files(path_pattern: str, encoding: str = "utf-8", max_files: int = 1000):
    errors = {}
    file_map = {}

    try:
        path_obj = Path()
        files = path_obj.glob(path_pattern) if '**' not in path_pattern else path_obj.rglob(path_pattern.replace('**/', '', 1))

        count = 0

        for f in files:
            if f.is_file():
                try:
                    file_map[str(f)] = f.read_text(encoding=encoding)
                    count += 1
                    if count >= max_files:
                        print(f"Warning: Reached max file limit ({max_files}).")
                        break
                except (UnicodeDecodeError, PermissionError, OSError) as e:
                    errors[str(f)] = e

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
        return None, "Unrecognized Command"
    
    # Read files into memory
    files, errors = read_files(path)

    if errors: # Error while reading
        err_str = f"File read error(s): {[f'{k}: {str(v)}' for k,v in errors]}"
        return None, err_str

    if not files: # Invalid filepath
        return None, "Unrecognized Command"

    return format_output(files, split)



