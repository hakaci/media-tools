import argparse

from media_tools.youtube.append_metadata import (
    append_single_video_metadata,
    append_playlist_metadata,
)

from media_tools.youtube.downloader import download_youtube_videos
from media_tools.youtube.ui import choose_channel

COMMAND_NAME = "youtube"
DESCRIPTION = "Download and process YouTube media"


YOUTUBE_HELP = """
YouTube Commands:

  metadata     Append video or playlist metadata into CSV
  download     Download videos from metadata CSV
"""


METADATA_HELP = """
Append YouTube video metadata into CSV.

Usage:
  media-tools youtube metadata [--url URL ...] [--playlist URL]

Options:
  --url        One or more video URLs
  --playlist   Playlist or channel URL

Examples:
  media-tools youtube metadata --url https://youtube.com/watch?v=xxxx
  media-tools youtube metadata --url url1 url2 url3
  media-tools youtube metadata --playlist https://youtube.com/playlist?list=xxxx
"""


DOWNLOAD_HELP = """
Download YouTube videos from metadata CSV.

Usage:
  media-tools youtube download [--channel NAME] [--limit N]

Options:
  --channel   Channel name from CSV (default: interactive)
  --limit     Number of videos to download (default: 10)

Examples:
  media-tools youtube download --channel "Music"
  media-tools youtube download --channel "Music" --limit 20
  media-tools youtube download
"""


def print_youtube_help():
    print(YOUTUBE_HELP)


def handle_metadata(args):
    if not args:
        print(METADATA_HELP)
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--url", nargs="+")
    parser.add_argument("--playlist")

    parsed = parser.parse_args(args)

    if parsed.url:
        append_single_video_metadata(parsed.url)
        return

    if parsed.playlist:
        append_playlist_metadata(parsed.playlist)
        return

    print(METADATA_HELP)


def handle_download(args):
    if not args:
        print(DOWNLOAD_HELP)
        return

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--channel")
    parser.add_argument("--limit", type=int)

    parsed = parser.parse_args(args)

    channel = parsed.channel or choose_channel()

    limit = parsed.limit
    if limit is None:
        try:
            limit = int(input("Enter download limit: "))
        except ValueError:
            limit = 10

    download_youtube_videos(channel_name=channel, limit=limit)


def run(args):
    if not args:
        print_youtube_help()
        return

    cmd = args[0]

    if cmd == "metadata":
        return handle_metadata(args[1:])

    if cmd == "download":
        return handle_download(args[1:])

    print_youtube_help()
