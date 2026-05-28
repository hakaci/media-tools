import subprocess
from random import randint

from media_tools.file_manager.fs_ops import (
    file_search,
    sort_files_by_creation_date
)

from media_tools.constants import (
    HOARD_PATHS,
    HOARD_BROKEN_VIDS_PATH,
)

# video formats to convert
EXTENSIONS_TO_ENCODE = [
    ".mov",
    ".webm",
    ".mkv"
]


# Convert videos into mp4
def convert_videos():
    print("\nVideo converter started.")

    files = file_search(
        HOARD_PATHS,
        EXTENSIONS_TO_ENCODE
    )

    # oldest -> newest
    files = sort_files_by_creation_date(files)

    # nothing to convert
    if not files:
        print("\nNo files to convert\n")
        return []

    converted_files = []

    for file in files:
        # randomized output name
        output_name = (
            file.parent /
            f"{file.stem}_{randint(10000, 99999)}.mp4"
        )

        # ffmpeg command
        args = [
            "ffmpeg",
            "-i", str(file),
            "-c:v", "libx264",
            "-c:a", "aac",
            str(output_name)
        ]

        # execute ffmpeg
        process = subprocess.run(args)

        # success
        if process.returncode == 0:
            print(f"converted: {file.name}")

            # remove original
            if file.exists():
                file.unlink()

            converted_files.append(output_name)

        # failure
        else:
            print(f"failed: {file.name}")

            # remove broken output
            if output_name.exists():
                output_name.unlink()

            # move broken source
            file.replace(
                HOARD_BROKEN_VIDS_PATH / file.name
            )

    print("Video converter finished.\n")

    return converted_files