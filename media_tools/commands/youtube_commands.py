import argparse

from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata
)

from media_tools.youtube.downloader import download_youtube_videos


def run(args):
    parser = argparse.ArgumentParser(
        prog="media-tools youtube",
        description="YouTube tools"
    )

    subparsers = parser.add_subparsers(dest="command")

    # -------------------------
    # metadata command
    # -------------------------
    meta = subparsers.add_parser("metadata", help="Fetch and store video metadata")
    meta.add_argument("--url", nargs="+", help="One or more video URLs")
    meta.add_argument("--playlist", help="Playlist or channel URL")

    # -------------------------
    # download command
    # -------------------------
    dl = subparsers.add_parser("download", help="Download videos from CSV")
    dl.add_argument("--channel", help="Channel name from CSV")
    dl.add_argument("--limit", type=int, default=10, help="Download limit")

    parsed = parser.parse_args(args)

    # -------------------------
    # ROUTING
    # -------------------------
    if parsed.command == "metadata":

        if parsed.url:
            append_single_video_metadata(parsed.url)
            return

        if parsed.playlist:
            append_playlist_metadata(parsed.playlist)
            return

        parser.parse_args(["metadata", "--help"])
        return

    if parsed.command == "download":
        download_youtube_videos(
            channel_name=parsed.channel,
            limit=parsed.limit
        )
        return

    parser.print_help()