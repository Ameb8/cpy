import re
import os
import platform
import random
import uuid
import subprocess
from datetime import datetime, date

def preprocess_content(clip_content):
    return re.sub(r'\\\s*', '\n', clip_content)

def handle_command(command_text):
    if ':' in command_text:
        cmd, arg = command_text.split(':', 1)
    else:
        cmd, arg = command_text, None

    commands = {
        "now": lambda: datetime.now().isoformat(sep=' ', timespec='seconds'),
        "today": lambda: date.today().isoformat(),
        "time": lambda: datetime.now().strftime("%H:%M:%S"),
        "year": lambda: str(date.today().year),
        "month": lambda: f"{date.today().month:02d}",
        "weekday": lambda: date.today().strftime('%A'),
        "uuid": lambda: str(uuid.uuid4()),
        "user": lambda: os.environ.get("USER") or os.getlogin(),
        "hostname": lambda: platform.node(),
        "cwd": lambda: os.getcwd(),
        "os": lambda: platform.system(),
        "git_branch": lambda: subprocess.getoutput("git rev-parse --abbrev-ref HEAD"),
        "git_commit": lambda: subprocess.getoutput("git rev-parse HEAD"),
        "upper": lambda: arg.upper() if arg else "[missing arg]",
        "lower": lambda: arg.lower() if arg else "[missing arg]",
        "reverse": lambda: arg[::-1] if arg else "[missing arg]",
        "repeat": lambda: arg.split(',', 1)[1] * int(arg.split(',', 1)[0]) if arg and ',' in arg else "[invalid repeat syntax]",
        "file": lambda: read_file(arg) if arg else "[missing file arg]",
        "random": lambda: random.choice(arg.split('|')) if arg else "[missing random options]",
    }

    if cmd == "env" and arg:
        return os.environ.get(arg, f"[Env var {arg} not set]")

    if cmd in commands:
        return commands[cmd]()
    elif os.path.isfile(command_text):
        return read_file(command_text)
    else:
        return f"[Command not recognized: {command_text}]"

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        return f"[ERROR reading file: {e}]"

def get_output(clip_content):
    clip_content = preprocess_content(clip_content)
    pattern = r'\[\[(.*?)\]\]'

    def replacer(match):
        command = match.group(1)
        return handle_command(command)

    return re.sub(pattern, replacer, clip_content)
