import argparse

from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata
)


def run(args):
    """
    Append YouTube metadata into CSV.

    Examples:
    media-tools metadata --url <video1> <video2>
    media-tools metadata --playlist <url>
    """

    parser = argparse.ArgumentParser(
        prog="media-tools metadata",
        description="Append YouTube metadata into CSV"
    )

    # -------------------------
    # Multiple positional URLs
    # -------------------------
    parser.add_argument(
        "--url",
        nargs="+",
        help="One or more YouTube video URLs"
    )

    parser.add_argument(
        "--playlist",
        help="Playlist or channel URL"
    )

    parsed = parser.parse_args(args)

    # -------------------------
    # Validation
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