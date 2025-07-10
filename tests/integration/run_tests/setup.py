from ..file_setup.file_setup import setup_temp_structure

SETUP_FUNCTIONS = {
    "setup_files": setup_temp_structure
}

def run_setup(setup_block):
    if not setup_block:
        return

    for action, args in setup_block.items():
        if action not in SETUP_FUNCTIONS:
            return

        func = SETUP_FUNCTIONS[action]

        # Normalize to list if single instance
        if not isinstance(args, list):
            args = [args]

        func(*args)