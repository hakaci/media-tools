import argparse
import os

from media_tools.misc.video_splitter import split_video
from media_tools.constants import (
    DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH,
    DEFAULT_SPLIT_OUTPUT_FOLDER,
)

COMMAND_NAME = "misc"
DESCRIPTION = "Misc utilities like video splitting and small tools"

SPLIT_VIDEO_HELP = """
Split a media file into segments using timestamps.

Usage:
  media-tools misc split-video <video_path> [options]

Options:
  --timestamps     Path to timestamps file
                   Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output\\timestamps.txt

  --output         Output folder
                   Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output

  --no-original    Disable original filename in outputs

Examples:
  media-tools misc split-video "video.mp4"
  media-tools misc split-video "video.mp4" --output "C:\\output"
  media-tools misc split-video "video.mp4" --timestamps "C:\\data\\timestamps.txt"
  media-tools misc split-video "video.mp4" --no-original
"""


MISC_HELP = """
Misc Commands:

  split-video     Split media file into segments using timestamps
"""


def handle_split_video(args):
    if not args:
        print(SPLIT_VIDEO_HELP)
        return

    parser = argparse.ArgumentParser(
        prog="media-tools misc split-video", add_help=False
    )

    parser.add_argument("video_path")
    parser.add_argument("--timestamps", default=DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH)
    parser.add_argument("--output", default=DEFAULT_SPLIT_OUTPUT_FOLDER)
    parser.add_argument("--no-original", action="store_true")

    parsed = parser.parse_args(args)

    if not os.path.exists(parsed.video_path):
        print("Error: video not found")
        return

    if not os.path.exists(parsed.timestamps):
        print(f"Error: timestamps file not found -> {parsed.timestamps}")
        return

    split_video(
        video_path=parsed.video_path,
        timestamps_path=parsed.timestamps,
        include_original_name=not parsed.no_original,
        output_folder=parsed.output,
    )


def run(args):
    if not args:
        print(MISC_HELP)
        return

    cmd = args[0]

    if cmd == "split-video":
        return handle_split_video(args[1:])

    print(f"Unknown command: {cmd}")
    print(MISC_HELP)
