import argparse

from media_tools.file_manager.fs_ops import rename_all_from_metadata, file_search, safe_rename
from media_tools.file_manager.metadata_ops import create_metadata_csv
from media_tools.file_manager.csv_ops import get_metadata_csv_list

from media_tools.config import (
    HOARD_METADATA_CSV_PATH,
    PATHS,
    EXTS
)


def run(args):
    parser = argparse.ArgumentParser(prog="media-tools file")

    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("create-csv")
    sub.add_parser("rename-all")

    parsed = parser.parse_args(args)

    # -------------------------
    # CREATE CSV
    # -------------------------
    if parsed.cmd == "create-csv":
        files = file_search(PATHS, EXTS)
        create_metadata_csv(files)
        print("CSV created")

    # -------------------------
    # RENAME ALL
    # -------------------------
    elif parsed.cmd == "rename-all":
        rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)[1:]

        rename_all_from_metadata(rows, safe_rename)

        print("Rename completed")

    else:
        parser.print_help()