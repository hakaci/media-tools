import csv
from pathlib import Path

from media_tools.constants import HOARD_METADATA_CSV_PATH, FIELDS


def get_metadata_csv_list(path):
    # load CSV into memory
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def write_metadata_csv(listToWrite, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        # get file writer object
        csvwriter = csv.writer(f, delimiter=",")

        # Write title row
        csvwriter.writerow(FIELDS)

        # write data to rows with list
        csvwriter.writerows(listToWrite)


def append_metadata_csv(listToAppend, path):
    with open(path, "a", newline="", encoding="utf-8") as f:
        # get file writer object
        csvwriter = csv.writer(f, delimiter=",")

        # append data to rows with list
        csvwriter.writerows(listToAppend)


def get_last_row_of_csv(path):
    # get metadata list
    metaDataList = get_metadata_csv_list(path)

    # return last row (without modifying list)
    return metaDataList[-1]


def get_absolute_paths_from_metadata_csv(metadataCSVList):
    absolutePaths = []

    # delete title row
    del metadataCSVList[0]

    # create and append absolute paths
    for row in metadataCSVList:
        absolutePaths.append(Path(row[4]) / f"{row[1]}{row[2]}")

    return absolutePaths


def get_file_path_from_name(nameList):
    pathList = []

    # get paths from CSV for searching
    pathsFromCSV = get_absolute_paths_from_metadata_csv(
        get_metadata_csv_list(HOARD_METADATA_CSV_PATH)
    )

    pathsFromCSV = list(map(Path, pathsFromCSV))

    # iterate names for searching
    for name in nameList:
        for path in pathsFromCSV:
            # if found, add path then stop searching
            if str(name) == path.name:
                pathList.append(path)
                break

    return pathList


def get_file_path_from_stem(stemList):
    pathList = []

    # get paths from CSV for searching
    pathsFromCSV = get_absolute_paths_from_metadata_csv(
        get_metadata_csv_list(HOARD_METADATA_CSV_PATH)
    )

    pathsFromCSV = list(map(Path, pathsFromCSV))

    # iterate stems for searching
    for stem in stemList:
        for path in pathsFromCSV:
            # if found, add path to result then break
            if str(stem) == path.stem:
                pathList.append(path)
                break

    return pathList
