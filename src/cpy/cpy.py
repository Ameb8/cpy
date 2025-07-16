import argparse
import pyperclip
from .parse_content import get_output
from user_vars.use_vars import handle_var_args

CPY_DESCRIPTION = "cpy is a command line tool for copying formatted text to your clipboard"


def get_args():
    parser = argparse.ArgumentParser(description=CPY_DESCRIPTION, prog = 'cpy')

    parser.add_argument(
        "clip_content",
        help="The contents of text to copy to clipboard",
        nargs=argparse.REMAINDER
    )

    parser.add_argument(
        "--append",
        help="Append to current clipboard content",
        action="store_true"
    )

    parser.add_argument(
        "--out",
        help="Print text copied to clipboard",
        action="store_true"
    )

    parser.add_argument(
        "--get",
        help="Access user-defined Key-Value pair by Key",
        nargs=1
    )

    parser.add_argument(
        "--set",
        help="Save Key-Value pair as user-defined variable",
        nargs=2
    )

    parser.add_argument(
        "--list",
        help="List all user defined variables",
        action="store_true"
    )

    parser.add_argument(
        "--delete",
        help="Remove user defined variable by Key",
        nargs=1
    )

    return parser.parse_args()


def update_clipboard(text, append=False):
    if append:
        text = pyperclip.paste() + text

    pyperclip.copy(text)


def is_valid_key(key):
    return all(c.isalnum() or c == '_' for c in key)


def main():
    args = get_args() # Get user arguments
    handle_var_args(args) # Handle variable updates
    output, errors = get_output(" ".join(args.clip_content)) # Get text to copy

    if len(errors) != 0: # Text generation failed
        print("INPUT ERRORS:")

        for command, error in errors: # Print errors
            print(f"Failed Command: {command}\n\t{error}")
    else: # Success, copy text to clipboard
        update_clipboard(text=output, append=args.append)
    
    if args.out: # Print content if requested
        print(output)
    

if __name__ == "__main__":
    main()




