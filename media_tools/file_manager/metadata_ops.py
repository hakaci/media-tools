from genericpath import getctime
from pathlib import Path
from operator import itemgetter
import csv
import os.path
from media_tools.file_manager.csv_ops import (
    get_metadata_csv_list,
    get_last_row_of_csv,
    append_metadata_csv,
    write_metadata_csv
)
from media_tools.file_manager.fs_ops import (
    file_search,
    rename_a_file_given_name,
    lowercase_extensions
)

from media_tools.constants import (
    HOARD_METADATA_CSV_PATH,
    HOARD_DROPPED_METADATA_CSV_PATH,
    HOARD_PATHS,
    EXTS,
    FIELDS
)


def create_rename_metadata_rows(files):
    metadataRows = []

    # get last row of metadataCSV
    lastRowCSV = get_last_row_of_csv(HOARD_METADATA_CSV_PATH)
    lastNo = int(lastRowCSV[0])
    lastName = int(lastRowCSV[1])

    # create (timestamp, file) list
    timestamps_filepaths = [
        (int(getctime(file)), file)
        for file in files
    ]

    # sort by creation time
    timestamps_filepaths.sort(key=itemgetter(0))

    # create rows sorted
    for i, (timestamp, file) in enumerate(timestamps_filepaths, 1):
        new_name = str(lastName - i)
        rename_a_file_given_name(file, new_name)

        metadataRows.append([
            str(lastNo + i),
            new_name,
            str(file.suffix),
            str(timestamp),
            str(file.parent)
        ])

    return metadataRows

def update_metadata_csv():
    dropped_metadata = []

    # normalize extensions first
    lowercase_extensions(HOARD_PATHS, EXTS)

    # current filesystem files
    all_files = list(map(Path, file_search(HOARD_PATHS, EXTS)))

    # current metadata rows
    metadata_rows = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)

    # keep header
    header = metadata_rows[0]

    # data rows only
    rows = metadata_rows[1:]

    # -----------------------------------
    # BUILD LOOKUP TABLES
    # -----------------------------------

    # filesystem names
    filesystem_names = {
        f.name: f
        for f in all_files
    }

    # metadata names
    metadata_names = {
        f"{row[1]}{row[2]}": row
        for row in rows
    }

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

    new_files = [
        f for f in all_files
        if f.name not in metadata_names
    ]

    if new_files:
        new_rows = create_rename_metadata_rows(new_files)
        updated_rows.extend(new_rows)

    # -----------------------------------
    # SAVE RESULTS
    # -----------------------------------

    # archive deleted rows
    if dropped_metadata:
        append_metadata_csv(
            dropped_metadata,
            HOARD_DROPPED_METADATA_CSV_PATH
        )

    # rewrite metadata CSV
    write_metadata_csv(
        updated_rows,
        HOARD_METADATA_CSV_PATH
    )
    
def build_metadata_rows(files):
    # convert files → csv rows
    rows = []

    for i, f in enumerate(files, 1):
        rows.append([
            i,
            f.stem,
            f.suffix,
            int(os.path.getctime(f)),
            str(f.parent)
        ])

    return rows


def create_metadata_csv(files):
    # write full CSV
    with open(HOARD_METADATA_CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        w.writerow(FIELDS)
        w.writerows(build_metadata_rows(files))