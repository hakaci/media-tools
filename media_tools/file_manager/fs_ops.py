# Search files by extension in multiple roots
from pathlib import Path
from os import walk, makedirs
from os.path import join, exists, relpath, getctime

from media_tools.constants import (
    HOARD_PATHS,
    EXTS,
    REVERSE_NAMING_CONST
)

def file_search(paths, extensions):
    extensions = set(extensions)
    results = set()

    for path in paths:
        p = Path(path)
        if not p.exists():
            continue

        # recursive scan
        for f in p.rglob("*"):
            if f.suffix.lower() in extensions:
                results.add(f.resolve())

    return list(results)

# normalize extensions (.PNG -> .png)
def lowercase_extensions(paths, extensions):
    files = file_search(paths, extensions)

    for f in files:
        # normalize extension to lowercase
        lower_ext = f.suffix.lower()

        # rename only if needed
        if f.suffix != lower_ext:
            new_path = f.with_suffix(lower_ext)
            f.rename(new_path)
        
def empty_hoard_folders():
    # search files given paths
    files = file_search(HOARD_PATHS, EXTS)

    for f in files:
        # delete file
        f.unlink()

def copy_folders_to_another_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not exists(output_folder):
        makedirs(output_folder)

    # Walk through the directory tree
    for root, directories, _ in walk(input_folder):
        for directory in directories:
            # source directory path
            src_dir = join(root, directory)

            # destination directory path (preserve structure)
            dest_dir = join(output_folder, relpath(src_dir, input_folder))

            makedirs(dest_dir, exist_ok=True)

def sort_files_by_creation_date(files):
    # sort files by creation time (oldest → newest)
    return sorted(files, key=getctime)

def rename_a_file_given_name(file, new_file_name):
    # rename the file
    file = Path(file)
    file_extension = file.suffix
    parent_dir = file.parent

    new_file_name = Path(new_file_name)

    # create absolute path with new name for rename function
    absolute_new_file_name = parent_dir / new_file_name.with_suffix(file_extension)

    # rename
    file.rename(absolute_new_file_name)
    
def safe_rename(old_path, new_name):
    # rename helper (keeps logic centralized)
    old_path = Path(old_path)
    new_path = old_path.with_name(new_name)

    old_path.rename(new_path)
    return new_path

def build_path(row):
    # row = [no, file_name, ext, time, parent]
    return Path(row[4]) / f"{row[1]}{row[2]}"


def rename_all_from_metadata(rows, safe_rename):
    # rename using reverse naming rule
    for row in rows:
        old_path = build_path(row)

        new_name = f"{REVERSE_NAMING_CONST - int(row[0])}{old_path.suffix}"

        safe_rename(old_path, new_name)
        
def replace_strings_in_filenames(
    files,
    targets,
    replacement
):
    renamed = []

    for file_path in files:
        new_name = file_path.name

        for target in targets:
            new_name = new_name.replace(
                target,
                replacement
            )

        if new_name != file_path.name:
            new_path = file_path.with_name(new_name)

            file_path.rename(new_path)

            renamed.append((file_path, new_path))

    return renamed