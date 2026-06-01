import sys

from media_tools.cli import file_cli, misc_cli, youtube_cli


COMMANDS = {
    "file": file_cli.run,
    "misc": misc_cli.run,
    "youtube": youtube_cli.run,
}


DESCRIPTIONS = {
    "file": file_cli.DESCRIPTION,
    "misc": misc_cli.DESCRIPTION,
    "youtube": youtube_cli.DESCRIPTION,
}


def print_help():
    print("\nMedia Tools CLI\n")
    print("Usage:\n  media-tools <command> [args]\n")

    print("Commands:\n")

    for name, desc in DESCRIPTIONS.items():
        print(f"  {name:<10} {desc}")


def main():
    args_list = sys.argv[1:]

    if not args_list or args_list[0] in ("-h", "--help"):
        print_help()
        return

    command = args_list[0]
    unknown_args = args_list[1:]

    handler = COMMANDS.get(command)

    if not handler:
        print(f"Unknown command: {command}\n")
        print_help()
        return

    try:
        handler(unknown_args)
    except Exception as e:
        print(f"Command error in '{command}': {e}")


if __name__ == "__main__":
    main()