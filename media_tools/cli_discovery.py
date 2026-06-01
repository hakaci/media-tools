import importlib
import pkgutil
import media_tools.cli as commands_pkg


def discover_commands():
    commands = {}

    for m in pkgutil.iter_modules(commands_pkg.__path__):
        module = importlib.import_module(f"media_tools.cli.{m.name}")

        if hasattr(module, "COMMAND_NAME") and hasattr(module, "run"):
            commands[module.COMMAND_NAME] = {
                "run": module.run,
                "description": getattr(module, "DESCRIPTION", "No description"),
            }

    return commands
