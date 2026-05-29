import argparse
import os

from media_tools.misc.video_splitter import split_video
from media_tools.constants import (
    DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH,
    DEFAULT_SPLIT_OUTPUT_FOLDER
)


def run(args):
    parser = argparse.ArgumentParser(
        prog="media-tools misc split-video",
        description="Split media file using timestamps.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "video_path",
        help="Path to input media file"
    )

    parser.add_argument(
        "--timestamps",
        default=DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH,
        help="Path to timestamps file"
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_SPLIT_OUTPUT_FOLDER,
        help="Output folder"
    )

    parser.add_argument(
    "--no-original",
    action="store_true",
    help="Disable original filename"
    )

    parsed_args = parser.parse_args(args)

    include_original_name = not parsed_args.no_original

    if not os.path.exists(parsed_args.video_path):
        print("Error: video not found")
        return

    if not os.path.exists(parsed_args.timestamps):
        print(f"Error: timestamps file not found -> {parsed_args.timestamps}")
        return

    split_video(
        video_path=parsed_args.video_path,
        timestamps_path=parsed_args.timestamps,
        include_original_name=include_original_name,
        output_folder=parsed_args.output
    )