import argparse

from media_tools.youtube.csv_store import (
    get_metadata_csv_list,
    get_channels_list_from_csv
)

from media_tools.youtube.downloader import download_youtube_videos

from media_tools.constants import HOARD_YOUTUBE_CSV_PATH


def run(args):
    """
    Download YouTube videos from metadata CSV.

    Examples:
    media-tools download --channel "Music" --limit 10
    """

    # -------------------------
    # CLI argument parser
    # -------------------------
    parser = argparse.ArgumentParser(
        prog="media-tools download",
        description="Download YouTube videos from metadata CSV"
    )

    parser.add_argument(
        "--channel",
        required=True,
        help="Channel name (must exist in CSV)"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of videos to download (default: 10)"
    )

    parsed = parser.parse_args(args)

    # -------------------------
    # Load CSV data
    # -------------------------
    rows = get_metadata_csv_list(HOARD_YOUTUBE_CSV_PATH)
    channel_names = get_channels_list_from_csv(rows)

    # -------------------------
    # Validate channel exists
    # -------------------------
    if parsed.channel not in channel_names.values():
        print(f"Invalid channel: {parsed.channel}")
        print("Available channels:")
        for c in channel_names.values():
            print(f" - {c}")
        return

    # -------------------------
    # Run download workflow
    # -------------------------
    download_youtube_videos(
        channel_name=parsed.channel,
        limit=parsed.limit
    )