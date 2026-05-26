import argparse

from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata
)

from media_tools.youtube.downloader import download_youtube_videos


def run(args):
    parser = argparse.ArgumentParser(prog="media-tools youtube")

    sub = parser.add_subparsers(dest="cmd")

    # -------------------------
    # METADATA COMMAND
    # -------------------------
    meta = sub.add_parser("metadata")
    meta.add_argument("--url", nargs="+")
    meta.add_argument("--playlist")

    # -------------------------
    # DOWNLOAD COMMAND
    # -------------------------
    dl = sub.add_parser("download")
    dl.add_argument("--channel", required=True)
    dl.add_argument("--limit", type=int, default=10)

    parsed = parser.parse_args(args)

    # -------------------------
    # METADATA ROUTING
    # -------------------------
    if parsed.cmd == "metadata":

        if parsed.playlist:
            append_playlist_metadata(parsed.playlist)

        elif parsed.url:
            append_single_video_metadata(parsed.url)

        else:
            parser.error("metadata requires --url or --playlist")

    # -------------------------
    # DOWNLOAD ROUTING
    # -------------------------
    elif parsed.cmd == "download":
        download_youtube_videos(
            channel_name=parsed.channel,
            limit=parsed.limit
        )

    else:
        parser.print_help()