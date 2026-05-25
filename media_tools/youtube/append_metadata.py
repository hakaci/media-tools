import csv
from os.path import exists

from media_tools.youtube.extractor import fetch_video_metadata
from media_tools.youtube.csv_store import (
    FIELDNAMES,
    get_relevant_video_infos
)

from media_tools.constants import HOARD_YOUTUBE_CSV_PATH


# Write rows into CSV
def _write_csv(rows):
    with open(HOARD_YOUTUBE_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDNAMES).writerows(rows)


# Ensure CSV exists with header
def _ensure_csv():
    if not exists(HOARD_YOUTUBE_CSV_PATH):
        with open(HOARD_YOUTUBE_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDNAMES).writeheader()


# Append metadata from multiple single video URLs
def append_single_video_metadata(urls):
    _ensure_csv()

    # Fetch metadata for each URL
    infos = [fetch_video_metadata(u) for u in urls]

    # Normalize data into CSV format
    rows = get_relevant_video_infos(infos)

    _write_csv(rows)

    print(f"Added {len(rows)} videos")


# Append metadata from playlist/channel
def append_playlist_metadata(url):
    _ensure_csv()

    print(f"\nFetching metadata:\n{url}")

    # Fetch playlist/channel metadata
    infos = fetch_video_metadata(url)

    # Normalize data into CSV format
    rows = get_relevant_video_infos(infos)

    _write_csv(rows)

    print(f"Added {len(rows)} videos")