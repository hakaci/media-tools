import sys


from media_tools.commands import (
    video_splitter_commands,
    download_commands,
    metadata_commands
)

# Command registry
COMMANDS = {
    "split": video_splitter_commands.run,
    "download": download_commands.run,
    "metadata": metadata_commands.run,
}


def main():
    # No command provided → show help
    if len(sys.argv) < 2:
        print("Available commands:")

        for cmd in COMMANDS:
            print(f"  - {cmd}")

        return

    # Extract command and arguments
    cmd = sys.argv[1]
    args = sys.argv[2:]

    # Resolve command function
    command = COMMANDS.get(cmd)

    if command is None:
        print(f"Unknown command: {cmd}")
        print("Available commands:", ", ".join(COMMANDS.keys()))
        return

    # Run command safely
    try:
        command(args)

    except Exception as e:
        print(f"Error while running '{cmd}': {e}")


if __name__ == "__main__":
    main()