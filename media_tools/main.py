import sys
import argparse

from media_tools.cli_helpers import register_commands, run_command, print_global_help

from media_tools.cli_discovery import discover_commands


def main():
    parser = argparse.ArgumentParser(
        prog="media-tools",
        description="Media Tools CLI",
        add_help=False,
    )
    # auto-load all commands
    COMMANDS = discover_commands()

    parser = register_commands(parser, COMMANDS)

    args_list = sys.argv[1:]

    if not args_list or args_list[0] in ("-h", "--help"):
        print_global_help(parser)
        return

    args, unknown = parser.parse_known_args()

    if not args.command:
        print_global_help(parser)
        return

    run_command(args, unknown)


if __name__ == "__main__":
    main()
