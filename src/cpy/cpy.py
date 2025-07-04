import argparse

CPY_DESCRIPTION = "cpy is a command line tool for copying formatted text to your clipboard"

def process_args(args):
    print(f"clip_content: {args.clip_content}\nappend: {args.append}")

def main():
    parser = argparse.ArgumentParser(description=CPY_DESCRIPTION, prog = 'cpy')

    parser.add_argument(
        "clip_content",
        help="The contents of text to copy to clipboard",
        nargs=argparse.REMAINDER  # captures all remaining positional args
    )

    parser.add_argument(
        "--append",
        help="Append to current clipboard content",
        action="store_true"
    )

    args = parser.parse_args()
    process_args(args)
    

if __name__ == "__main__":
    main()