import argparse

from media_tools.file_manager.converter import convert_videos
from media_tools.file_manager.renamer import rename_new_files
from media_tools.file_manager.metadata_cleaner import clean_metadata
from media_tools.file_manager.last_files import copy_last_files

from media_tools.file_manager.fs_ops import (
    file_search,
    rename_all_from_metadata,
    safe_rename
)

from media_tools.file_manager.metadata_ops import (
    create_metadata_csv,
    update_metadata_csv
)

from media_tools.file_manager.csv_ops import (
    get_metadata_csv_list
)

from media_tools.constants import (
    HOARD_METADATA_CSV_PATH,
    HOARD_PATHS,
    EXTS
)


def run(args):
    parser = argparse.ArgumentParser(prog="media-tools file")

    sub = parser.add_subparsers(dest="cmd")

    # metadata commands
    sub.add_parser("create-csv")
    sub.add_parser("update-csv")
    sub.add_parser("rename-all")

    # automation commands
    sub.add_parser("convert")
    sub.add_parser("rename")
    sub.add_parser("clean")
    sub.add_parser("latest")

    # full workflow
    sub.add_parser("pipeline")

    parsed = parser.parse_args(args)

    # -------------------------
    # CREATE CSV
    # -------------------------

    if parsed.cmd == "create-csv":
        files = file_search(HOARD_PATHS, EXTS)

        create_metadata_csv(files)

        print("CSV created")

    # -------------------------
    # UPDATE CSV
    # -------------------------

    elif parsed.cmd == "update-csv":
        update_metadata_csv()

        print("CSV updated")

    # -------------------------
    # RENAME ALL
    # -------------------------

    elif parsed.cmd == "rename-all":
        rows = get_metadata_csv_list(
            HOARD_METADATA_CSV_PATH
        )[1:]

        rename_all_from_metadata(
            rows,
            safe_rename
        )

        print("Rename completed")

    # -------------------------
    # CONVERT VIDEOS
    # -------------------------

    elif parsed.cmd == "convert":
        convert_videos()

    # -------------------------
    # RENAME NEW FILES
    # -------------------------

    elif parsed.cmd == "rename":
        rename_new_files()

    # -------------------------
    # CLEAN METADATA
    # -------------------------

    elif parsed.cmd == "clean":
        clean_metadata()

    # -------------------------
    # COPY LATEST FILES
    # -------------------------

    elif parsed.cmd == "latest":
        copy_last_files()

    # -------------------------
    # FULL PIPELINE
    # -------------------------

    elif parsed.cmd == "pipeline":
        # sync metadata csv first
        update_metadata_csv()

        # convert videos
        convert_videos()

        # rename newly added files
        renamed_files = rename_new_files()

        # clean metadata from renamed files
        clean_metadata(renamed_files)

        # copy latest files to temp folder
        copy_last_files()

        print("Pipeline completed")

    else:
        parser.print_help()