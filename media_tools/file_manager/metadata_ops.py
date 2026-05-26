from genericpath import getctime
from pathlib import Path
from operator import itemgetter
import csv
import os.path
from media_tools.file_manager.csv_ops import (
    get_metadata_csv_list,
    get_absolute_paths_from_metadata_csv,
    get_last_row_of_csv,
    append_metadata_csv,
    write_metadata_csv
)
from media_tools.file_manager.fs_ops import (
    file_search,
    rename_a_file_given_name
)

from media_tools.constants import (
    HOARD_METADATA_CSV_PATH,
    HOARD_DROPPED_METADATA_CSV_PATH,
    PATHS,
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
    pathListNames = []
    allFilesNames = []
    droppedMetadataList = []
    filesChangedDirectoryReal = []

    metadataCSVList = get_metadata_csv_list(HOARD_METADATA_CSV_PATH)
    newItemMetaData = metadataCSVList.copy()

    allFiles = list(map(Path, file_search(PATHS, EXTS)))

    # build CSV path list
    pathList = list(map(Path, get_absolute_paths_from_metadata_csv(metadataCSVList)))

    # extract names
    for p in pathList:
        pathListNames.append(p.stem)

    for f in allFiles:
        allFilesNames.append(f.stem)

    # find deleted items
    deletedItems = set(pathListNames) - set(allFilesNames)

    # remove deleted from metadata + collect dropped
    i = 0
    while i < len(newItemMetaData):
        if newItemMetaData[i][1] in deletedItems:
            droppedMetadataList.append(newItemMetaData.pop(i))
        else:
            i += 1

    # detect moved files
    newItemMetaDataPath = list(map(Path, get_absolute_paths_from_metadata_csv(newItemMetaData)))
    filesChangedDirectory = set(newItemMetaDataPath) - set(allFiles)

    # resolve new locations
    for moved in filesChangedDirectory:
        name = moved.stem

        for i, f in enumerate(allFiles):
            if f.stem == name:
                filesChangedDirectoryReal.append(f)
                break

    # update parent paths
    for f in filesChangedDirectoryReal:
        for row in newItemMetaData:
            if row[1] == f.stem:
                row[4] = str(f.parent)
                break

    # persist changes
    append_metadata_csv(droppedMetadataList, HOARD_DROPPED_METADATA_CSV_PATH)
    write_metadata_csv(newItemMetaData, HOARD_METADATA_CSV_PATH)
    
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