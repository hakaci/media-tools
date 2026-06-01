import subprocess
from pathlib import Path

from media_tools.constants import HOARD_PATH


# remove all metadata using exiftool
def clear_metadata(path_to_clean):
    args = ["exiftool", "-overwrite_original", "-all=", str(path_to_clean)]

    process = subprocess.run(args)

    if process.returncode == 0:
        print("metadata cleaned successfully")
    else:
        print(f"metadata clean failed: {process.returncode}")


# clean metadata safely using temp folder swap
def clean_metadata(paths):
    print("\nCleaner started.")

    if not paths:
        print("No files to clean\n")
        return

    temp_folder = HOARD_PATH / "temp"

    temp_folder.mkdir(exist_ok=True)

    temp_paths = []

    # move files to temp
    for file in paths:
        file = Path(file)
        temp_path = temp_folder / file.name

        file.replace(temp_path)
        temp_paths.append((file, temp_path))

    # strip metadata on temp folder
    clear_metadata(temp_folder)

    # restore files back to original locations
    for original, temp in temp_paths:
        temp.replace(original)

    # cleanup temp folder
    try:
        temp_folder.rmdir()
    except OSError:
        pass

    print("Cleaner finished.\n")
