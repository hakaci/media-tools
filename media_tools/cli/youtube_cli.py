import argparse

from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata,
)

from media_tools.youtube.downloader import download_youtube_videos
from media_tools.youtube.ui import choose_channel

COMMAND_NAME = "youtube"
DESCRIPTION = "Download and process YouTube media"


def run(args):
    parser = argparse.ArgumentParser(
        prog="media-tools youtube",
        add_help=True,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    sub = parser.add_subparsers(dest="cmd", metavar="command")
    sub.required = False

    metadata_parser = sub.add_parser(
        "metadata", help="Append video or playlist metadata into CSV"
    )
    metadata_parser.add_argument(
        "--url", nargs="+", help="One or more YouTube video URLs"
    )
    metadata_parser.add_argument("--playlist", help="Playlist or channel URL")

    download_parser = sub.add_parser(
        "download", help="Download videos from metadata CSV"
    )
    download_parser.add_argument(
        "--channel", help="Channel name from CSV (default: interactive selection)"
    )

    download_parser.add_argument(
        "--limit", type=int, help="Number of videos to download (default: 10)"
    )

    parsed = parser.parse_args(args)

    if parsed.cmd is None:
        parser.print_help()
        return

    # -------------------------
    # METADATA
    # -------------------------
    if parsed.cmd == "metadata":
        if parsed.url:
            append_single_video_metadata(parsed.url)
            return

        if parsed.playlist:
            append_playlist_metadata(parsed.playlist)
            return

        return

    # -------------------------
    # DOWNLOAD
    # -------------------------
    if parsed.cmd == "download":
        channel = parsed.channel or choose_channel()

        limit = parsed.limit
        if limit is None:
            try:
                limit = int(input("Enter download limit: "))
            except ValueError:
                limit = 10

        download_youtube_videos(channel_name=channel, limit=limit)

    parser.print_help()
