import argparse

from media_tools.misc.video_splitter import split_video
from media_tools.constants import (
    DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH,
    DEFAULT_SPLIT_OUTPUT_FOLDER,
)

COMMAND_NAME = "misc"
DESCRIPTION = "Misc utilities like video splitting and small tools"


def run(args):
    parser = argparse.ArgumentParser(
        prog="media-tools misc",
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="cmd", metavar="command")
    sub.required = False

    split_video_parser = sub.add_parser(
        "split-video", help="Split media file into segments using timestamps"
    )

    split_video_parser.add_argument("video_path", help="Path to input video file")

    split_video_parser.add_argument(
        "--timestamps",
        default=DEFAULT_SPLIT_VIDEO_TIMESTAMPS_PATH,
        help="Path to timestamps file. Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output\\timestamps.txt",
    )

    split_video_parser.add_argument(
        "--output",
        default=DEFAULT_SPLIT_OUTPUT_FOLDER,
        help="Output folder for split segments. Default: C:\\Users\\hakaci-desktop\\Videos\\video_split_output",
    )

    split_video_parser.add_argument(
        "--no-original",
        action="store_true",
        help="Don't include original filename in outputs",
    )

    parsed = parser.parse_args(args)

    if parsed.cmd is None:
        parser.print_help()
        return

    if parsed.cmd == "split-video":
        split_video(
            video_path=parsed.video_path,
            timestamps_path=parsed.timestamps,
            include_original_name=not parsed.no_original,
            output_folder=parsed.output,
        )
        return

    parser.print_help()
