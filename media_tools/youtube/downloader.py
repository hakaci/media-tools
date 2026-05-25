import csv
from os.path import join

import yt_dlp

from media_tools.youtube.csv_store import (
    get_metadata_csv_list,
    get_false_download_status_rows
)

from media_tools.constants import (
    HOARD_YOUTUBE_CSV_PATH,
    HOARD_YOUTUBE_DOWNLOAD_PATH
)


def download_youtube_videos(channel_name, limit):
    """
    Download videos from selected channel.
    """

    filtered_rows = []

    # Get all rows from CSV
    rows = get_metadata_csv_list(HOARD_YOUTUBE_CSV_PATH)

    # Filter rows by selected channel
    for row in rows[1:]:
        if row[2] == channel_name:
            filtered_rows.append(row)

    # Get limited amount of non-downloaded videos
    filtered_rows = get_false_download_status_rows(
        filtered_rows,
        limit
    )

    # yt-dlp configuration
    ydl_opts = {
        'format_sort': ['ext', 'res:1080', '+vbr'],

        # Output filename format
        'outtmpl': join(
            HOARD_YOUTUBE_DOWNLOAD_PATH,
            '%(upload_date)s - %(title)s - %(channel)s.%(ext)s'
        ),
    }

    # Initialize yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        # Iterate through selected videos
        for filtered_row in filtered_rows:

            # Get video ID from CSV row
            video_id = filtered_row[0]

            # Construct video URL
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            try:
                # Download video
                ydl.download([video_url])

                print(f"\nDownloaded: {video_id}")

                # Update download status in rows
                for index, row in enumerate(rows):

                    if row[0] == video_id:
                        rows[index][4] = True

            except Exception as e:
                print(f"\nFailed: {video_id}")
                print(e)

    # Save updated CSV rows
    with open(
        HOARD_YOUTUBE_CSV_PATH,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # Write all rows back into CSV
        writer.writerows(rows)