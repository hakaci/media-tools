import csv
from os.path import exists

from media_tools.youtube.extractor import fetch_video_metadata
from media_tools.youtube.csv_store import get_relevant_video_infos

from media_tools.config import HOARD_YOUTUBE_CSV_PATH, FIELDS


# -------------------------
# WRITE TO CSV
# -------------------------
def append_metadata_to_csv(rows):
    # create file if missing
    if not exists(HOARD_YOUTUBE_CSV_PATH):
        with open(HOARD_YOUTUBE_CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)

    # append rows
    with open(HOARD_YOUTUBE_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        if f.tell() == 0:
            w.writerow(FIELDS)

        for row in rows:
            w.writerow(row)


# -------------------------
# SINGLE VIDEO FLOW
# -------------------------
def append_single_video_metadata(urls):
    all_data = []

    for url in urls:
        info = fetch_video_metadata(url)

        if not info:
            continue

        if isinstance(info, list):
            info = info[0]

        all_data.append(info)

    rows = get_relevant_video_infos(all_data)

    append_metadata_to_csv(rows)


# -------------------------
# PLAYLIST / CHANNEL FLOW
# -------------------------
def append_playlist_metadata(url):
    video_infos = fetch_video_metadata(url)

    if not video_infos:
        return

    rows = get_relevant_video_infos(video_infos)

    append_metadata_to_csv(rows)