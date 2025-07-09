import subprocess

def delete_vars(*vars):
    for var in vars:
        return subprocess.run(
            ["python3", "-m", "src.cpy.cpy", "--delete", var],
            capture_output=True,
            text=True
        )

CLEANUP_FUNCTIONS = {
    "delete_var": delete_vars
}

def run_cleanup(cleanup_block):
    if not cleanup_block:
        return

    for action, args in cleanup_block.items():
        if action not in CLEANUP_FUNCTIONS:
            return

        func = CLEANUP_FUNCTIONS[action]

        # Normalize to list if single instance
        if not isinstance(args, list):
            args = [args]

        func(*args)