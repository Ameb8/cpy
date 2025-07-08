import re
import os
import platform
import random
import uuid
import subprocess
import glob
from datetime import datetime, date
from .get_files import evaluate_path
from .command import resolve_command

def preprocess_content(clip_content):
    return re.sub(r'\\\s*', '\n', clip_content)


def handle_input(command_text):
    result, error = resolve_command(command_text)
    if result is not None or error is not None:
        return result, error

    return evaluate_path(command_text)

def get_output(clip_content):
    clip_content = preprocess_content(clip_content)
    pattern = r'\[\[(.*?)\]\]'
    errors = []

    def replacer(match):
        command = match.group(1)
        result, error = handle_input(command)

        if error: # Handle input errors
            errors.append((command, error))
            return ""
    
        # Handled commands inside variables
        if command.startswith("var") and result:
            return re.sub(pattern, replacer, result)

        return result

    result = re.sub(pattern, replacer, clip_content)
    return result, errors

