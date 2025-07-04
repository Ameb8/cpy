import re
import os
from datetime import datetime, date

def preprocess_content(clip_content):
    return re.sub(r'\\\s*', '\n', clip_content)

def handle_command(command_text):
    commands = {
        "now": lambda: datetime.now().isoformat(sep=' ', timespec='seconds'),
        "today": lambda: date.today().isoformat(),
    }

    if command_text in commands:
        return commands[command_text]()
    
    if os.path.isfile(command_text):
        try:
            with open(command_text, 'r') as f:
                return f.read().strip()
        except Exception as e:
            return f"[ERROR reading file: {e}]"
    else:
        return f"[Command not recognized: {command_text}]"

def get_output(clip_content):
    clip_content = preprocess_content(clip_content)
    pattern = r'\[\[(.*?)\]\]'

    def replacer(match):
        command = match.group(1)
        return handle_command(command)

    return re.sub(pattern, replacer, clip_content)
