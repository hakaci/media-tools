import sys

from media_tools.commands.youtube_commands import run as youtube_run
from media_tools.commands.file_commands import run as file_run
from media_tools.commands.misc_commands import run as misc_run

COMMANDS = {
    "youtube": youtube_run,
    "file": file_run,
    "misc": misc_run,
}


def main():
    # no command provided
    if len(sys.argv) < 2:
        print("Available commands:")

        for cmd in COMMANDS:
            print(f"  - {cmd}")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    handler = COMMANDS.get(cmd)

    # unknown command
    if handler is None:
        print(f"Unknown command: {cmd}")
        print(
            "Available commands:",
            ", ".join(COMMANDS.keys())
        )
        return
    try:
        handler(args)

    except Exception as e:
        print(f"Error in '{cmd}': {e}")

if __name__ == "__main__":
    main()