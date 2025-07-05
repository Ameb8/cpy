import re
import os
import platform
import random
import uuid
import subprocess
import glob
from datetime import datetime, date
from command import resolve_command

def preprocess_content(clip_content):
    return re.sub(r'\\\s*', '\n', clip_content)

def _missing_arg(command):
    return None, f"Missing argument for '{command}'"

def _bad_arg(command):
    return None, f"Invalid syntax for '{command}'"

def read_file(path):
    # Check if path contains any glob pattern characters
    if any(char in path for char in "*?[]"):
        matched_files = glob.glob(path)
        if not matched_files:
            return None, f"No files matched the pattern '{path}'"
        combined_content = []
        for file_path in matched_files:
            try:
                with open(file_path, 'r') as f:
                    combined_content.append(f.read().strip())
            except Exception as e:
                return None, f"Error reading file '{file_path}': {e}"
        # Join all file contents separated by two newlines for clarity
        return "\n\n".join(combined_content), None
    else:
        # If no glob pattern, just read single file as before
        try:
            with open(path, 'r') as f:
                return f.read().strip(), None
        except Exception as e:
            return None, f"Error reading file '{path}': {e}"

'''
def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip(), None
    except Exception as e:
        return None, f"Error reading file '{path}': {e}"
'''

def handle_input(command_text):
    result, error = resolve_command(command_text)
    if result is not None or error is not None:
        return result, error

    if os.path.isfile(command_text):
        return read_file(command_text)

    return None, f"Command not recognized: {command_text}"

def get_output(clip_content):
    clip_content = preprocess_content(clip_content)
    pattern = r'\[\[(.*?)\]\]'
    errors = []

    def replacer(match):
        command = match.group(1)
        result, error = handle_input(command)
        if error:
            errors.append((command, error))
            return ""
        return result

    result = re.sub(pattern, replacer, clip_content)
    return result, errors

