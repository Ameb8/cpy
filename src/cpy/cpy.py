import argparse
import pyperclip
from .parse_content import get_output

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

    return parser.parse_args()


def update_clipboard(text, append=False):
    if append:
        text = pyperclip.paste() + text

    pyperclip.copy(text)
    

def main():
    args = get_args()
    output = get_output(" ".join(args.clip_content))
    update_clipboard(text=output, append=args.append)
    
    if args.out:
        print(output)
    

if __name__ == "__main__":
    main()