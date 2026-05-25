import argparse

from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata
)


def run(args):
    """
    Append YouTube metadata into CSV.

    Examples:
    media-tools metadata --url <video>
    media-tools metadata --url <video1> --url <video2>
    media-tools metadata --playlist <url>
    """

    # -------------------------
    # CLI argument parser
    # -------------------------
    parser = argparse.ArgumentParser(
        prog="media-tools metadata",
        description="Append YouTube metadata into CSV"
    )

    parser.add_argument(
        "--url",
        action="append",
        help="Single video URL(s)"
    )

    parser.add_argument(
        "--playlist",
        help="Playlist or channel URL"
    )

    parsed = parser.parse_args(args)

    # -------------------------
    # Require explicit input
    # -------------------------
    if not parsed.url and not parsed.playlist:
        print("Error: provide --url or --playlist")
        return

    # -------------------------
    # Single video mode
    # -------------------------
    if parsed.url:
        append_single_video_metadata(parsed.url)

    # -------------------------
    # Playlist mode
    # -------------------------
    if parsed.playlist:
        append_playlist_metadata(parsed.playlist)