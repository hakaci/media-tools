import argparse

from media_tools.youtube.csv_store import (
    get_metadata_csv_list,
    get_channels_list_from_csv
)

from media_tools.youtube.ui import choose_channel

from media_tools.youtube.downloader import download_youtube_videos

from media_tools.constants import HOARD_YOUTUBE_CSV_PATH


def run(args):
    """
    Download YouTube videos from metadata CSV.

    Examples:
    media-tools download
    media-tools download --channel "channel name"
    media-tools download --channel "channel name" --limit 10
    """

    # Create CLI argument parser
    parser = argparse.ArgumentParser(
        prog="media-tools download",
        description="Download YouTube videos from metadata CSV"
    )

    # Optional channel argument
    parser.add_argument(
        "--channel",
        help="Channel name to download from"
    )

    # Optional download limit
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of videos to download (default: 10)"
    )

    # Parse CLI arguments
    parsed = parser.parse_args(args)

    # Load metadata CSV rows
    rows = get_metadata_csv_list(HOARD_YOUTUBE_CSV_PATH)

    # Get available channels from CSV
    channel_names = get_channels_list_from_csv(rows)

    # If user passed --channel use it
    # otherwise open interactive selection menu
    chosen_channel = parsed.channel

    if not chosen_channel:
        chosen_channel = choose_channel(channel_names)

    # Start download workflow
    download_youtube_videos(
        channel_name=chosen_channel,
        limit=parsed.limit
    )