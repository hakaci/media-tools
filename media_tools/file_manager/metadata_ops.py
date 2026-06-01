from genericpath import getctime
from pathlib import Path
from operator import itemgetter
import subprocess
import csv
import os.path
from media_tools.file_manager.csv_ops import (
    get_metadata_csv_list,
    get_last_row_of_csv,
    append_metadata_csv,
    write_metadata_csv,
    get_absolute_paths_from_metadata_csv,
)
from media_tools.file_manager.fs_ops import (
    file_search,
    rename_a_file_given_name,
    lowercase_extensions,
)

from media_tools.constants import (
    HOARD_BROKEN_VIDS_PATH,
    HOARD_METADATA_CSV_PATH,
    HOARD_DROPPED_METADATA_CSV_PATH,
    HOARD_PATHS,
    EXTS,
    FIELDS,
)


def create_rename_metadata_rows(files):
    metadataRows = []

    # get last row of metadataCSV
    lastRowCSV = get_last_row_of_csv(HOARD_METADATA_CSV_PATH)
    lastNo = int(lastRowCSV[0])
    lastName = int(lastRowCSV[1])

    # create (timestamp, file) list
    timestamps_filepaths = [(int(getctime(file)), file) for file in files]

    # sort by creation time
    timestamps_filepaths.sort(key=itemgetter(0))

    # create rows sorted
    for i, (timestamp, file) in enumerate(timestamps_filepaths, 1):
        new_name = str(lastName - i)
        rename_a_file_given_name(file, new_name)

        metadataRows.append(
            [
                str(lastNo + i),
                new_name,
                str(file.suffix),
                str(timestamp),
                str(file.parent),
            ]
        )

    return metadataRows


def apply_metadata_sync(sync_data):
    """
    Applies filesystem/CSV reconciliation.
    """

    csv_rows = sync_data["csv_rows"]
    deleted = sync_data["deleted"]
    new = sync_data["new"]

    # -------------------------
    # 1. REMOVE DELETED
    # -------------------------
    deleted_names = {p.stem for p in deleted}

    cleaned_csv = []
    dropped = []

    for row in csv_rows:
        if row[1] in deleted_names:
            dropped.append(row)
        else:
            cleaned_csv.append(row)

    # -------------------------
    # 2. ADD NEW FILES
    # -------------------------
    if new:
        new_rows = create_rename_metadata_rows(new)
        cleaned_csv.extend(new_rows)

    # -------------------------
    # 3. WRITE OUTPUTS
    # -------------------------
    write_metadata_csv(cleaned_csv, HOARD_METADATA_CSV_PATH)

    if dropped:
        append_metadata_csv(dropped, HOARD_DROPPED_METADATA_CSV_PATH)
    dropped_metadata = []

    # normalize extensions first
    lowercase_extensions(HOARD_PATHS, EXTS)

    # current filesystem files
    all_files = list(map(Path, file_search(HOARD_PATHS, EXTS)))

    # current metadata rows
    metadata_rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)

    # data rows only
    rows = metadata_rows[1:]

    # -----------------------------------
    # BUILD LOOKUP TABLES
    # -----------------------------------

    # filesystem names
    filesystem_names = {f.name: f for f in all_files}

    # metadata names
    metadata_names = {f"{row[1]}{row[2]}": row for row in rows}

    # -----------------------------------
    # REMOVE DELETED FILES
    # -----------------------------------

    updated_rows = []

    for row in rows:
        file_name = f"{row[1]}{row[2]}"

        # file still exists
        if file_name in filesystem_names:
            updated_rows.append(row)

        # file deleted
        else:
            dropped_metadata.append(row)

    # -----------------------------------
    # UPDATE MOVED FILE PATHS
    # -----------------------------------

    for row in updated_rows:
        file_name = f"{row[1]}{row[2]}"

        real_file = filesystem_names[file_name]

        # update parent path
        row[4] = str(real_file.parent)

    # -----------------------------------
    # APPEND NEW FILES
    # -----------------------------------

    new_files = [f for f in all_files if f.name not in metadata_names]

    if new_files:
        new_rows = create_rename_metadata_rows(new_files)
        updated_rows.extend(new_rows)

    # -----------------------------------
    # SAVE RESULTS
    # -----------------------------------

    # archive deleted rows
    if dropped_metadata:
        append_metadata_csv(dropped_metadata, HOARD_DROPPED_METADATA_CSV_PATH)

    # rewrite metadata CSV
    write_metadata_csv(updated_rows, HOARD_METADATA_CSV_PATH)


def build_metadata_rows(files):
    """
    Build CSV rows sorted by creation time (oldest → newest).
    """

    # create (timestamp, file) pairs
    timestamped_files = [(int(os.path.getctime(f)), f) for f in files]

    # SORT BY CREATION TIME
    timestamped_files.sort(key=itemgetter(0))

    rows = []

    for i, (timestamp, f) in enumerate(timestamped_files, 1):
        rows.append([i, f.stem, f.suffix, timestamp, str(f.parent)])

    return rows


def create_metadata_csv(files):
    """
    Full CSV rebuild (authoritative snapshot).
    """

    rows = build_metadata_rows(files)

    with open(HOARD_METADATA_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        w.writerows(rows)


def sync_metadata_state():
    """
    Compare filesystem vs CSV and return diff state.
    """
    csv_rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)

    fs_files = set(file_search(HOARD_PATHS, EXTS))

    csv_paths = set(map(Path, get_absolute_paths_from_metadata_csv(csv_rows)))

    # 1. deleted files (in CSV, not in FS)
    deleted = csv_paths - fs_files

    # 2. new files (in FS, not in CSV)
    new = fs_files - csv_paths

    # 3. existing files
    stable = fs_files & csv_paths

    return {"csv_rows": csv_rows, "deleted": deleted, "new": new, "stable": stable}


def update_metadata_csv():
    sync_data = sync_metadata_state()
    apply_metadata_sync(sync_data)


def get_absolute_paths_from_exif_errors(output):
    """
    Extract absolute file paths from exiftool error output.
    """
    absolute_paths = []

    for line in output.splitlines():

        parts = line.split("- ", 1)

        if len(parts) == 2:
            absolute_paths.append(Path(parts[1].strip()))

    return absolute_paths


def run_exif_error_scan(path):
    """
    Run exiftool, detect errors, move broken files.
    """
    args = ["exiftool", "-r", "-overwrite_original", "-all=", str(path)]

    process = subprocess.run(args, capture_output=True, text=True)

    print(f"\nerr:\n{process.stderr}")
    print(f"\nout:\n{process.stdout}")

    broken_count = 0

    if process.returncode != 0:

        broken_paths = get_absolute_paths_from_exif_errors(process.stderr)

        for p in broken_paths:
            new_destination = HOARD_BROKEN_VIDS_PATH / p.name
            p.replace(new_destination)
            broken_count += 1

    return {"moved": broken_count, "success": process.returncode == 0}
