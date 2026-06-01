import argparse
from pathlib import Path

from media_tools.file_manager.converter import convert_videos
from media_tools.file_manager.renamer import rename_new_files
from media_tools.file_manager.metadata_cleaner import clean_metadata
from media_tools.file_manager.last_files import copy_last_files
from media_tools.file_manager.mp3_service import run_mp3_conversion

from media_tools.file_manager.fs_ops import (
    file_search,
    rename_all_from_metadata,
    safe_rename,
    path_search,
    replace_strings_in_filenames,
    remove_prefix_from_filenames,
    remove_suffix_from_filenames,
)

from media_tools.file_manager.metadata_ops import (
    create_metadata_csv,
    update_metadata_csv,
    run_exif_error_scan,
)

from media_tools.file_manager.csv_ops import get_metadata_csv_list

from media_tools.constants import (
    HOARD_METADATA_CSV_PATH,
    HOARD_PATHS,
    EXTS,
    CONVERT_MP3_CSV_PATH,
    CONVERT_MP3_OUTPUT_PATH,
)

COMMAND_NAME = "file"
DESCRIPTION = "File operations: rename, convert, clean, organize"


def run(args):
    parser = argparse.ArgumentParser(
        prog="media-tools file",
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", metavar="command")
    sub.required = False

    # metadata commands
    sub.add_parser("create-csv", help="Create metadata CSV from filesystem scan")
    sub.add_parser(
        "update-csv", help="Update metadata CSV by syncing filesystem changes"
    )
    sub.add_parser("rename-all", help="Rename all files using metadata CSV mapping")
    exif_error_parser = sub.add_parser(
        "exif-errors",
        help="Detect files that fail metadata cleaning and move them to broken files folder",
    )
    exif_error_parser.add_argument("path", help="Folder path to scan")

    # automation commands
    sub.add_parser("convert", help="Convert supported video files to MP4 using ffmpeg")
    sub.add_parser(
        "rename", help="Rename newly added files and append them into metadata CSV"
    )
    sub.add_parser("clean", help="Remove metadata from media files using exiftool")
    sub.add_parser("latest", help="Copy latest tracked files into temp folder")

    # string manipulation commands
    replace_parser = sub.add_parser("replace", help="Replace strings inside filenames")
    replace_parser.add_argument("path", help="Folder path to scan files in")
    replace_parser.add_argument(
        "replacements",
        nargs="+",
        help="Pairs of strings to replace (old new old new ...)",
    )
    replace_parser.add_argument(
        "--include-folders",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include folder names in replacements (default: True)",
    )

    remove_prefix_parser = sub.add_parser(
        "remove-prefix", help="Remove prefix from filenames"
    )
    remove_prefix_parser.add_argument("path", help="Folder path to scan files in")
    remove_prefix_parser.add_argument("prefix", help="Prefix to remove")

    remove_suffix_parser = sub.add_parser(
        "remove-suffix", help="Remove suffix from filenames"
    )
    remove_suffix_parser.add_argument("path", help="Folder path to scan files in")
    remove_suffix_parser.add_argument("suffix", help="Suffix to remove")

    # Convert to MP3
    convert_mp3_parser = sub.add_parser(
        "convert-mp3", help="Convert supported media files to MP3 using ffmpeg"
    )
    convert_mp3_parser.add_argument("path", help="Folder path to scan and convert")

    # full workflow
    sub.add_parser("organize", help="Organize and synchronize media archive")

    parsed = parser.parse_args(args)

    if parsed.cmd is None:
        parser.print_help()
        return

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
    # RENAME ALL FILES
    # -------------------------

    elif parsed.cmd == "rename-all":
        rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)[1:]

        rename_all_from_metadata(rows, safe_rename)

        # rebuild CSV after destructive rename
        files = file_search(HOARD_PATHS, EXTS)
        create_metadata_csv(files)

        print("Full rename + CSV reset completed")

    # -------------------------
    # EXIF ERRORS
    # -------------------------

    elif parsed.cmd == "exif-errors":
        path = Path(parsed.path)

        result = run_exif_error_scan(path)

        print(f"Moved {result['moved']} broken files")

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
    # REPLACE STRINGS
    # -------------------------

    elif parsed.cmd == "replace":

        paths = path_search(Path(parsed.path))

        replace_strings_in_filenames(
            paths,
            parsed.replacements,
            include_folders=parsed.include_folders,
        )

    # -------------------------
    # REMOVE PREFIX
    # -------------------------
    elif parsed.cmd == "remove-prefix":

        paths = path_search(Path(parsed.path))

        remove_prefix_from_filenames(
            paths,
            parsed.prefix,
            include_folders=parsed.include_folders,
        )

    # -------------------------
    # REMOVE SUFFIX
    # -------------------------
    elif parsed.cmd == "remove-suffix":

        paths = path_search(Path(parsed.path))

        remove_suffix_from_filenames(
            paths,
            parsed.suffix,
            include_folders=parsed.include_folders,
        )

    # -------------------------
    # CONVERT MP3
    # -------------------------

    elif parsed.cmd == "convert-mp3":
        folder_path = Path(parsed.path)

        # run full conversion pipeline
        converted = run_mp3_conversion(
            folder_path,
            [".mp4", ".webm", ".mp3"],
            CONVERT_MP3_CSV_PATH,
            CONVERT_MP3_OUTPUT_PATH,
        )

        print(f"\nsuccessfully converted {len(converted)} files")
        print("\nMP3 converter finished\n")

    # -------------------------
    # ORGANIZER
    # -------------------------

    elif parsed.cmd == "organize":
        # convert videos
        convert_videos()

        # sync current filesystem state
        update_metadata_csv()

        # refresh latest temp folder
        copy_last_files()

        print("Organizer completed")

    else:
        parser.print_help()
