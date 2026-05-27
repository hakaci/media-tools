from pathlib import Path

from media_tools.file_manager.fs_ops import file_search, safe_rename
from media_tools.file_manager.csv_ops import (
    get_metadata_csv_list,
    get_absolute_paths_from_metadata_csv
)
from media_tools.file_manager.metadata_ops import create_rename_metadata_rows

from media_tools.constants import (
    HOARD_METADATA_CSV_PATH,
    HOARD_PATHS,
    EXTS
)


# build path from metadata row
def _build_path(row):
    return Path(row[4]) / f"{row[1]}{row[2]}"

def rename_new_files():
    print("\nRenamer started.")

    # current metadata
    metadata_rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)

    # existing tracked files from CSV
    tracked_paths = set(
        get_absolute_paths_from_metadata_csv(metadata_rows)
    )

    # all filesystem files
    all_files = file_search(HOARD_PATHS, EXTS)

    # detect new files
    new_files = set(all_files) - tracked_paths

    if not new_files:
        print("No new files to rename.\n")
        return []

    # create metadata rows + rename files inside that function
    new_rows = create_rename_metadata_rows(new_files)

    # append to CSV handled inside metadata ops OR externally
    renamed_paths = []

    for row in new_rows:
        renamed_paths.append(_build_path(row))

    print("Renamer finished.\n")

    return renamed_paths