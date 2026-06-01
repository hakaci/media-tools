def register_commands(parser, commands):

    subparsers = parser.add_subparsers(dest="command")

    for name, meta in commands.items():

        subparsers.add_parser(
            name, help=meta["description"], description=meta["description"]
        )

    return parser


def run_command(args, unknown_args):
    """
    Executes selected command safely.
    """

    if not hasattr(args, "func"):
        return

    try:
        args.func(unknown_args)

    except Exception as e:
        print(f"Command error: {e}")


def print_global_help(parser):
    print("\nMedia Tools CLI\n")
    print("Usage:\n  media-tools <command> [args]\n")

    print("Commands:\n")

    for action in parser._subparsers._actions:
        if hasattr(action, "choices"):
            for name, sub in action.choices.items():
                desc = sub.description or "No description"
                print(f"  {name:<10} {desc}")
