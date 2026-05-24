import sys
from media_tools.commands import video_splitter_commands

COMMANDS = {
    "split": video_splitter_commands.run,
}

def main(): 
    if len(sys.argv) < 2:
        print("Available commands:")
        for cmd in COMMANDS:
            print(f"  - {cmd}")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    command = COMMANDS.get(cmd)

    if command is None:
        print(f"Unknown command: {cmd}")
        print("Available commands:", ", ".join(COMMANDS.keys()))
        return

    try:
        command(args)
    except Exception as e:
        print(f"Error while running '{cmd}': {e}")


if __name__ == "__main__":
    main()