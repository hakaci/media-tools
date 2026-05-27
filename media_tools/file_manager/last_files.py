from pathlib import Path
import shutil

from media_tools.file_manager.fs_ops import file_search
from media_tools.file_manager.csv_ops import (
    get_file_path_from_name,
    get_metadata_csv_list
)

from media_tools.constants import (
    HOARD_TEMP_PATH,
    HOARD_METADATA_CSV_PATH
)

EXTS = [".mp4", ".png", ".jpg", ".jpeg", ".webm", ".mov", ".gif", ".webp"]

ITEM_AMOUNT = 610


# remove old temp files that are no longer needed
def clear_temp_folder_content(paths):
    if not HOARD_TEMP_PATH.exists():
        HOARD_TEMP_PATH.mkdir()

    temp_files = file_search([HOARD_TEMP_PATH], EXTS)

    path_names = {p.name for p in paths}
    temp_names = {p.name for p in temp_files}

    new_files = path_names - temp_names
    old_files = temp_names - path_names

    # delete removed files
    for f in old_files:
        (HOARD_TEMP_PATH / f.name).unlink()

    return new_files


# copy latest files into temp folder
def get_last_files(paths):
    new_files = clear_temp_folder_content(paths)

    new_paths = get_file_path_from_name(new_files)

    for p in new_paths:
        shutil.copy(p, HOARD_TEMP_PATH)


# main logic
def copy_last_files():
    print("\nLast file getter started.")

    metadata = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)

    last_rows = metadata[-ITEM_AMOUNT:]

    last_paths = [
        Path(row[4]) / f"{row[1]}{row[2]}"
        for row in last_rows
    ]

    get_last_files(last_paths)

    print("Last file getter finished.\n")