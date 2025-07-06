import argparse
import pyperclip
from .parse_content import get_output
from .user_vars import save_kv, load_value, list_kvs, delete_kv

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
    
def handle_vars(args):
    # Handle --list command
    if args.list:
        vars = list_kvs()

        if vars: # Display vars
            print("\n".join(f"{k}:\t{v}" for k, v in list_kvs().items()))
        else: # No vars set
            print("No variables have been defined")

    # Handle --get command    
    if args.get:
        # Get KV pair
        key = args.get[0]
        val = load_value(key)
        
        if not val: # Key not found
            print(f"No variable defined for Key {args.get}")
        else: # Display Key-Value pair
            print(f"{args.get}:\t{val}")

    # Handle --set command
    if args.set:
        if not is_valid_key(args.set[0]): # Invalid Key
            print(f"'{args.set[0]}' is not a valid key. Keys must contain only letters, digits, and underscores")
        else: # Save or update variable
            save_kv(args.set[0], args.set[1])

    # Handle --delete command
    if args.delete:
        key = args.delete[0] # Get user inputted Key

        if(delete_kv):
            print(f"variable '{key}' successfully deleted")
        else:
            print(f"Could not delete variable '{key}' as it has not been defined")

def main():
    args = get_args()

    handle_vars(args)
    output, errors = get_output(" ".join(args.clip_content))

    if len(errors) != 0:
        print("INPUT ERRORS:")
        for command, error in errors:
            print(f"Failed Command: {command}\n\t{error}")
    else:
        update_clipboard(text=output, append=args.append)
    
    if args.out:
        print(output)
    

if __name__ == "__main__":
    main()




