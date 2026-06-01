import subprocess
from pathlib import Path
from os import walk, makedirs
from os.path import join, exists, relpath, getctime

from media_tools.constants import HOARD_PATHS, EXTS, REVERSE_NAMING_CONST


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


def encode_to_mp3(files, temp_path):
    converted = []

    for file in files:
        # new file name
        new_file_name = f"{file.stem}.mp3"

        # temp output directory (preserve folder structure)
        output_dir = Path(temp_path) / file.parent.name

        # create folder if not exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # final output path
        output_path = output_dir / new_file_name

        # ffmpeg command
        args = [
            "ffmpeg",
            "-i",
            str(file),
            "-vn",
            "-acodec",
            "libmp3lame",
            "-ab",
            "128k",
            str(output_path),
        ]

        # execute ffmpeg
        process = subprocess.run(args)

        # success case
        if process.returncode == 0:
            print(f"successfully converted {file}")
            converted.append(file)

        # failure case
        else:
            print(f"error converting {file}, errno: {process.returncode}")

            # remove corrupted output if exists
            if output_path.exists():
                output_path.unlink()

    return converted


def path_search(root_path):
    """
    Return all files and folders recursively.

    Paths are returned deepest-first so parent folder
    renames do not break child paths.
    """

    root_path = Path(root_path)

    paths = []

    for path in root_path.rglob("*"):
        paths.append(path)

    return sorted(
        paths,
        key=lambda p: len(p.parts),
        reverse=True,
    )


def replace_strings_in_filenames(
    paths,
    replacement_args,
    include_folders=True,
):
    if len(replacement_args) % 2 != 0:
        print("Replacement arguments must be pairs.")
        return

    replacements = []

    for i in range(0, len(replacement_args), 2):
        replacements.append((replacement_args[i], replacement_args[i + 1]))

    for path in paths:

        if path.is_dir() and not include_folders:
            continue

        new_name = path.name

        for old, new in replacements:
            new_name = new_name.replace(old, new)

        if new_name == path.name:
            continue

        path.rename(path.with_name(new_name))

        print(f"Renamed: {path.name} -> {new_name}")


def remove_prefix_from_filenames(
    paths,
    prefix,
    include_folders=True,
):
    for path in paths:

        if path.is_dir() and not include_folders:
            continue

        new_name = path.name

        if new_name.startswith(prefix):
            new_name = new_name[len(prefix) :]

        if new_name == path.name:
            continue

        new_path = path.with_name(new_name)

        path.rename(new_path)

        print(f"Renamed: {path.name} -> {new_name}")


def remove_suffix_from_filenames(
    paths,
    suffix,
    include_folders=True,
):
    for path in paths:

        if path.is_dir() and not include_folders:
            continue

        new_name = path.name

        if new_name.endswith(suffix):
            new_name = new_name[: -len(suffix)]

        if new_name == path.name:
            continue

        new_path = path.with_name(new_name)

        path.rename(new_path)

        print(f"Renamed: {path.name} -> {new_name}")
