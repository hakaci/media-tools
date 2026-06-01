import csv
from pathlib import Path

from media_tools.file_manager.fs_ops import encode_to_mp3
from media_tools.file_manager.fs_ops import file_search


def get_new_file_paths(files, csv_file_path):
    # read converted file names from CSV
    converted_file_names = set()

    with open(csv_file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        next(reader)  # skip header

        for row in reader:
            converted_file_names.add(row[0])

    # get file names from filesystem
    file_names = [file.name for file in files]

    # find new file names
    new_file_names = set(file_names) - converted_file_names

    # map names to absolute paths
    file_path_dict = {file_path.name: file_path for file_path in files}

    # resolve absolute paths
    new_file_paths = [
        file_path_dict[file_name]
        for file_name in new_file_names
        if file_name in file_path_dict
    ]

    return new_file_paths


def run_mp3_conversion(folder_path, extensions, csv_file_path, temp_path):

    # scan folder for media files
    files = file_search([folder_path], extensions)

    # detect new files (not yet converted)
    new_files = get_new_file_paths(files, csv_file_path)

    # check if there are files to convert
    if not new_files:
        print("No files to convert")
        return []

    # convert files
    converted = encode_to_mp3(new_files, temp_path)

    # append converted file names to CSV
    with open(csv_file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        for f in converted:
            writer.writerow([f.name])

    return converted
