from pathlib import Path

from media_tools.file_manager.fs_ops import file_search, safe_rename
from media_tools.file_manager.csv_ops import (
    get_metadata_csv_list,
    get_absolute_paths_from_metadata_csv
)
from media_tools.file_manager.metadata_ops import append_metadata_csv
from media_tools.constants import (
    HOARD_METADATA_CSV_PATH,
    HOARD_PATHS,
    EXTS,
    REVERSE_NAMING_CONST
)


def rename_new_files():
    metadata_rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)

    # current CSV-tracked file paths
    tracked_paths = set(
        get_absolute_paths_from_metadata_csv(metadata_rows)
    )

    # actual filesystem state
    all_files = set(file_search(HOARD_PATHS, EXTS))

    # ONLY truly new files
    new_files = all_files - tracked_paths

    if not new_files:
        return []

    rename_map = []
    new_rows = []

    # stable ordering prevents collisions
    new_files = sorted(new_files)

    # build next metadata index safely
    last_row = metadata_rows[-1] if len(metadata_rows) > 1 else ["0", "0"]
    last_no = int(last_row[0])

    for i, file in enumerate(new_files, 1):
        file = Path(file)

        # safe new naming scheme
        new_name = f"{REVERSE_NAMING_CONST - (last_no + i)}{file.suffix}"

        new_path = file.with_name(new_name)

        # apply rename
        safe_rename(file, new_name)

        # build metadata row
        new_rows.append([
            str(last_no + i),
            new_name,
            file.suffix,
            str(int(file.stat().st_ctime)),
            str(file.parent)
        ])

        rename_map.append({
            "old": file,
            "new": new_path
        })

    # append ONLY new metadata
    append_metadata_csv(new_rows, HOARD_METADATA_CSV_PATH)

    return rename_map